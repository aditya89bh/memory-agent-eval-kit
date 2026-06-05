"""Evaluation result and aggregate metric models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from statistics import mean
from typing import Any

from memory_agent_eval_kit.models import Category


@dataclass(frozen=True)
class EvaluationResult:
    scenario_id: str
    category: Category
    success: bool
    score: float
    latency_ms: float
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AggregateMetrics:
    overall_score: float
    recall_accuracy: float
    contradiction_accuracy: float
    correction_accuracy: float
    forgetting_accuracy: float
    temporal_accuracy: float
    stale_memory_accuracy: float
    continuity_accuracy: float
    latency_avg_ms: float
    latency_p95_ms: float
    total_scenarios: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _score_for(results: list[EvaluationResult], category: Category) -> float:
    category_results = [result.score for result in results if result.category == category]
    return mean(category_results) if category_results else 0.0


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(0.95 * (len(ordered) - 1)))
    return ordered[index]


def aggregate_results(results: list[EvaluationResult]) -> AggregateMetrics:
    scores = [result.score for result in results]
    latencies = [result.latency_ms for result in results]
    return AggregateMetrics(
        overall_score=mean(scores) if scores else 0.0,
        recall_accuracy=_score_for(results, "recall"),
        contradiction_accuracy=_score_for(results, "contradiction"),
        correction_accuracy=_score_for(results, "correction"),
        forgetting_accuracy=_score_for(results, "forgetting"),
        temporal_accuracy=_score_for(results, "temporal"),
        stale_memory_accuracy=_score_for(results, "stale_memory"),
        continuity_accuracy=_score_for(results, "continuity"),
        latency_avg_ms=mean(latencies) if latencies else 0.0,
        latency_p95_ms=_p95(latencies),
        total_scenarios=len(results),
    )
