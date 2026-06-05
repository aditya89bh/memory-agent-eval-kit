"""Benchmark suite registry support."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class BenchmarkSuiteRegistration:
    """Metadata for a registered benchmark suite."""

    name: str
    dataset_path: Path
    description: str = ""
    version: str = "unknown"

    def to_dict(self) -> dict[str, str]:
        payload = asdict(self)
        payload["dataset_path"] = str(self.dataset_path)
        return payload


class BenchmarkRegistry:
    """In-process registry for built-in and external benchmark suites."""

    def __init__(self) -> None:
        self._suites: dict[str, BenchmarkSuiteRegistration] = {}

    def register(self, suite: BenchmarkSuiteRegistration) -> None:
        if not suite.name:
            raise ValueError("suite name is required")
        if suite.name in self._suites:
            raise ValueError(f"Benchmark suite already registered: {suite.name}")
        self._suites[suite.name] = suite

    def get(self, name: str) -> BenchmarkSuiteRegistration:
        try:
            return self._suites[name]
        except KeyError as exc:
            raise KeyError(f"Unknown benchmark suite: {name}") from exc

    def list(self) -> list[BenchmarkSuiteRegistration]:
        return sorted(self._suites.values(), key=lambda suite: suite.name)


DEFAULT_REGISTRY = BenchmarkRegistry()


def register_benchmark_suite(
    name: str,
    dataset_path: Path,
    *,
    description: str = "",
    version: str = "unknown",
    registry: BenchmarkRegistry = DEFAULT_REGISTRY,
) -> BenchmarkSuiteRegistration:
    """Register an external benchmark suite with a registry."""

    suite = BenchmarkSuiteRegistration(
        name=name,
        dataset_path=dataset_path,
        description=description,
        version=version,
    )
    registry.register(suite)
    return suite
