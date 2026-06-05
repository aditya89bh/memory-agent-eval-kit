"""Hierarchical memory evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class HierarchicalMemoryEvaluator(ScenarioEvaluator):
    """Evaluator for organization hierarchy retrieval."""

    def __init__(self) -> None:
        super().__init__("hierarchical_memory")
