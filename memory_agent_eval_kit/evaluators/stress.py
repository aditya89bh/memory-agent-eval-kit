"""Memory stress evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class StressEvaluator(ScenarioEvaluator):
    """Evaluator for synthetic memory-scale stress scenarios."""

    def __init__(self) -> None:
        super().__init__("stress")
