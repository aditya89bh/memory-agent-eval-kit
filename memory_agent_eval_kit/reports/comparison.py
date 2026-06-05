"""Benchmark comparison reporting utilities."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CategoryDelta:
    """Score delta for one benchmark category."""

    category: str
    baseline_score: float
    candidate_score: float
    delta: float
    regressed: bool


@dataclass(frozen=True)
class BenchmarkComparison:
    """Comparison between two benchmark reports."""

    baseline_score: float
    candidate_score: float
    score_delta: float
    category_deltas: list[CategoryDelta]
    regressions: list[str]

    @property
    def has_regressions(self) -> bool:
        return bool(self.regressions)

    def to_dict(self) -> dict[str, Any]:
        return {
            "baseline_score": self.baseline_score,
            "candidate_score": self.candidate_score,
            "score_delta": self.score_delta,
            "category_deltas": [asdict(delta) for delta in self.category_deltas],
            "regressions": self.regressions,
            "has_regressions": self.has_regressions,
        }


def compare_results(
    baseline: str | Path | dict[str, Any],
    candidate: str | Path | dict[str, Any],
    *,
    regression_threshold: float = -0.01,
) -> BenchmarkComparison:
    """Compare two benchmark report payloads.

    ``regression_threshold`` is a negative allowed delta. The default flags category
    drops greater than one percentage point while still reporting all deltas.
    """

    baseline_payload = _load_payload(baseline)
    candidate_payload = _load_payload(candidate)
    baseline_score = _metric(baseline_payload, "overall_score")
    candidate_score = _metric(candidate_payload, "overall_score")
    categories = sorted(set(_breakdown(baseline_payload)) | set(_breakdown(candidate_payload)))
    category_deltas: list[CategoryDelta] = []
    regressions: list[str] = []
    for category in categories:
        old_score = _category_score(baseline_payload, category)
        new_score = _category_score(candidate_payload, category)
        delta = new_score - old_score
        regressed = delta < regression_threshold
        if regressed:
            regressions.append(category)
        category_deltas.append(
            CategoryDelta(
                category=category,
                baseline_score=old_score,
                candidate_score=new_score,
                delta=delta,
                regressed=regressed,
            )
        )
    overall_delta = candidate_score - baseline_score
    if overall_delta < regression_threshold:
        regressions.insert(0, "overall")
    return BenchmarkComparison(
        baseline_score=baseline_score,
        candidate_score=candidate_score,
        score_delta=overall_delta,
        category_deltas=category_deltas,
        regressions=regressions,
    )


def _load_payload(source: str | Path | dict[str, Any]) -> dict[str, Any]:
    if isinstance(source, dict):
        return source
    payload = json.loads(Path(source).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Benchmark report must be a JSON object")
    return payload


def _metric(payload: dict[str, Any], name: str) -> float:
    metrics = payload.get("metrics", {})
    return float(metrics.get(name, 0.0))


def _breakdown(payload: dict[str, Any]) -> dict[str, Any]:
    raw = payload.get("category_breakdown", {})
    return raw if isinstance(raw, dict) else {}


def _category_score(payload: dict[str, Any], category: str) -> float:
    item = _breakdown(payload).get(category, {})
    if not isinstance(item, dict):
        return 0.0
    return float(item.get("score", 0.0))
