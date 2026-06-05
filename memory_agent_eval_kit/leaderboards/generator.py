"""Generate leaderboard artifacts from benchmark reports."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class LeaderboardEntry:
    agent_name: str
    suite_name: str
    overall_score: float
    category_scores: dict[str, float]
    latency: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class LeaderboardGenerator:
    """Create JSON and Markdown leaderboard files."""

    def __init__(self, output_dir: Path = Path("leaderboards")) -> None:
        self.output_dir = output_dir

    def from_report(
        self,
        report_path: Path,
        agent_name: str = "SimpleMemoryAgent",
        suite_name: str = "default",
    ) -> LeaderboardEntry:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        metrics = payload["metrics"]
        category_scores = {
            key.removesuffix("_accuracy"): float(value)
            for key, value in metrics.items()
            if key.endswith("_accuracy")
        }
        category_scores["contradiction_resolution"] = float(
            metrics.get("contradiction_resolution", 0.0)
        )
        category_scores["poisoning_resistance"] = float(metrics.get("poisoning_resistance", 0.0))
        latency = {
            "avg_ms": float(metrics.get("latency_avg_ms", 0.0)),
            "p95_ms": float(metrics.get("latency_p95_ms", 0.0)),
        }
        return LeaderboardEntry(
            agent_name=agent_name,
            suite_name=suite_name,
            overall_score=float(metrics["overall_score"]),
            category_scores=category_scores,
            latency=latency,
        )

    def write(self, entries: list[LeaderboardEntry]) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        ordered = sorted(entries, key=lambda entry: entry.overall_score, reverse=True)
        (self.output_dir / "results.json").write_text(
            json.dumps([entry.to_dict() for entry in ordered], indent=2),
            encoding="utf-8",
        )
        lines = [
            "# Memory Agent Leaderboard",
            "",
            "| Rank | Agent | Suite | Overall | Avg Latency ms | P95 Latency ms |",
            "|---:|---|---|---:|---:|---:|",
        ]
        for rank, entry in enumerate(ordered, start=1):
            lines.append(
                f"| {rank} | {entry.agent_name} | {entry.suite_name} | "
                f"{entry.overall_score * 100:.0f}% | {entry.latency['avg_ms']:.2f} | "
                f"{entry.latency['p95_ms']:.2f} |"
            )
        (self.output_dir / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
