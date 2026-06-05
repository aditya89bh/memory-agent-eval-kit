"""Timeline reasoning evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.temporal_drift import TemporalDriftEvaluator


class TimelineReasoningEvaluator(TemporalDriftEvaluator):
    """Evaluator for chronological state reasoning."""

    def __init__(self) -> None:
        self.category = "timeline_reasoning"
