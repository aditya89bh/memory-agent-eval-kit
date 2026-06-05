"""Benchmark comparison across named suite versions."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from memory_agent_eval_kit.reports.comparison import BenchmarkComparison, compare_results


@dataclass(frozen=True)
class VersionComparison:
    """Score and category deltas for a pair of benchmark suite versions."""

    baseline_version: str
    candidate_version: str
    comparison: BenchmarkComparison

    def to_dict(self) -> dict[str, Any]:
        return {
            "baseline_version": self.baseline_version,
            "candidate_version": self.candidate_version,
            **self.comparison.to_dict(),
        }


@dataclass(frozen=True)
class BenchmarkVersionComparisonReport:
    """Version-to-version benchmark comparison report."""

    comparisons: list[VersionComparison]

    def to_dict(self) -> dict[str, Any]:
        return {"comparisons": [item.to_dict() for item in self.comparisons]}


def compare_benchmark_versions(
    version_reports: dict[str, str | Path | dict[str, Any]],
    pairs: list[tuple[str, str]] | None = None,
) -> BenchmarkVersionComparisonReport:
    """Compare benchmark report payloads across named versions.

    If pairs are omitted, adjacent versions sorted by name are compared, which supports
    standard v1 -> v2 -> v3 workflows while remaining usable for future suites.
    """

    comparison_pairs = pairs or _adjacent_pairs(version_reports)
    comparisons = [
        VersionComparison(
            baseline_version=baseline,
            candidate_version=candidate,
            comparison=compare_results(version_reports[baseline], version_reports[candidate]),
        )
        for baseline, candidate in comparison_pairs
    ]
    return BenchmarkVersionComparisonReport(comparisons=comparisons)


def write_benchmark_version_comparison(
    version_reports: dict[str, str | Path | dict[str, Any]],
    output_path: str | Path,
    pairs: list[tuple[str, str]] | None = None,
) -> BenchmarkVersionComparisonReport:
    """Write benchmark version comparison JSON to disk."""

    report = compare_benchmark_versions(version_reports, pairs)
    Path(output_path).write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    return report


def _adjacent_pairs(
    version_reports: dict[str, str | Path | dict[str, Any]],
) -> list[tuple[str, str]]:
    versions = sorted(version_reports)
    return list(zip(versions, versions[1:], strict=False))
