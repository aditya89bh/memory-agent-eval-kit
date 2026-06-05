"""StaleMemoryEvaluator implementation."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class StaleMemoryEvaluator(ScenarioEvaluator):
    """Evaluator for stale_memory benchmark scenarios."""

    def __init__(self) -> None:
        super().__init__("stale_memory")
