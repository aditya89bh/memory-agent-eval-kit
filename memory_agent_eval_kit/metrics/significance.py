"""Statistical significance helpers for benchmark score comparisons."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from statistics import NormalDist
from typing import Protocol


class ScoredResult(Protocol):
    score: float


@dataclass(frozen=True)
class SignificanceResult:
    """Approximate two-sided score-difference significance result."""

    baseline_mean: float
    candidate_mean: float
    score_delta: float
    z_score: float
    p_value: float
    significant: bool
    alpha: float

    def to_dict(self) -> dict[str, float | bool]:
        return asdict(self)


def score_difference_significance(
    baseline: list[ScoredResult],
    candidate: list[ScoredResult],
    *,
    alpha: float = 0.05,
) -> SignificanceResult:
    """Estimate whether two benchmark result sets differ meaningfully.

    Uses a normal approximation over bounded scenario scores. This is intended
    as a lightweight signal for benchmark comparisons, not as a replacement for
    domain-specific statistical review.
    """

    baseline_scores = [result.score for result in baseline]
    candidate_scores = [result.score for result in candidate]
    baseline_mean = _mean(baseline_scores)
    candidate_mean = _mean(candidate_scores)
    delta = candidate_mean - baseline_mean
    standard_error = math.sqrt(
        _sample_variance(baseline_scores) / max(1, len(baseline_scores))
        + _sample_variance(candidate_scores) / max(1, len(candidate_scores))
    )
    z_score = 0.0 if standard_error == 0.0 else delta / standard_error
    p_value = 1.0 if standard_error == 0.0 else 2 * (1 - NormalDist().cdf(abs(z_score)))
    return SignificanceResult(
        baseline_mean=baseline_mean,
        candidate_mean=candidate_mean,
        score_delta=delta,
        z_score=z_score,
        p_value=p_value,
        significant=p_value < alpha,
        alpha=alpha,
    )


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _sample_variance(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    avg = _mean(values)
    return sum((value - avg) ** 2 for value in values) / (len(values) - 1)
