"""Temporal drift evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class TemporalDriftEvaluator(ScenarioEvaluator):
    """Evaluator for evolving facts across a multi-event timeline."""

    def __init__(self) -> None:
        super().__init__("temporal_drift")
