"""TemporalEvaluator implementation."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class TemporalEvaluator(ScenarioEvaluator):
    """Evaluator for temporal benchmark scenarios."""

    def __init__(self) -> None:
        super().__init__("temporal")
