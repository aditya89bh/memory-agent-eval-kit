"""Side-by-side benchmark comparison dashboard generation."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DashboardEntry:
    """Normalized benchmark summary for one agent/report."""

    agent_name: str
    report_path: str
    overall_score: float
    scenario_count: int
    hallucination_rate: float
    false_recall_rate: float
    latency_avg_ms: float
    latency_p95_ms: float
    category_scores: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def write_comparison_dashboard(
    reports: dict[str, Path],
    output_dir: Path = Path("reports"),
) -> list[Path]:
    """Write JSON and Markdown comparison dashboard artifacts."""

    output_dir.mkdir(parents=True, exist_ok=True)
    entries = [
        _entry_from_report(agent_name, report_path)
        for agent_name, report_path in reports.items()
    ]
    entries = sorted(entries, key=lambda entry: entry.overall_score, reverse=True)
    json_path = output_dir / "comparison_dashboard.json"
    markdown_path = output_dir / "comparison_dashboard.md"
    json_path.write_text(
        json.dumps([entry.to_dict() for entry in entries], indent=2),
        encoding="utf-8",
    )
    markdown_path.write_text(_dashboard_markdown(entries), encoding="utf-8")
    return [json_path, markdown_path]


def _entry_from_report(agent_name: str, report_path: Path) -> DashboardEntry:
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    metrics = payload.get("metrics", {})
    category_breakdown = payload.get("category_breakdown", {})
    category_scores = {
        str(category): float(values.get("score", 0.0))
        for category, values in category_breakdown.items()
        if isinstance(values, dict)
    }
    return DashboardEntry(
        agent_name=agent_name,
        report_path=str(report_path),
        overall_score=float(metrics.get("overall_score", 0.0)),
        scenario_count=int(metrics.get("total_scenarios", 0)),
        hallucination_rate=float(metrics.get("hallucination_rate", 0.0)),
        false_recall_rate=float(metrics.get("false_recall_rate", 0.0)),
        latency_avg_ms=float(metrics.get("latency_avg_ms", 0.0)),
        latency_p95_ms=float(metrics.get("latency_p95_ms", 0.0)),
        category_scores=category_scores,
    )


def _dashboard_markdown(entries: list[DashboardEntry]) -> str:
    lines = [
        "# Benchmark Comparison Dashboard",
        "",
        "| Rank | Agent | Overall | Scenarios | Hallucination Rate | "
        "False Recall Rate | Avg Latency ms | P95 Latency ms |",
        "|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for rank, entry in enumerate(entries, start=1):
        lines.append(
            f"| {rank} | {entry.agent_name} | {entry.overall_score * 100:.2f}% | "
            f"{entry.scenario_count} | {entry.hallucination_rate * 100:.2f}% | "
            f"{entry.false_recall_rate * 100:.2f}% | {entry.latency_avg_ms:.2f} | "
            f"{entry.latency_p95_ms:.2f} |"
        )
    lines.extend(["", "## Category Scores", ""])
    categories = sorted({category for entry in entries for category in entry.category_scores})
    lines.append("| Agent | " + " | ".join(categories) + " |")
    lines.append("|---|" + "---:|" * len(categories))
    for entry in entries:
        scores = [
            f"{entry.category_scores.get(category, 0.0) * 100:.0f}%"
            for category in categories
        ]
        lines.append(f"| {entry.agent_name} | " + " | ".join(scores) + " |")
    return "\n".join(lines) + "\n"
