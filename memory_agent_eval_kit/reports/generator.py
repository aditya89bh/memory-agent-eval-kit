"""Report generation for benchmark runs."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from memory_agent_eval_kit.benchmarks.runner import BenchmarkRun


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
        lines = [
            "# Memory Agent Benchmark Results",
            "",
            f"Overall Score: {_pct(metrics.overall_score)}",
            f"Average Latency: {metrics.latency_avg_ms:.2f} ms",
            f"P95 Latency: {metrics.latency_p95_ms:.2f} ms",
            "",
            "## Category Scores",
            "",
            f"- Recall: {_pct(metrics.recall_accuracy)}",
            f"- Contradiction: {_pct(metrics.contradiction_accuracy)}",
            f"- Correction: {_pct(metrics.correction_accuracy)}",
            f"- Forgetting: {_pct(metrics.forgetting_accuracy)}",
            f"- Temporal: {_pct(metrics.temporal_accuracy)}",
            f"- Stale Memory: {_pct(metrics.stale_memory_accuracy)}",
            f"- Continuity: {_pct(metrics.continuity_accuracy)}",
            "",
            "## Scenario Scores",
            "",
            "| Scenario | Category | Score | Latency ms | Success |",
            "|---|---:|---:|---:|---:|",
        ]
        for result in run.results:
            lines.append(
                f"| {result.scenario_id} | {result.category} | {result.score:.2f} | "
                f"{result.latency_ms:.2f} | {result.success} |"
            )
        (self.report_dir / "results.md").write_text(
            "\n".join(lines) + "\n",
            encoding="utf-8",
        )


def _pct(value: float) -> str:
    return f"{value * 100:.0f}%"
