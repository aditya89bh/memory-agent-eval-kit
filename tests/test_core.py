from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from memory_agent_eval_kit.adapters import MemoryAgentAdapter, SimpleMemoryAgent
from memory_agent_eval_kit.benchmarks import BenchmarkRunner
from memory_agent_eval_kit.cli import build_parser, main
from memory_agent_eval_kit.datasets import DatasetError, load_scenarios
from memory_agent_eval_kit.evaluators import (
    ContinuityEvaluator,
    ContradictionEvaluator,
    CorrectionEvaluator,
    ForgettingEvaluator,
    RecallEvaluator,
    StaleMemoryEvaluator,
    TemporalEvaluator,
)
from memory_agent_eval_kit.metrics import EvaluationResult, aggregate_results
from memory_agent_eval_kit.models import BenchmarkScenario, MemoryEvent
from memory_agent_eval_kit.reports.generator import ReportGenerator


def test_adapter_is_abstract() -> None:
    with pytest.raises(TypeError):
        MemoryAgentAdapter()  # type: ignore[abstract]


def test_simple_agent_add_and_query() -> None:
    agent = SimpleMemoryAgent()
    agent.add_memory({"memory_id": "1", "content": "Favorite robot brand is Universal Robots"})
    assert "Universal Robots" in agent.query("What robot brand do I prefer?")


def test_simple_agent_delete() -> None:
    agent = SimpleMemoryAgent()
    agent.add_memory({"memory_id": "1", "content": "Temporary password is alpha123"})
    agent.delete_memory("1")
    assert "I do not know" in agent.query("What is my temporary password?")


def test_simple_agent_correction_supersedes_old() -> None:
    agent = SimpleMemoryAgent()
    agent.add_memory({"memory_id": "old", "content": "Preferred language is JavaScript"})
    agent.add_memory(
        {
            "memory_id": "new",
            "type": "correction",
            "supersedes": "old",
            "content": "Preferred language is Python",
        }
    )
    answer = agent.query("What language do I prefer now?")
    assert "Python" in answer
    assert "JavaScript" not in answer


def test_simple_agent_inactive_memory_is_ignored() -> None:
    agent = SimpleMemoryAgent()
    agent.add_memory({"memory_id": "old", "active": False, "content": "Old city is Pune"})
    agent.add_memory({"memory_id": "new", "content": "Current city is Delhi"})
    assert "Delhi" in agent.query("Which city is current?")


def test_simple_agent_temporal_prefers_recent() -> None:
    agent = SimpleMemoryAgent()
    agent.add_memory(
        {
            "memory_id": "old",
            "timestamp": "2026-01-01T00:00:00Z",
            "content": "Preferred model was GPT-4",
        }
    )
    agent.add_memory(
        {
            "memory_id": "new",
            "timestamp": "2026-02-01T00:00:00Z",
            "content": "Preferred model was GPT-5",
        }
    )
    assert "GPT-5" in agent.query("What model was preferred most recently?")


def test_simple_agent_detects_contradiction() -> None:
    agent = SimpleMemoryAgent()
    agent.add_memory({"memory_id": "a", "content": "Preferred IDE is VS Code"})
    agent.add_memory({"memory_id": "b", "content": "Preferred IDE is Vim"})
    assert "contradiction" in agent.query("What is my preferred IDE?").casefold()


def test_memory_event_from_dict_preserves_metadata() -> None:
    event = MemoryEvent.from_dict({"type": "fact", "content": "x", "confidence": 0.8})
    assert event.metadata == {"confidence": 0.8}
    assert event.to_memory()["confidence"] == 0.8


def test_benchmark_scenario_from_dict_defaults() -> None:
    scenario = BenchmarkScenario.from_dict(
        {
            "scenario_id": "x",
            "category": "recall",
            "memory_events": [],
            "query": "q",
            "expected_answer": "a",
        }
    )
    assert scenario.expected_absent == []


def test_load_default_dataset_has_70_scenarios() -> None:
    scenarios = load_scenarios()
    assert len(scenarios) == 70
    assert len({scenario.scenario_id for scenario in scenarios}) == 70


def test_load_dataset_filter_category() -> None:
    assert len(load_scenarios(categories=["recall"])) == 10


