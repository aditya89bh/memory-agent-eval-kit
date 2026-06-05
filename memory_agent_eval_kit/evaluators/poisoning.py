"""Memory poisoning evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class PoisoningEvaluator(ScenarioEvaluator):
    """Evaluator for malicious or low-trust memory injections."""

    def __init__(self) -> None:
        super().__init__("memory_poisoning")
