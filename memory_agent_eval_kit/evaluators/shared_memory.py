"""Shared memory evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class SharedMemoryEvaluator(ScenarioEvaluator):
    """Evaluator for multiple agents reading a shared memory store."""

    def __init__(self) -> None:
        super().__init__("shared_memory")
