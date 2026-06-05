"""Benchmark suite version metadata."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkSuiteVersion:
    """Metadata describing a benchmark suite version."""

    version: str
    description: str


SUITE_VERSIONS: tuple[BenchmarkSuiteVersion, ...] = (
    BenchmarkSuiteVersion("v1", "Original core memory benchmark categories."),
    BenchmarkSuiteVersion("v2", "Research toolkit suites for safety, drift, and poisoning."),
    BenchmarkSuiteVersion(
        "v3", "Benchmark authority suites for enterprise and multi-agent memory."
    ),
)

CURRENT_SUITE_VERSION = "v3"
