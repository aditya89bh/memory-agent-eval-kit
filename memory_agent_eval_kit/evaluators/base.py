"""Base evaluator implementation."""

from __future__ import annotations

from time import perf_counter

from memory_agent_eval_kit.adapters import MemoryAgentAdapter
from memory_agent_eval_kit.metrics import EvaluationResult
from memory_agent_eval_kit.models import BenchmarkScenario, Category
from memory_agent_eval_kit.scoring import exact_score, partial_score


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
                "expected_behavior": scenario.expected_behavior.to_dict(),
            },
        )

    def score_answer(self, scenario: BenchmarkScenario, answer: str) -> float:
        score = self._positive_score(scenario, answer)
        extra_expected = scenario.expected_behavior.metadata.get("also_contains")
        if extra_expected is not None:
            extra_text = str(extra_expected)
            extra_score = (
                1.0
                if all(part.casefold() in answer.casefold() for part in extra_text.split())
                else self._text_score(extra_text, answer, scenario)
            )
            score = min(score, extra_score)
        absent_ok = all(
            absent.casefold() not in answer.casefold() for absent in scenario.expected_absent
        )
        if score >= scenario.scoring_rules.threshold and absent_ok:
            return 1.0
        if scenario.scoring_rules.allow_partial and absent_ok:
            return score
        if score >= scenario.scoring_rules.threshold or absent_ok and scenario.expected_absent:
            return 0.5
        return 0.0

    def _positive_score(self, scenario: BenchmarkScenario, answer: str) -> float:
        return self._text_score(scenario.expected_answer, answer, scenario)

    def _text_score(self, expected: str, answer: str, scenario: BenchmarkScenario) -> float:
        if scenario.scoring_rules.mode in {"normalized", "partial", "semantic"}:
            return partial_score(expected, answer)
        return exact_score(expected, answer)
