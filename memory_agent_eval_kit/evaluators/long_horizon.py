"""Long-horizon memory evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class LongHorizonEvaluator(ScenarioEvaluator):
    """Evaluator for recall after many prior memories."""

    def __init__(self) -> None:
        super().__init__("long_horizon")
