"""Base evaluator implementation."""

from __future__ import annotations

from time import perf_counter

from memory_agent_eval_kit.adapters import MemoryAgentAdapter
from memory_agent_eval_kit.metrics import EvaluationResult
from memory_agent_eval_kit.models import BenchmarkScenario, Category


class ScenarioEvaluator:
    """Executes one scenario against an adapter and scores the answer."""

    category: Category

    def __init__(self, category: Category) -> None:
        self.category = category

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
        start = perf_counter()
        answer = adapter.query(scenario.query)
        latency_ms = (perf_counter() - start) * 1000
        for memory_id in touched_ids:
            adapter.delete_memory(memory_id)
        score = self.score_answer(scenario, answer)
        return EvaluationResult(
            scenario_id=scenario.scenario_id,
            category=scenario.category,
            success=score >= 1.0,
            score=score,
            latency_ms=latency_ms,
            details={
                "query": scenario.query,
                "expected_answer": scenario.expected_answer,
                "expected_absent": scenario.expected_absent,
                "actual_answer": answer,
            },
        )

    def score_answer(self, scenario: BenchmarkScenario, answer: str) -> float:
        normalized = answer.casefold()
        expected_ok = scenario.expected_answer.casefold() in normalized
        absent_ok = all(absent.casefold() not in normalized for absent in scenario.expected_absent)
        if expected_ok and absent_ok:
            return 1.0
        if expected_ok or absent_ok and scenario.expected_absent:
            return 0.5
        return 0.0
