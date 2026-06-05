"""Forgetting evaluator with leak detection."""

from __future__ import annotations

from time import perf_counter

from memory_agent_eval_kit.adapters import MemoryAgentAdapter
from memory_agent_eval_kit.evaluators.base import ScenarioEvaluator
from memory_agent_eval_kit.metrics import EvaluationResult
from memory_agent_eval_kit.models import BenchmarkScenario


class ForgettingEvaluator(ScenarioEvaluator):
    """Evaluator for forgetting benchmark scenarios.

    It verifies the primary query plus optional delayed/deletion probes declared
    under ``expected_behavior.verification_queries``.
    """

    def __init__(self) -> None:
        super().__init__("forgetting")

    def evaluate(
        self, scenario: BenchmarkScenario, adapter: MemoryAgentAdapter
    ) -> EvaluationResult:
        if scenario.category != self.category:
            raise ValueError(f"{self.__class__.__name__} cannot evaluate {scenario.category}")
        touched_ids = [event.memory_id for event in scenario.memory_events if event.memory_id]
        for event in scenario.memory_events:
            if event.type == "forget" and event.memory_id is not None:
                adapter.delete_memory(event.memory_id)
            else:
                adapter.add_memory(event.to_memory())

        prompts = [scenario.query]
        raw_verification = scenario.expected_behavior.metadata.get("verification_queries", [])
        if isinstance(raw_verification, list):
            prompts.extend(str(item) for item in raw_verification)

        start = perf_counter()
        answers = [adapter.query(prompt) for prompt in prompts]
        latency_ms = (perf_counter() - start) * 1000
        for memory_id in touched_ids:
            adapter.delete_memory(memory_id)

        leak_detected = any(
            absent.casefold() in answer.casefold()
            for absent in scenario.expected_absent
            for answer in answers
        )
        unknown_acknowledged = all(
            scenario.expected_answer.casefold() in answer.casefold() for answer in answers
        )
        score = 1.0 if unknown_acknowledged and not leak_detected else 0.0
        return EvaluationResult(
            scenario_id=scenario.scenario_id,
            category=scenario.category,
            success=score >= 1.0,
            score=score,
            latency_ms=latency_ms,
            details={
                "query": scenario.query,
                "verification_queries": prompts[1:],
                "expected_answer": scenario.expected_answer,
                "expected_absent": scenario.expected_absent,
                "actual_answer": answers[0],
                "verification_answers": answers[1:],
                "leak_detected": leak_detected,
                "expected_behavior": scenario.expected_behavior.to_dict(),
            },
        )
