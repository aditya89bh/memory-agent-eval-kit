"""Memory leakage evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.forgetting import ForgettingEvaluator


class MemoryLeakageEvaluator(ForgettingEvaluator):
    """Forgetting-style evaluator dedicated to deleted-information leakage."""

    def __init__(self) -> None:
        self.category = "memory_leakage"
