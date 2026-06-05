"""ContradictionEvaluator implementation."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class ContradictionEvaluator(ScenarioEvaluator):
    """Evaluator for contradiction benchmark scenarios."""

    def __init__(self) -> None:
        super().__init__("contradiction")
