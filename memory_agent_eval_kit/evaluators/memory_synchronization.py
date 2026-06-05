"""Memory synchronization evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class MemorySynchronizationEvaluator(ScenarioEvaluator):
    """Evaluator for memory propagation across agents."""

    def __init__(self) -> None:
        super().__init__("memory_synchronization")
