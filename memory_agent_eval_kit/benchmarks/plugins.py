"""Plugin discovery for external benchmark suites."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path
from typing import Protocol

from memory_agent_eval_kit.benchmarks.registry import BenchmarkRegistry, BenchmarkSuiteRegistration

PLUGIN_ENTRY_POINT_GROUP = "memory_agent_eval_kit.benchmark_suites"


class BenchmarkSuitePlugin(Protocol):
    """Callable plugin contract for benchmark suite registration."""

    def __call__(self, registry: BenchmarkRegistry) -> None: ...


@dataclass(frozen=True)
class LoadedBenchmarkPlugin:
    """Metadata for a discovered benchmark plugin."""

    name: str
    module: str


def load_benchmark_plugins(
    registry: BenchmarkRegistry,
    *,
    group: str = PLUGIN_ENTRY_POINT_GROUP,
) -> list[LoadedBenchmarkPlugin]:
    """Load benchmark suite plugins from Python entry points."""

    loaded: list[LoadedBenchmarkPlugin] = []
    for entry_point in metadata.entry_points(group=group):
        plugin = entry_point.load()
        _run_plugin(plugin, registry)
        loaded.append(
            LoadedBenchmarkPlugin(
                name=entry_point.name,
                module=f"{entry_point.module}:{entry_point.attr or ''}".rstrip(":"),
            )
        )
    return loaded


def register_suite_plugin(
    *,
    name: str,
    dataset_path: Path,
    description: str = "",
    version: str = "unknown",
) -> BenchmarkSuitePlugin:
    """Create a plugin callable that registers one benchmark suite."""

    def plugin(registry: BenchmarkRegistry) -> None:
        registry.register(
            BenchmarkSuiteRegistration(
                name=name,
                dataset_path=dataset_path,
                description=description,
                version=version,
            )
        )

    return plugin


def _run_plugin(plugin: Callable[[BenchmarkRegistry], None], registry: BenchmarkRegistry) -> None:
    plugin(registry)
