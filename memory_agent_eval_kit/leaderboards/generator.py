"""Generate leaderboard artifacts from benchmark reports."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class LeaderboardEntry:
    agent_name: str
    suite_name: str
    overall_score: float
    category_scores: dict[str, float]
    latency: dict[str, float]
    hallucination_rate: float = 0.0
    false_recall_rate: float = 0.0
    overall_rank: int = 0
    category_rank: int = 0
    latency_rank: int = 0
    hallucination_rank: int = 0

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
        for key in ("compliance_score", "deletion_score", "retention_score", "privacy_score"):
            category_scores[key] = float(metrics.get(key, 0.0))
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
            hallucination_rate=float(metrics.get("hallucination_rate", 0.0)),
            false_recall_rate=float(metrics.get("false_recall_rate", 0.0)),
        )

    def write(self, entries: list[LeaderboardEntry]) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        ordered = rank_entries(entries)
        (self.output_dir / "results.json").write_text(
            json.dumps([entry.to_dict() for entry in ordered], indent=2),
            encoding="utf-8",
        )
        lines = [
            "# Memory Agent Leaderboard",
            "",
            "| Overall Rank | Category Rank | Latency Rank | Hallucination Rank | Agent | "
            "Suite | Overall | Hallucination Rate | False Recall Rate | Avg Latency ms | "
            "P95 Latency ms |",
            "|---:|---:|---:|---:|---|---|---:|---:|---:|---:|---:|",
        ]
        for entry in ordered:
            lines.append(
                f"| {entry.overall_rank} | {entry.category_rank} | {entry.latency_rank} | "
                f"{entry.hallucination_rank} | {entry.agent_name} | {entry.suite_name} | "
                f"{entry.overall_score * 100:.0f}% | "
                f"{entry.hallucination_rate * 100:.0f}% | "
                f"{entry.false_recall_rate * 100:.0f}% | {entry.latency['avg_ms']:.2f} | "
                f"{entry.latency['p95_ms']:.2f} |"
            )
        (self.output_dir / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def rank_entries(entries: list[LeaderboardEntry]) -> list[LeaderboardEntry]:
    """Return entries with overall, category, and latency ranks assigned."""

    overall_ranks = _rank_map(entries, key=lambda entry: entry.overall_score, reverse=True)
    category_ranks = _rank_map(entries, key=_category_mean, reverse=True)
    latency_ranks = _rank_map(
        entries, key=lambda entry: entry.latency.get("avg_ms", 0.0), reverse=False
    )
    hallucination_ranks = _rank_map(entries, key=_hallucination_sort_score, reverse=False)
    ranked = [
        replace(
            entry,
            overall_rank=overall_ranks[id(entry)],
            category_rank=category_ranks[id(entry)],
            latency_rank=latency_ranks[id(entry)],
            hallucination_rank=hallucination_ranks[id(entry)],
        )
        for entry in entries
    ]
    return sorted(ranked, key=lambda entry: (entry.overall_rank, entry.hallucination_rank))


def _hallucination_sort_score(entry: LeaderboardEntry) -> float:
    return entry.hallucination_rate + entry.false_recall_rate


def _category_mean(entry: LeaderboardEntry) -> float:
    if not entry.category_scores:
        return 0.0
    return sum(entry.category_scores.values()) / len(entry.category_scores)


def _rank_map(entries: list[LeaderboardEntry], *, key: Any, reverse: bool) -> dict[int, int]:
    ordered = sorted(entries, key=key, reverse=reverse)
    ranks: dict[int, int] = {}
    previous_value: object | None = None
    previous_rank = 0
    for index, entry in enumerate(ordered, start=1):
        value = key(entry)
        rank = previous_rank if value == previous_value else index
        ranks[id(entry)] = rank
        previous_value = value
        previous_rank = rank
    return ranks
