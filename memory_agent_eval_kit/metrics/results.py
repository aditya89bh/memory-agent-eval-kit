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
    hallucination_accuracy: float
    hallucination_rate: float
    false_recall_rate: float
    stress_recall_accuracy: float
    temporal_drift_accuracy: float
    contradiction_resolution: float
    ambiguity_handling: float
    poisoning_resistance: float
    memory_leak_rate: float
    leak_rate: float
    delayed_leak_rate: float
    hallucinated_recall_accuracy: float
    timeline_reasoning_accuracy: float
    drift_accuracy: float
    update_accuracy: float
    long_horizon_recall_accuracy: float
    long_horizon_latency_ms: float
    retrieval_precision: float
    retrieval_robustness: float
    preference_update_accuracy: float
    relationship_recall_accuracy: float
    role_recall_accuracy: float
    hierarchical_retrieval_accuracy: float
    pii_deletion_success: float
    gdpr_compliance_score: float
    retention_compliance: float
    latency_degradation_ms: float
    latency_avg_ms: float
    latency_p95_ms: float
    total_scenarios: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _score_for(results: list[EvaluationResult], category: Category) -> float:
    category_results = [result.score for result in results if result.category == category]
    return mean(category_results) if category_results else 0.0


def _latency_for(results: list[EvaluationResult], category: Category) -> float:
    latencies = [result.latency_ms for result in results if result.category == category]
    return mean(latencies) if latencies else 0.0


def _failure_rate_for(results: list[EvaluationResult], category: Category) -> float:
    category_results = [result for result in results if result.category == category]
    if not category_results:
        return 0.0
    return 1.0 - mean(result.score for result in category_results)


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(0.95 * (len(ordered) - 1)))
    return ordered[index]


def aggregate_results(results: list[EvaluationResult]) -> AggregateMetrics:
    scores = [result.score for result in results]
    latencies = [result.latency_ms for result in results]
    hallucination_rate = _failure_rate_for(results, "hallucination")
    stress_results = [result for result in results if result.category == "stress"]
    stress_latencies = [result.latency_ms for result in stress_results]
    latency_degradation_ms = (
        (max(stress_latencies) - min(stress_latencies)) if stress_latencies else 0.0
    )
    ambiguous_results = [
        result
        for result in results
        if result.category == "adversarial_contradiction"
        and result.details.get("expected_behavior", {}).get("ambiguity") is True
    ]
    ambiguity_handling = (
        mean([result.score for result in ambiguous_results]) if ambiguous_results else 0.0
    )
    return AggregateMetrics(
        overall_score=mean(scores) if scores else 0.0,
        recall_accuracy=_score_for(results, "recall"),
        contradiction_accuracy=_score_for(results, "contradiction"),
        correction_accuracy=_score_for(results, "correction"),
        forgetting_accuracy=_score_for(results, "forgetting"),
        temporal_accuracy=_score_for(results, "temporal"),
        stale_memory_accuracy=_score_for(results, "stale_memory"),
        continuity_accuracy=_score_for(results, "continuity"),
        hallucination_accuracy=_score_for(results, "hallucination"),
        hallucination_rate=hallucination_rate,
        false_recall_rate=hallucination_rate,
        stress_recall_accuracy=_score_for(results, "stress"),
        temporal_drift_accuracy=_score_for(results, "temporal_drift"),
        contradiction_resolution=_score_for(results, "adversarial_contradiction"),
        ambiguity_handling=ambiguity_handling,
        poisoning_resistance=_score_for(results, "memory_poisoning"),
        memory_leak_rate=_failure_rate_for(results, "forgetting"),
        leak_rate=_failure_rate_for(results, "memory_leakage"),
        delayed_leak_rate=_failure_rate_for(results, "memory_leakage"),
        hallucinated_recall_accuracy=_score_for(results, "hallucinated_recall"),
        timeline_reasoning_accuracy=_score_for(results, "timeline_reasoning"),
        drift_accuracy=_score_for(results, "memory_drift"),
        update_accuracy=_score_for(results, "memory_drift"),
        long_horizon_recall_accuracy=_score_for(results, "long_horizon"),
        long_horizon_latency_ms=_latency_for(results, "long_horizon"),
        retrieval_precision=_score_for(results, "noisy_memory"),
        retrieval_robustness=_score_for(results, "noisy_memory"),
        preference_update_accuracy=_score_for(results, "preference_evolution"),
        relationship_recall_accuracy=_score_for(results, "relationship_memory"),
        role_recall_accuracy=_score_for(results, "relationship_memory"),
        hierarchical_retrieval_accuracy=_score_for(results, "hierarchical_memory"),
        pii_deletion_success=_score_for(results, "pii_deletion"),
        gdpr_compliance_score=_score_for(results, "gdpr_forgetting"),
        retention_compliance=_score_for(results, "retention_policy"),
        latency_degradation_ms=latency_degradation_ms,
        latency_avg_ms=mean(latencies) if latencies else 0.0,
        latency_p95_ms=_p95(latencies),
        total_scenarios=len(results),
    )
