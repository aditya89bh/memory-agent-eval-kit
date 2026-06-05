"""Agent disagreement evaluator."""

from __future__ import annotations

from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator


class AgentDisagreementEvaluator(ScenarioEvaluator):
    """Evaluator for detecting disagreement between agent observations."""

    def __init__(self) -> None:
        super().__init__("agent_disagreement")
