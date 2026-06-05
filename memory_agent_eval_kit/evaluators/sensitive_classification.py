"""Sensitive memory classification evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class SensitiveClassificationEvaluator(ScenarioEvaluator):
    """Evaluator for personal, sensitive, and public memory labels."""

    def __init__(self) -> None:
        super().__init__("sensitive_classification")
