"""Report generation for benchmark runs."""

from __future__ import annotations

import csv
import json
import math
import platform
import tomllib
from collections import defaultdict
from datetime import UTC, datetime
from importlib import metadata
from pathlib import Path
from typing import TYPE_CHECKING, Any

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
        self.write_reproducibility(run)

    def write_json(self, run: BenchmarkRun) -> None:
        payload = {
            "metrics": run.metrics.to_dict(),
            "category_breakdown": _category_breakdown(run.results),
            "difficulty_breakdown": _difficulty_breakdown(run.results),
            "confidence_metrics": _confidence_metrics(run.results),
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
                lineterminator="\n",
                fieldnames=[
                    "scenario_id",
                    "category",
                    "difficulty",
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
                        "difficulty": result.details.get("difficulty", "medium"),
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
        difficulty = _difficulty_breakdown(run.results)
        confidence = _confidence_metrics(run.results)
        lines = [
            "# Memory Agent Benchmark Results",
            "",
            "## Summary",
            "",
            f"- Overall Score: {_pct(metrics.overall_score)}",
            f"- Total Scenarios: {metrics.total_scenarios}",
            f"- Average Latency: {metrics.latency_avg_ms:.2f} ms",
            f"- P95 Latency: {metrics.latency_p95_ms:.2f} ms",
            f"- Compliance Score: {_pct(metrics.compliance_score)}",
            f"- Deletion Score: {_pct(metrics.deletion_score)}",
            f"- Retention Score: {_pct(metrics.retention_score)}",
            f"- Privacy Score: {_pct(metrics.privacy_score)}",
            "",
            "## Confidence Metrics",
            "",
            f"- Overall 95% CI: {_pct(float(confidence['overall']['lower']))} to "
            f"{_pct(float(confidence['overall']['upper']))}",
            f"- Overall estimate: {_pct(float(confidence['overall']['estimate']))}",
            "- Method: Wilson score interval over scenario pass/fail outcomes.",
            "",
            "## Category Breakdown",
            "",
            "| Category | Pass | Fail | Score | 95% CI | Avg Latency ms |",
            "|---|---:|---:|---:|---:|---:|",
        ]
        category_confidence = confidence["categories"]
        for category, item in sorted(breakdown.items()):
            interval = category_confidence[str(category)]
            lines.append(
                f"| {category} | {item['pass']} | {item['fail']} | "
                f"{item['score'] * 100:.0f}% | {_pct(float(interval['lower']))}-"
                f"{_pct(float(interval['upper']))} | {item['latency_avg_ms']:.2f} |"
            )
        lines.extend(
            [
                "",
                "## Difficulty Breakdown",
                "",
                "| Difficulty | Pass | Fail | Score | Avg Latency ms |",
                "|---|---:|---:|---:|---:|",
            ]
        )
        default_difficulty = {"pass": 0, "fail": 0, "score": 0.0, "latency_avg_ms": 0.0}
        for level in ("easy", "medium", "hard"):
            item = difficulty.get(level, default_difficulty)
            lines.append(
                f"| {level} | {item['pass']} | {item['fail']} | "
                f"{float(item['score']) * 100:.0f}% | {float(item['latency_avg_ms']):.2f} |"
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
                "| Scenario | Category | Difficulty | Result | Score | Latency ms |",
                "|---|---|---|---:|---:|---:|",
            ]
        )
        for result in run.results:
            outcome = "PASS" if result.success else "FAIL"
            lines.append(
                f"| {result.scenario_id} | {result.category} | "
                f"{result.details.get('difficulty', 'medium')} | {outcome} | "
                f"{result.score:.2f} | {result.latency_ms:.2f} |"
            )
        (self.report_dir / "results.md").write_text(
            "\n".join(lines) + "\n",
            encoding="utf-8",
        )

    def write_reproducibility(self, run: BenchmarkRun) -> None:
        seed = getattr(run, "seed", None)
        lines = [
            "# Reproducibility Report",
            "",
            f"- Benchmark version: {_package_version()}",
            f"- Seed: {seed if seed is not None else 'not set'}",
            f"- Scenario count: {run.metrics.total_scenarios}",
            f"- Timestamp: {datetime.now(UTC).isoformat()}",
            f"- Python: {platform.python_version()}",
            f"- Platform: {platform.platform()}",
            f"- Implementation: {platform.python_implementation()}",
            "",
            "Use this file with `results.json`, `results.csv`, and `results.md` to reproduce "
            "the benchmark context for a specific run.",
        ]
        (self.report_dir / "reproducibility.md").write_text(
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


def _package_version() -> str:
    pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"
    if pyproject_path.exists():
        payload = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
        version = payload.get("project", {}).get("version")
        if isinstance(version, str):
            return version
    try:
        return metadata.version("memory-agent-eval-kit")
    except metadata.PackageNotFoundError:
        return "unknown"


def _confidence_metrics(results: list[EvaluationResult]) -> dict[str, Any]:
    overall_successes = sum(1 for result in results if result.success)
    overall = _confidence_interval(overall_successes, len(results))
    grouped: dict[str, list[EvaluationResult]] = defaultdict(list)
    for result in results:
        grouped[result.category].append(result)
    categories = {
        category: _confidence_interval(
            sum(1 for result in category_results if result.success),
            len(category_results),
        )
        for category, category_results in grouped.items()
    }
    return {"overall": overall, "categories": categories}


def _confidence_interval(successes: int, count: int) -> dict[str, float | int]:
    if count == 0:
        return {"estimate": 0.0, "lower": 0.0, "upper": 0.0, "count": 0}
    z = 1.96
    proportion = successes / count
    denominator = 1 + z**2 / count
    centre = proportion + z**2 / (2 * count)
    margin = z * math.sqrt((proportion * (1 - proportion) + z**2 / (4 * count)) / count)
    return {
        "estimate": proportion,
        "lower": max(0.0, (centre - margin) / denominator),
        "upper": min(1.0, (centre + margin) / denominator),
        "count": count,
    }


def _difficulty_breakdown(results: list[EvaluationResult]) -> dict[str, dict[str, float | int]]:
    grouped: dict[str, list[EvaluationResult]] = defaultdict(list)
    for result in results:
        grouped[str(result.details.get("difficulty", "medium"))].append(result)
    breakdown: dict[str, dict[str, float | int]] = {}
    for difficulty, difficulty_results in grouped.items():
        count = len(difficulty_results)
        passed = sum(1 for result in difficulty_results if result.success)
        breakdown[difficulty] = {
            "pass": passed,
            "fail": count - passed,
            "score": sum(result.score for result in difficulty_results) / count,
            "latency_avg_ms": sum(result.latency_ms for result in difficulty_results) / count,
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
