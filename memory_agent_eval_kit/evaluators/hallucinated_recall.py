"""Hallucinated recall evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.hallucination import HallucinationEvaluator


class HallucinatedRecallEvaluator(HallucinationEvaluator):
    """Evaluator for no-support recall prompts where invention is failure."""

    def __init__(self) -> None:
        self.category = "hallucinated_recall"
