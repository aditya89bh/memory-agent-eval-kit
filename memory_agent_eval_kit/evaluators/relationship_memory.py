"""Relationship memory evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class RelationshipMemoryEvaluator(ScenarioEvaluator):
    """Evaluator for person relationship and role recall."""

    def __init__(self) -> None:
        super().__init__("relationship_memory")
