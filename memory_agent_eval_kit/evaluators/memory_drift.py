"""Memory drift evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.temporal_drift import TemporalDriftEvaluator


class MemoryDriftEvaluator(TemporalDriftEvaluator):
    """Evaluator for evolving user facts and updates."""

    def __init__(self) -> None:
        self.category = "memory_drift"
