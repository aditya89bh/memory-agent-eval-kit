"""Confidence interval helpers for benchmark outcomes."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ConfidenceInterval:
    """Wilson score confidence interval for a bounded pass rate."""

    estimate: float
    lower: float
    upper: float
    count: int
    confidence_level: float = 0.95

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def wilson_score_interval(
    successes: int,
    count: int,
    *,
    confidence_level: float = 0.95,
) -> ConfidenceInterval:
    """Return a Wilson score interval without external statistical libraries."""

    if count <= 0:
        return ConfidenceInterval(0.0, 0.0, 0.0, 0, confidence_level)
    z = _z_value(confidence_level)
    proportion = successes / count
    denominator = 1 + z**2 / count
    centre = proportion + z**2 / (2 * count)
    margin = z * math.sqrt((proportion * (1 - proportion) + z**2 / (4 * count)) / count)
    return ConfidenceInterval(
        estimate=proportion,
        lower=max(0.0, (centre - margin) / denominator),
        upper=min(1.0, (centre + margin) / denominator),
        count=count,
        confidence_level=confidence_level,
    )


def _z_value(confidence_level: float) -> float:
    supported = {
        0.90: 1.6448536269514722,
        0.95: 1.959963984540054,
        0.99: 2.5758293035489004,
    }
    rounded = round(confidence_level, 2)
    if rounded in supported:
        return supported[rounded]
    return supported[0.95]
