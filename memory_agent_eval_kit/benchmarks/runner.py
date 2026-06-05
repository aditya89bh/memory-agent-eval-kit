"""Benchmark runner orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from memory_agent_eval_kit.adapters import MemoryAgentAdapter
from memory_agent_eval_kit.benchmarks.config import BenchmarkSuiteConfig
from memory_agent_eval_kit.benchmarks.stress import generate_stress_scenarios
from memory_agent_eval_kit.datasets import load_scenarios
from memory_agent_eval_kit.evaluators import (
    AdversarialContradictionEvaluator,
    ContinuityEvaluator,
    ContradictionEvaluator,
    CorrectionEvaluator,
    ForgettingEvaluator,
    HallucinationEvaluator,
    PoisoningEvaluator,
    RecallEvaluator,
    ScenarioEvaluator,
    StaleMemoryEvaluator,
    StressEvaluator,
    TemporalDriftEvaluator,
    TemporalEvaluator,
)
from memory_agent_eval_kit.metrics import AggregateMetrics, EvaluationResult, aggregate_results
from memory_agent_eval_kit.models import Category
from memory_agent_eval_kit.reports.generator import ReportGenerator


@dataclass(frozen=True)
class BenchmarkRun:
    results: list[EvaluationResult]
    metrics: AggregateMetrics


class BenchmarkRunner:
    """Loads scenarios, runs evaluators, aggregates metrics, and writes reports."""

    def __init__(self, adapter: MemoryAgentAdapter, dataset_path: Path | str | None = None) -> None:
        self.adapter = adapter
        self.dataset_path = dataset_path
        self.evaluators: dict[Category, ScenarioEvaluator] = {
            "recall": RecallEvaluator(),
            "contradiction": ContradictionEvaluator(),
            "correction": CorrectionEvaluator(),
            "forgetting": ForgettingEvaluator(),
            "temporal": TemporalEvaluator(),
            "stale_memory": StaleMemoryEvaluator(),
            "continuity": ContinuityEvaluator(),
            "hallucination": HallucinationEvaluator(),
            "stress": StressEvaluator(),
            "temporal_drift": TemporalDriftEvaluator(),
            "adversarial_contradiction": AdversarialContradictionEvaluator(),
            "memory_poisoning": PoisoningEvaluator(),
        }

    def run(
        self,
        categories: list[Category] | None = None,
        report_dir: Path | str | None = "reports",
        stress: bool = False,
        config: BenchmarkSuiteConfig | None = None,
    ) -> BenchmarkRun:
        suite_config = config or BenchmarkSuiteConfig(categories=categories, stress=stress)
        scenarios = (
            generate_stress_scenarios()
            if suite_config.stress
            else load_scenarios(self.dataset_path, categories=suite_config.categories)
        )
        results = [
            self.evaluators[scenario.category].evaluate(scenario, self.adapter)
            for scenario in scenarios
        ]
        metrics = aggregate_results(results)
        run = BenchmarkRun(results=results, metrics=metrics)
        if report_dir is not None:
            ReportGenerator(Path(report_dir)).write(run)
        return run