def test_load_dataset_rejects_non_list(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("{}", encoding="utf-8")
    with pytest.raises(DatasetError):
        load_scenarios(path)


def test_load_dataset_rejects_duplicate_ids(tmp_path: Path) -> None:
    payload = [
        {
            "scenario_id": "dup",
            "category": "recall",
            "memory_events": [],
            "query": "q",
            "expected_answer": "a",
        },
        {
            "scenario_id": "dup",
            "category": "recall",
            "memory_events": [],
            "query": "q",
            "expected_answer": "a",
        },
    ]
    path = tmp_path / "dup.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(DatasetError):
        load_scenarios(path)


def test_recall_evaluator_success() -> None:
    scenario = load_scenarios(categories=["recall"])[0]
    result = RecallEvaluator().evaluate(scenario, SimpleMemoryAgent())
    assert result.success


def test_contradiction_evaluator_success() -> None:
    scenario = load_scenarios(categories=["contradiction"])[0]
    result = ContradictionEvaluator().evaluate(scenario, SimpleMemoryAgent())
    assert result.success


def test_correction_evaluator_success() -> None:
    scenario = load_scenarios(categories=["correction"])[0]
    result = CorrectionEvaluator().evaluate(scenario, SimpleMemoryAgent())
    assert result.success


def test_forgetting_evaluator_success() -> None:
    scenario = load_scenarios(categories=["forgetting"])[0]
    result = ForgettingEvaluator().evaluate(scenario, SimpleMemoryAgent())
    assert result.success


def test_temporal_evaluator_success() -> None:
    scenario = load_scenarios(categories=["temporal"])[0]
    result = TemporalEvaluator().evaluate(scenario, SimpleMemoryAgent())
    assert result.success


def test_stale_memory_evaluator_success() -> None:
    scenario = load_scenarios(categories=["stale_memory"])[0]
    result = StaleMemoryEvaluator().evaluate(scenario, SimpleMemoryAgent())
    assert result.success


def test_continuity_evaluator_success() -> None:
    scenario = load_scenarios(categories=["continuity"])[0]
    result = ContinuityEvaluator().evaluate(senario := scenario, SimpleMemoryAgent())
    assert result.scenario_id == senario.scenario_id
    assert result.success


def test_evaluator_rejects_wrong_category() -> None:
    scenario = load_scenarios(categories=["recall"])[0]
    with pytest.raises(ValueError):
        CorrectionEvaluator().evaluate(scenario, SimpleMemoryAgent())


def test_aggregate_results() -> None:
    results = [
        EvaluationResult("a", "recall", True, 1.0, 1.0),
        EvaluationResult("b", "recall", False, 0.0, 3.0),
    ]
    metrics = aggregate_results(results)
    assert metrics.overall_score == 0.5
    assert metrics.recall_accuracy == 0.5
    assert metrics.latency_avg_ms == 2.0


def test_benchmark_runner_runs_all(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(report_dir=tmp_path)
    assert run.metrics.total_scenarios == 70
    assert (tmp_path / "results.json").exists()


def test_benchmark_runner_category_filter(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(categories=["recall"], report_dir=tmp_path)
    assert run.metrics.total_scenarios == 10


def test_report_generator_outputs_files(tmp_path: Path) -> None:
    result = EvaluationResult(
        "x", "recall", True, 1.0, 2.0, {"actual_answer": "a", "expected_answer": "a"}
    )

    class Run:
        results = [result]
        metrics = aggregate_results([result])

    ReportGenerator(tmp_path).write(Run())  # type: ignore[arg-type]
    assert (
        json.loads((tmp_path / "results.json").read_text(encoding="utf-8"))["metrics"][
            "overall_score"
        ]
        == 1.0
    )
    assert (
        list(csv.DictReader((tmp_path / "results.csv").open(encoding="utf-8")))[0]["scenario_id"]
        == "x"
    )
    assert "Overall Score" in (tmp_path / "results.md").read_text(encoding="utf-8")


def test_cli_parser_has_benchmark() -> None:
    parser = build_parser()
    args = parser.parse_args(["benchmark", "--category", "recall"])
    assert args.command == "benchmark"
    assert args.category == ["recall"]


def test_cli_benchmark(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["benchmark", "--category", "recall", "--report-dir", str(tmp_path)]) == 0
    captured = capsys.readouterr()
    assert "Overall Score" in captured.out
    assert (tmp_path / "results.md").exists()


def test_rich_scenario_schema_aliases_and_defaults() -> None:
    scenario = BenchmarkScenario.from_dict(
        {
            "scenario_id": "rich_001",
            "category": "recall",
            "events": [
                {
                    "type": "fact",
                    "memory_id": "m1",
                    "session_id": "s1",
                    "timestamp": "2026-06-01T00:00:00Z",
                    "content": "Favorite robot is UR5",
                }
            ],
            "query": "What robot is favorite?",
            "expected_behavior": {"answer": "UR5", "rationale": "stored fact"},
            "scoring_rules": {"mode": "exact", "threshold": 0.9},
            "negative_assertions": ["ABB"],
        }
    )
    assert scenario.memory_events == scenario.events
    assert scenario.expected_answer == "UR5"
    assert scenario.expected_behavior.rationale == "stored fact"
    assert scenario.scoring_rules.threshold == 0.9
    assert scenario.sessions == ["s1"]
    assert scenario.timestamps == ["2026-06-01T00:00:00Z"]
    assert scenario.expected_absent == ["ABB"]


def test_scenario_to_dict_contains_legacy_and_rich_fields() -> None:
    scenario = load_scenarios(categories=["recall"])[0]
    payload = scenario.to_dict()
    assert "events" in payload
    assert "memory_events" in payload
    assert "expected_behavior" in payload
    assert "negative_assertions" in payload
