"""Collaborative memory evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class CollaborativeMemoryEvaluator(ScenarioEvaluator):
    """Evaluator for memories contributed by multiple agents."""

    def __init__(self) -> None:
        super().__init__("collaborative_memory")
