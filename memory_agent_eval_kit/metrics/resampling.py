"""Bootstrap resampling analysis for benchmark stability."""

from __future__ import annotations

import random
from dataclasses import asdict, dataclass
from typing import Protocol


class ScoredResult(Protocol):
    score: float


@dataclass(frozen=True)
class BootstrapAnalysis:
    """Bootstrap summary for benchmark score stability."""

    iterations: int
    seed: int
    sample_size: int
    mean_score: float
    lower: float
    upper: float
    min_score: float
    max_score: float

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def bootstrap_score_interval(
    results: list[ScoredResult],
    *,
    iterations: int = 1000,
    seed: int = 42,
    confidence_level: float = 0.95,
) -> BootstrapAnalysis:
    """Estimate benchmark score stability by sampling results with replacement."""

    if iterations <= 0:
        raise ValueError("iterations must be positive")
    if not results:
        return BootstrapAnalysis(iterations, seed, 0, 0.0, 0.0, 0.0, 0.0, 0.0)
    rng = random.Random(seed)
    scores = [result.score for result in results]
    sample_size = len(scores)
    sampled_means = []
    for _ in range(iterations):
        sample = [scores[rng.randrange(sample_size)] for _ in range(sample_size)]
        sampled_means.append(sum(sample) / sample_size)
    sampled_means.sort()
    alpha = 1.0 - confidence_level
    lower_index = max(0, int((alpha / 2) * iterations))
    upper_index = min(iterations - 1, int((1 - alpha / 2) * iterations) - 1)
    return BootstrapAnalysis(
        iterations=iterations,
        seed=seed,
        sample_size=sample_size,
        mean_score=sum(sampled_means) / iterations,
        lower=sampled_means[lower_index],
        upper=sampled_means[upper_index],
        min_score=sampled_means[0],
        max_score=sampled_means[-1],
    )
