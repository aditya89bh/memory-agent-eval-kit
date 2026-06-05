"""Report generation for benchmark runs."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from memory_agent_eval_kit.benchmarks.runner import BenchmarkRun
    from memory_agent_eval_kit.metrics import EvaluationResult


class ReportGenerator:
    """Writes JSON, CSV, and Markdown reports."""

    def __init__(self, report_dir: Path) -> None:
        self.report_dir = report_dir

    def write(self, run: BenchmarkRun) -> None:
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.write_json(run)
        self.write_csv(run)
        self.write_markdown(run)

    def write_json(self, run: BenchmarkRun) -> None:
        payload = {
            "metrics": run.metrics.to_dict(),
            "category_breakdown": _category_breakdown(run.results),
            "weakest_categories": _ranked_categories(run.results, reverse=False)[:3],
            "strongest_categories": _ranked_categories(run.results, reverse=True)[:3],
            "results": [result.to_dict() for result in run.results],
        }
        (self.report_dir / "results.json").write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8",
        )

    def write_csv(self, run: BenchmarkRun) -> None:
        with (self.report_dir / "results.csv").open(
            "w",
            newline="",
            encoding="utf-8",
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "scenario_id",
                    "category",
                    "success",
                    "score",
                    "latency_ms",
                    "actual_answer",
                    "expected_answer",
                ],
            )
            writer.writeheader()
            for result in run.results:
                writer.writerow(
                    {
                        "scenario_id": result.scenario_id,
                        "category": result.category,
                        "success": result.success,
                        "score": f"{result.score:.3f}",
                        "latency_ms": f"{result.latency_ms:.3f}",
                        "actual_answer": result.details.get("actual_answer", ""),
                        "expected_answer": result.details.get("expected_answer", ""),
                    }
                )

    def write_markdown(self, run: BenchmarkRun) -> None:
        metrics = run.metrics
        breakdown = _category_breakdown(run.results)
        lines = [
            "# Memory Agent Benchmark Results",
            "",
            "## Summary",
            "",
            f"- Overall Score: {_pct(metrics.overall_score)}",
            f"- Total Scenarios: {metrics.total_scenarios}",
            f"- Average Latency: {metrics.latency_avg_ms:.2f} ms",
            f"- P95 Latency: {metrics.latency_p95_ms:.2f} ms",
            "",
            "## Category Breakdown",
            "",
            "| Category | Pass | Fail | Score | Avg Latency ms |",
            "|---|---:|---:|---:|---:|",
        ]
        for category, item in sorted(breakdown.items()):
            lines.append(
                f"| {category} | {item['pass']} | {item['fail']} | "
                f"{item['score'] * 100:.0f}% | {item['latency_avg_ms']:.2f} |"
            )
        lines.extend(
            [
                "",
                "## Strongest Categories",
                "",
                *[
                    f"- {item['category']}: {item['score'] * 100:.0f}%"
                    for item in _ranked_categories(run.results, True)[:3]
                ],
                "",
                "## Weakest Categories",
                "",
                *[
                    f"- {item['category']}: {item['score'] * 100:.0f}%"
                    for item in _ranked_categories(run.results, False)[:3]
                ],
                "",
                "## Pass/Fail Table",
                "",
                "| Scenario | Category | Result | Score | Latency ms |",
                "|---|---|---:|---:|---:|",
            ]
        )
        for result in run.results:
            outcome = "PASS" if result.success else "FAIL"
            lines.append(
                f"| {result.scenario_id} | {result.category} | {outcome} | "
                f"{result.score:.2f} | {result.latency_ms:.2f} |"
            )
        (self.report_dir / "results.md").write_text(
            "\n".join(lines) + "\n",
            encoding="utf-8",
        )


def _category_breakdown(results: list[EvaluationResult]) -> dict[str, dict[str, float | int]]:
    grouped: dict[str, list[EvaluationResult]] = defaultdict(list)
    for result in results:
        grouped[result.category].append(result)
    breakdown: dict[str, dict[str, float | int]] = {}
    for category, category_results in grouped.items():
        count = len(category_results)
        passed = sum(1 for result in category_results if result.success)
        breakdown[category] = {
            "pass": passed,
            "fail": count - passed,
            "score": sum(result.score for result in category_results) / count,
            "latency_avg_ms": sum(result.latency_ms for result in category_results) / count,
        }
    return breakdown


def _ranked_categories(
    results: list[EvaluationResult], reverse: bool
) -> list[dict[str, float | str]]:
    breakdown = _category_breakdown(results)
    ranked: list[dict[str, float | str]] = [
        {"category": category, "score": float(item["score"])}
        for category, item in breakdown.items()
    ]
    return sorted(ranked, key=lambda item: float(item["score"]), reverse=reverse)


def _pct(value: float) -> str:
    return f"{value * 100:.0f}%"
