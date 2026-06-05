"""Retention policy evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class RetentionPolicyEvaluator(ScenarioEvaluator):
    """Evaluator for temporary, expiring, and archived memory policies."""

    def __init__(self) -> None:
        super().__init__("retention_policy")
