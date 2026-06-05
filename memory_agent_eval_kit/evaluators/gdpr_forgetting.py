"""GDPR forgetting evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class GDPRForgettingEvaluator(ScenarioEvaluator):
    """Evaluator for right-to-be-forgotten compliance scenarios."""

    def __init__(self) -> None:
        super().__init__("gdpr_forgetting")
