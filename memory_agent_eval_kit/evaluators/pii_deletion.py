"""PII deletion evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class PIIDeletionEvaluator(ScenarioEvaluator):
    """Evaluator for verifying deleted PII cannot be recalled."""

    def __init__(self) -> None:
        super().__init__("pii_deletion")
