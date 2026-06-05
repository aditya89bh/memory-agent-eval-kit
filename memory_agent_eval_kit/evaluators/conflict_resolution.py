"""Conflict resolution evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class ConflictResolutionEvaluator(ScenarioEvaluator):
    """Evaluator for resolving conflicting memory facts."""

    def __init__(self) -> None:
        super().__init__("conflict_resolution")
