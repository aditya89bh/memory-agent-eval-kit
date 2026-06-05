"""Adversarial contradiction evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class AdversarialContradictionEvaluator(ScenarioEvaluator):
    """Evaluator for overlapping, ambiguous, and conflicting memories."""

    def __init__(self) -> None:
        super().__init__("adversarial_contradiction")
