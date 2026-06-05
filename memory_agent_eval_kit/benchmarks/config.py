"""Benchmark suite configuration."""

from __future__ import annotations

from dataclasses import dataclass, field

from memory_agent_eval_kit.models import Category


@dataclass(frozen=True)
class BenchmarkSuiteConfig:
    """Selection controls for a benchmark run."""

    suite_name: str = "default"
    categories: list[Category] | None = None
    stress: bool = False
    metadata: dict[str, str] = field(default_factory=dict)

    @classmethod
    def for_categories(
        cls, categories: list[Category], suite_name: str = "custom"
    ) -> BenchmarkSuiteConfig:
        return cls(suite_name=suite_name, categories=categories)
