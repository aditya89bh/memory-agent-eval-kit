"""RecallEvaluator implementation."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class RecallEvaluator(ScenarioEvaluator):
    """Evaluator for recall benchmark scenarios."""

    def __init__(self) -> None:
        super().__init__("recall")
