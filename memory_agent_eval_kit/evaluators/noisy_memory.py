"""Noisy memory evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class NoisyMemoryEvaluator(ScenarioEvaluator):
    """Evaluator for retrieval robustness with distractor memories."""

    def __init__(self) -> None:
        super().__init__("noisy_memory")
