"""Preference evolution evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class PreferenceEvolutionEvaluator(ScenarioEvaluator):
    """Evaluator for current and previous user preference recall."""

    def __init__(self) -> None:
        super().__init__("preference_evolution")
