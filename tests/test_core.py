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
    assert len(scenarios) >= 80
    assert len({scenario.scenario_id for scenario in scenarios}) == len(scenarios)


def test_load_dataset_filter_category() -> None:
    assert len(load_scenarios(categories=["recall"])) == 20


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
    assert metrics.hallucination_rate == 0.0


def test_benchmark_runner_runs_all(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(report_dir=tmp_path)
    assert run.metrics.total_scenarios >= 80
    assert (tmp_path / "results.json").exists()


def test_benchmark_runner_category_filter(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(categories=["recall"], report_dir=tmp_path)
    assert run.metrics.total_scenarios == 20


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


def test_hallucination_dataset_and_evaluator() -> None:
    from memory_agent_eval_kit.evaluators.hallucination import HallucinationEvaluator

    scenarios = load_scenarios(categories=["hallucination"])
    assert len(scenarios) == 10
    result = HallucinationEvaluator().evaluate(scenarios[0], SimpleMemoryAgent())
    assert result.success


def test_hallucination_metrics_for_false_recall() -> None:
    bad = EvaluationResult("h", "hallucination", False, 0.0, 1.0)
    metrics = aggregate_results([bad])
    assert metrics.hallucination_rate == 1.0
    assert metrics.false_recall_rate == 1.0


def test_generate_stress_scenarios() -> None:
    from memory_agent_eval_kit.benchmarks.stress import generate_stress_scenarios

    scenarios = generate_stress_scenarios()
    assert [len(scenario.memory_events) for scenario in scenarios] == [10, 100, 1000]
    assert scenarios[-1].category == "stress"


def test_stress_runner_and_metrics(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(report_dir=tmp_path, stress=True)
    assert run.metrics.total_scenarios == 3
    assert run.metrics.stress_recall_accuracy == 1.0
    assert run.metrics.latency_degradation_ms >= 0.0


def test_cli_stress_flag(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["benchmark", "--stress", "--report-dir", str(tmp_path)]) == 0
    assert "Stress Recall" in capsys.readouterr().out


def test_temporal_drift_dataset_current_previous_timeline() -> None:
    scenarios = load_scenarios(categories=["temporal_drift"])
    assert len(scenarios) == 10
    ids = {scenario.scenario_id for scenario in scenarios}
    assert "temporal_drift_1_current" in ids
    assert "temporal_drift_1_previous" in ids
    assert "temporal_drift_1_timeline" in ids


def test_temporal_drift_evaluator_supports_timeline() -> None:
    from memory_agent_eval_kit.evaluators.temporal_drift import TemporalDriftEvaluator

    scenarios = load_scenarios(categories=["temporal_drift"])
    results = [
        TemporalDriftEvaluator().evaluate(scenario, SimpleMemoryAgent()) for scenario in scenarios
    ]
    assert all(result.success for result in results)
    assert aggregate_results(results).temporal_drift_accuracy == 1.0


def test_adversarial_contradiction_scenarios_and_metrics() -> None:
    from memory_agent_eval_kit.evaluators.adversarial_contradiction import (
        AdversarialContradictionEvaluator,
    )

    scenarios = load_scenarios(categories=["adversarial_contradiction"])
    assert len(scenarios) == 6
    results = [
        AdversarialContradictionEvaluator().evaluate(scenario, SimpleMemoryAgent())
        for scenario in scenarios
    ]
    metrics = aggregate_results(results)
    assert metrics.contradiction_resolution == 1.0
    assert metrics.ambiguity_handling == 1.0


def test_memory_poisoning_resistance_metric() -> None:
    from memory_agent_eval_kit.evaluators.poisoning import PoisoningEvaluator

    scenarios = load_scenarios(categories=["memory_poisoning"])
    assert len(scenarios) >= 10
    results = [
        PoisoningEvaluator().evaluate(scenario, SimpleMemoryAgent()) for scenario in scenarios
    ]
    assert all(result.success for result in results)
    assert aggregate_results(results).poisoning_resistance == 1.0


def test_simple_agent_ignores_untrusted_overlap() -> None:
    agent = SimpleMemoryAgent()
    agent.add_memory(
        {"memory_id": "good", "content": "Trusted timezone is Asia/Kolkata", "source": "trusted"}
    )
    agent.add_memory(
        {"memory_id": "bad", "content": "Trusted timezone is UTC", "source": "untrusted"}
    )
    answer = agent.query("What is the trusted timezone?")
    assert "Asia/Kolkata" in answer
    assert "UTC" not in answer


def test_forgetting_evaluator_runs_delayed_leak_checks() -> None:
    scenario = load_scenarios(categories=["forgetting"])[0]
    result = ForgettingEvaluator().evaluate(scenario, SimpleMemoryAgent())
    assert result.success
    assert result.details["verification_queries"]
    assert result.details["leak_detected"] is False


def test_memory_leak_rate_metric() -> None:
    leaked = EvaluationResult("f", "forgetting", False, 0.0, 1.0)
    metrics = aggregate_results([leaked])
    assert metrics.memory_leak_rate == 1.0


def test_semantic_scoring_utilities() -> None:
    from memory_agent_eval_kit.scoring import (
        exact_score,
        normalized_text,
        partial_score,
        token_overlap,
    )

    assert normalized_text("Hello, WORLD!") == "hello world"
    assert exact_score("Universal Robots", "universal robots") == 1.0
    assert token_overlap("favorite robot brand", "robot brand is UR") == pytest.approx(2 / 3)
    assert partial_score("Universal Robots", "Universal Robotics preference") > 0.7


def test_evaluator_partial_scoring_mode() -> None:
    scenario = BenchmarkScenario.from_dict(
        {
            "scenario_id": "partial_001",
            "category": "recall",
            "events": [],
            "query": "q",
            "expected_answer": "Universal Robots",
            "scoring_rules": {"mode": "partial", "threshold": 0.5, "allow_partial": True},
        }
    )
    assert RecallEvaluator().score_answer(scenario, "Universal Robotics") >= 0.5


def test_benchmark_suite_config_filters_categories(tmp_path: Path) -> None:
    from memory_agent_eval_kit.benchmarks import BenchmarkSuiteConfig

    config = BenchmarkSuiteConfig.for_categories(["hallucination"], suite_name="hallucination-only")
    run = BenchmarkRunner(SimpleMemoryAgent()).run(report_dir=tmp_path, config=config)
    assert run.metrics.total_scenarios == 10
    assert run.metrics.hallucination_accuracy == 1.0


def test_cli_category_hallucination(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["benchmark", "--category", "hallucination", "--report-dir", str(tmp_path)]) == 0
    assert "False Recall Rate" in capsys.readouterr().out


def test_leaderboard_generation(tmp_path: Path) -> None:
    from memory_agent_eval_kit.leaderboards import LeaderboardGenerator

    report_dir = tmp_path / "reports"
    BenchmarkRunner(SimpleMemoryAgent()).run(categories=["recall"], report_dir=report_dir)
    output_dir = tmp_path / "leaderboards"
    generator = LeaderboardGenerator(output_dir)
    entry = generator.from_report(report_dir / "results.json", "agent", "recall")
    generator.write([entry])
    assert (output_dir / "results.json").exists()
    assert "agent" in (output_dir / "results.md").read_text(encoding="utf-8")


def test_cli_leaderboard(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    report_dir = tmp_path / "reports"
    BenchmarkRunner(SimpleMemoryAgent()).run(categories=["recall"], report_dir=report_dir)
    output_dir = tmp_path / "leaderboards"
    assert (
        main(
            [
                "leaderboard",
                "--report",
                str(report_dir / "results.json"),
                "--output-dir",
                str(output_dir),
            ]
        )
        == 0
    )
    assert "Leaderboard written" in capsys.readouterr().out
    assert (output_dir / "results.md").exists()


def test_file_backed_memory_agent_persists(tmp_path: Path) -> None:
    from memory_agent_eval_kit.adapters import FileBackedMemoryAgent

    path = tmp_path / "memories.json"
    agent = FileBackedMemoryAgent(path)
    agent.add_memory({"memory_id": "m", "content": "Favorite robot brand is Universal Robots"})
    reloaded = FileBackedMemoryAgent(path)
    assert "Universal Robots" in reloaded.query("What robot brand do I prefer?")


def test_session_memory_agent_sets_default_session() -> None:
    from memory_agent_eval_kit.adapters import SessionMemoryAgent

    agent = SessionMemoryAgent("session-a")
    agent.add_memory({"memory_id": "m", "content": "Project codename is Lotus"})
    assert "Lotus" in agent.query_session("What is the project codename?", "session-a")


def test_improved_report_contains_breakdowns(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(categories=["recall"], report_dir=tmp_path)
    payload = json.loads((tmp_path / "results.json").read_text(encoding="utf-8"))
    assert "category_breakdown" in payload
    assert "weakest_categories" in payload
    markdown = (tmp_path / "results.md").read_text(encoding="utf-8")
    assert "## Pass/Fail Table" in markdown
    assert "## Strongest Categories" in markdown
    assert run.metrics.total_scenarios == 20


def test_validate_dataset_success() -> None:
    from memory_agent_eval_kit.datasets import validate_dataset

    result = validate_dataset()
    assert result.valid
    assert result.scenario_count >= 150


def test_validate_dataset_reports_duplicates(tmp_path: Path) -> None:
    from memory_agent_eval_kit.datasets import validate_dataset

    payload = [
        {
            "scenario_id": "dup",
            "category": "recall",
            "events": [],
            "query": "q",
            "expected_answer": "a",
        },
        {
            "scenario_id": "dup",
            "category": "recall",
            "events": [],
            "query": "q",
            "expected_answer": "a",
        },
    ]
    path = tmp_path / "dup.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    result = validate_dataset(path)
    assert not result.valid
    assert result.errors


def test_cli_validate(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["validate"]) == 0
    assert "Dataset valid" in capsys.readouterr().out


def test_memory_leakage_suite_metrics() -> None:
    from memory_agent_eval_kit.evaluators.memory_leakage import MemoryLeakageEvaluator

    scenarios = load_scenarios(categories=["memory_leakage"])
    assert len(scenarios) == 5
    results = [
        MemoryLeakageEvaluator().evaluate(scenario, SimpleMemoryAgent()) for scenario in scenarios
    ]
    metrics = aggregate_results(results)
    assert metrics.leak_rate == 0.0
    assert metrics.delayed_leak_rate == 0.0


def test_hallucinated_recall_suite() -> None:
    from memory_agent_eval_kit.evaluators.hallucinated_recall import HallucinatedRecallEvaluator

    scenarios = load_scenarios(categories=["hallucinated_recall"])
    assert len(scenarios) == 8
    results = [
        HallucinatedRecallEvaluator().evaluate(scenario, SimpleMemoryAgent())
        for scenario in scenarios
    ]
    metrics = aggregate_results(results)
    assert metrics.hallucinated_recall_accuracy == 1.0
    assert metrics.false_recall_rate == 0.0


def test_timeline_reasoning_suite() -> None:
    from memory_agent_eval_kit.evaluators.timeline_reasoning import TimelineReasoningEvaluator

    scenarios = load_scenarios(categories=["timeline_reasoning"])
    assert len(scenarios) == 3
    results = [
        TimelineReasoningEvaluator().evaluate(scenario, SimpleMemoryAgent())
        for scenario in scenarios
    ]
    assert aggregate_results(results).timeline_reasoning_accuracy == 1.0


def test_memory_drift_suite_metrics() -> None:
    from memory_agent_eval_kit.evaluators.memory_drift import MemoryDriftEvaluator

    scenarios = load_scenarios(categories=["memory_drift"])
    assert len(scenarios) == 5
    results = [
        MemoryDriftEvaluator().evaluate(scenario, SimpleMemoryAgent()) for scenario in scenarios
    ]
    metrics = aggregate_results(results)
    assert metrics.drift_accuracy == 1.0
    assert metrics.update_accuracy == 1.0


def test_expanded_poisoning_suite_has_trust_variants() -> None:
    scenarios = load_scenarios(categories=["memory_poisoning"])
    assert len(scenarios) >= 16
    poisoning_types = {
        scenario.expected_behavior.metadata.get("poisoning_type") for scenario in scenarios
    }
    assert "malicious update" in poisoning_types
    assert "source trust" in poisoning_types


def test_benchmark_seed_deterministic_order(tmp_path: Path) -> None:
    run_a = BenchmarkRunner(SimpleMemoryAgent()).run(
        categories=["recall"], report_dir=tmp_path / "a", seed=42
    )
    run_b = BenchmarkRunner(SimpleMemoryAgent()).run(
        categories=["recall"], report_dir=tmp_path / "b", seed=42
    )
    assert [result.scenario_id for result in run_a.results] == [
        result.scenario_id for result in run_b.results
    ]


def test_cli_seed_flag(tmp_path: Path) -> None:
    assert (
        main(["benchmark", "--category", "recall", "--seed", "42", "--report-dir", str(tmp_path)])
        == 0
    )


def test_compare_results_detects_score_and_category_regressions(tmp_path: Path) -> None:
    from memory_agent_eval_kit.reports import compare_results

    baseline = {
        "metrics": {"overall_score": 0.95},
        "category_breakdown": {"recall": {"score": 1.0}, "temporal": {"score": 0.9}},
    }
    candidate = {
        "metrics": {"overall_score": 0.90},
        "category_breakdown": {"recall": {"score": 0.8}, "temporal": {"score": 0.95}},
    }
    baseline_path = tmp_path / "baseline.json"
    candidate_path = tmp_path / "candidate.json"
    baseline_path.write_text(json.dumps(baseline), encoding="utf-8")
    candidate_path.write_text(json.dumps(candidate), encoding="utf-8")

    comparison = compare_results(baseline_path, candidate_path, regression_threshold=-0.01)

    assert comparison.score_delta == pytest.approx(-0.05)
    assert "overall" in comparison.regressions
    assert "recall" in comparison.regressions
    assert comparison.to_dict()["has_regressions"] is True


def test_cli_fail_under_passes_when_score_meets_threshold(tmp_path: Path) -> None:
    assert (
        main(
            [
                "benchmark",
                "--category",
                "recall",
                "--fail-under",
                "90",
                "--report-dir",
                str(tmp_path),
            ]
        )
        == 0
    )


def test_cli_fail_under_fails_when_score_drops(tmp_path: Path) -> None:
    assert (
        main(
            [
                "benchmark",
                "--category",
                "hallucination",
                "--fail-under",
                "101",
                "--report-dir",
                str(tmp_path),
            ]
        )
        == 1
    )


def test_leaderboard_assigns_overall_category_and_latency_ranks(tmp_path: Path) -> None:
    from memory_agent_eval_kit.leaderboards.generator import (
        LeaderboardEntry,
        LeaderboardGenerator,
        rank_entries,
    )

    entries = [
        LeaderboardEntry(
            "fast",
            "suite",
            0.90,
            {"recall": 0.90, "temporal": 0.90},
            {"avg_ms": 5.0, "p95_ms": 6.0},
        ),
        LeaderboardEntry(
            "accurate",
            "suite",
            0.95,
            {"recall": 0.95, "temporal": 0.95},
            {"avg_ms": 10.0, "p95_ms": 12.0},
        ),
    ]
    ranked = rank_entries(entries)
    assert ranked[0].agent_name == "accurate"
    assert ranked[0].overall_rank == 1
    assert ranked[0].category_rank == 1
    assert ranked[0].latency_rank == 2

    LeaderboardGenerator(tmp_path).write(entries)
    payload = json.loads((tmp_path / "results.json").read_text(encoding="utf-8"))
    assert {"overall_rank", "category_rank", "latency_rank"} <= set(payload[0])


def test_generate_visual_assets_writes_svg_files(tmp_path: Path) -> None:
    from memory_agent_eval_kit.reports import generate_visual_assets

    report = {
        "metrics": {
            "overall_score": 0.91,
            "recall_accuracy": 1.0,
            "forgetting_accuracy": 0.8,
            "poisoning_resistance": 0.95,
            "timeline_reasoning_accuracy": 0.9,
            "drift_accuracy": 0.85,
        },
        "category_breakdown": {"recall": {"score": 1.0}, "forgetting": {"score": 0.8}},
    }
    leaderboard = [{"agent_name": "agent-a", "overall_score": 0.91}]
    report_path = tmp_path / "report.json"
    leaderboard_path = tmp_path / "leaderboard.json"
    output_dir = tmp_path / "visuals"
    report_path.write_text(json.dumps(report), encoding="utf-8")
    leaderboard_path.write_text(json.dumps(leaderboard), encoding="utf-8")

    paths = generate_visual_assets(report_path, leaderboard_path, output_dir)

    assert {path.name for path in paths} == {
        "category_score_chart.svg",
        "leaderboard_chart.svg",
        "benchmark_summary_chart.svg",
    }
    assert all(path.read_text(encoding="utf-8").startswith("<svg") for path in paths)


def test_long_horizon_memory_benchmarks_measure_recall_and_latency(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(categories=["long_horizon"], report_dir=tmp_path)
    assert len(run.results) == 3
    assert run.metrics.long_horizon_recall_accuracy == 1.0
    assert run.metrics.long_horizon_latency_ms >= 0.0


def test_noisy_memory_benchmarks_measure_precision_and_robustness(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(categories=["noisy_memory"], report_dir=tmp_path)
    assert len(run.results) == 5
    assert run.metrics.retrieval_precision == 1.0
    assert run.metrics.retrieval_robustness == 1.0


def test_preference_evolution_benchmarks_measure_updates(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(
        categories=["preference_evolution"], report_dir=tmp_path
    )
    assert len(run.results) == 6
    assert run.metrics.preference_update_accuracy == 1.0


def test_relationship_memory_benchmarks_measure_relationship_and_role(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(
        categories=["relationship_memory"], report_dir=tmp_path
    )
    assert len(run.results) == 4
    assert run.metrics.relationship_recall_accuracy == 1.0
    assert run.metrics.role_recall_accuracy == 1.0


def test_hierarchical_memory_benchmarks_measure_retrieval(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(
        categories=["hierarchical_memory"], report_dir=tmp_path
    )
    assert len(run.results) == 3
    assert run.metrics.hierarchical_retrieval_accuracy == 1.0


def test_pii_deletion_benchmarks_verify_no_recall_after_deletion(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(categories=["pii_deletion"], report_dir=tmp_path)
    assert len(run.results) == 3
    assert run.metrics.pii_deletion_success == 1.0


def test_gdpr_forgetting_benchmarks_measure_compliance(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(
        categories=["gdpr_forgetting"], report_dir=tmp_path
    )
    assert len(run.results) == 3
    assert run.metrics.gdpr_compliance_score == 1.0


def test_retention_policy_benchmarks_measure_compliance(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(
        categories=["retention_policy"], report_dir=tmp_path
    )
    assert len(run.results) == 3
    assert run.metrics.retention_compliance == 1.0


def test_sensitive_memory_classification_benchmarks_measure_accuracy(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(
        categories=["sensitive_classification"], report_dir=tmp_path
    )
    assert len(run.results) == 5
    assert run.metrics.classification_accuracy == 1.0


def test_enterprise_compliance_metrics_surface_in_reports_and_leaderboard(tmp_path: Path) -> None:
    report_dir = tmp_path / "reports"
    run = BenchmarkRunner(SimpleMemoryAgent()).run(
        categories=[
            "pii_deletion",
            "gdpr_forgetting",
            "retention_policy",
            "sensitive_classification",
        ],
        report_dir=report_dir,
    )
    assert run.metrics.compliance_score == 1.0
    assert run.metrics.deletion_score == 1.0
    assert run.metrics.retention_score == 1.0
    assert run.metrics.privacy_score == 1.0
    report_text = (report_dir / "results.md").read_text(encoding="utf-8")
    assert "Compliance Score" in report_text

    from memory_agent_eval_kit.leaderboards import LeaderboardGenerator

    entry = LeaderboardGenerator(tmp_path / "leaderboard").from_report(report_dir / "results.json")
    assert entry.category_scores["compliance_score"] == 1.0


def test_shared_memory_benchmarks_measure_consistency(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(
        categories=["shared_memory"], report_dir=tmp_path
    )
    assert len(run.results) == 3
    assert run.metrics.shared_memory_consistency == 1.0


def test_memory_synchronization_benchmarks_measure_propagation(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(
        categories=["memory_synchronization"], report_dir=tmp_path
    )
    assert len(run.results) == 3
    assert run.metrics.propagation_correctness == 1.0
    assert run.metrics.synchronization_accuracy == 1.0


def test_agent_disagreement_benchmarks_measure_detection(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(
        categories=["agent_disagreement"], report_dir=tmp_path
    )
    assert len(run.results) == 3
    assert run.metrics.disagreement_detection == 1.0


def test_conflict_resolution_benchmarks_measure_resolution_quality(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(
        categories=["conflict_resolution"], report_dir=tmp_path
    )
    assert len(run.results) == 3
    assert run.metrics.conflict_handling_accuracy == 1.0
    assert run.metrics.resolution_quality == 1.0


def test_collaborative_memory_benchmarks_measure_recall(tmp_path: Path) -> None:
    run = BenchmarkRunner(SimpleMemoryAgent()).run(
        categories=["collaborative_memory"], report_dir=tmp_path
    )
    assert len(run.results) == 3
    assert run.metrics.collaborative_recall == 1.0


def test_benchmark_suite_version_metadata_is_attached() -> None:
    from memory_agent_eval_kit.datasets.versions import CURRENT_SUITE_VERSION, SUITE_VERSIONS

    scenarios = load_scenarios(categories=["recall"])
    assert CURRENT_SUITE_VERSION == "v3"
    assert {version.version for version in SUITE_VERSIONS} == {"v1", "v2", "v3"}
    assert all(scenario.suite_version == "v3" for scenario in scenarios)


def test_dataset_changelog_generation_tracks_added_removed_modified(tmp_path: Path) -> None:
    from memory_agent_eval_kit.datasets import generate_dataset_changelog, write_dataset_changelog

    before = [
        {"scenario_id": "same", "category": "recall", "query": "q", "expected_answer": "a"},
        {"scenario_id": "removed", "category": "recall", "query": "q", "expected_answer": "a"},
        {"scenario_id": "modified", "category": "recall", "query": "q", "expected_answer": "a"},
    ]
    after = [
        {"scenario_id": "same", "category": "recall", "query": "q", "expected_answer": "a"},
        {"scenario_id": "modified", "category": "recall", "query": "q2", "expected_answer": "a"},
        {"scenario_id": "added", "category": "recall", "query": "q", "expected_answer": "a"},
    ]
    changelog = generate_dataset_changelog(before, after)
    assert changelog.added == ["added"]
    assert changelog.removed == ["removed"]
    assert changelog.modified == ["modified"]
    output = tmp_path / "dataset_changelog.json"
    write_dataset_changelog(before, after, output)
    assert json.loads(output.read_text(encoding="utf-8"))["added"] == ["added"]


def test_scenario_deprecation_status_support(tmp_path: Path) -> None:
    from memory_agent_eval_kit.datasets.validation import validate_dataset

    payload = [
        {
            "scenario_id": "active_case",
            "category": "recall",
            "events": [],
            "query": "What is active?",
            "expected_answer": "active",
            "status": "active",
        },
        {
            "scenario_id": "deprecated_case",
            "category": "recall",
            "events": [],
            "query": "What was deprecated?",
            "expected_answer": "deprecated",
            "status": "deprecated",
            "deprecation_reason": "Replaced by a richer recall scenario.",
        },
    ]
    dataset = tmp_path / "dataset.json"
    dataset.write_text(json.dumps(payload), encoding="utf-8")
    assert validate_dataset(dataset).valid
    assert len(load_scenarios(dataset, statuses=["active"])) == 1
    assert load_scenarios(dataset, statuses=["deprecated"])[0].status == "deprecated"


def test_deprecated_scenarios_require_reason(tmp_path: Path) -> None:
    from memory_agent_eval_kit.datasets.validation import validate_dataset

    dataset = tmp_path / "dataset.json"
    dataset.write_text(
        json.dumps(
            [
                {
                    "scenario_id": "deprecated_without_reason",
                    "category": "recall",
                    "events": [],
                    "query": "q",
                    "expected_answer": "a",
                    "status": "deprecated",
                }
            ]
        ),
        encoding="utf-8",
    )
    result = validate_dataset(dataset)
    assert not result.valid
    assert "deprecation_reason" in result.errors[0]


def test_benchmark_version_comparison_generates_deltas(tmp_path: Path) -> None:
    from memory_agent_eval_kit.reports import (
        compare_benchmark_versions,
        write_benchmark_version_comparison,
    )

    v1 = {
        "metrics": {"overall_score": 0.8},
        "category_breakdown": {"recall": {"score": 0.8}},
    }
    v2 = {
        "metrics": {"overall_score": 0.9},
        "category_breakdown": {"recall": {"score": 0.95}, "temporal": {"score": 0.7}},
    }
    v3 = {
        "metrics": {"overall_score": 0.85},
        "category_breakdown": {"recall": {"score": 0.9}, "temporal": {"score": 0.8}},
    }
    report = compare_benchmark_versions({"v1": v1, "v2": v2, "v3": v3})
    assert len(report.comparisons) == 2
    assert report.comparisons[0].baseline_version == "v1"
    assert report.comparisons[0].candidate_version == "v2"
    assert report.comparisons[0].comparison.score_delta == pytest.approx(0.1)
    output = tmp_path / "version_comparison.json"
    write_benchmark_version_comparison({"v1": v1, "v2": v2, "v3": v3}, output)
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["comparisons"][1]["baseline_version"] == "v2"
    assert payload["comparisons"][1]["candidate_version"] == "v3"
    assert payload["comparisons"][1]["category_deltas"][0]["category"] == "recall"


def test_historical_benchmark_archive_support(tmp_path: Path) -> None:
    from datetime import UTC, datetime

    from memory_agent_eval_kit.reports import archive_benchmark_report, list_benchmark_archives

    report = {"metrics": {"overall_score": 0.91, "total_scenarios": 253}}
    record = archive_benchmark_report(
        report,
        tmp_path,
        suite_version="v3",
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
    )
    archive_path = Path(record.archive_path)
    assert archive_path.exists()
    payload = json.loads(archive_path.read_text(encoding="utf-8"))
    assert payload["archive"]["suite_version"] == "v3"
    assert payload["archive"]["scenario_count"] == 253
    assert list_benchmark_archives(tmp_path) == [archive_path]


def test_mem0_adapter_gracefully_falls_back_when_dependency_missing() -> None:
    from memory_agent_eval_kit.adapters import Mem0Adapter

    fallback = SimpleMemoryAgent()
    adapter = Mem0Adapter(fallback=fallback)
    assert not adapter.available
    adapter.add_memory({"memory_id": "mem0-local", "content": "Mem0 fallback color is blue"})
    assert "blue" in adapter.query("What is the Mem0 fallback color?")
    adapter.delete_memory("mem0-local")
    assert "I do not know" in adapter.query("What is the Mem0 fallback color?")


def test_mem0_adapter_uses_configured_client() -> None:
    from memory_agent_eval_kit.adapters import Mem0Adapter

    class FakeMem0Client:
        def __init__(self) -> None:
            self.memories: list[dict[str, object]] = []
            self.deleted: list[str] = []

        def add(self, content: str, *, user_id: str, metadata: dict[str, object]) -> None:
            self.memories.append({"memory": content, "user_id": user_id, **metadata})

        def search(self, prompt: str, *, user_id: str) -> list[dict[str, object]]:
            return [item for item in self.memories if item["user_id"] == user_id]

        def delete(self, *, memory_id: str, user_id: str) -> None:
            self.deleted.append(f"{user_id}:{memory_id}")

    client = FakeMem0Client()
    adapter = Mem0Adapter(client=client, user_id="u1")
    assert adapter.available
    adapter.add_memory({"memory_id": "m1", "content": "Mem0 client fact is real"})
    assert "real" in adapter.query("What is the Mem0 client fact?")
    adapter.delete_memory("m1")
    assert client.deleted == ["u1:m1"]


def test_langgraph_adapter_gracefully_falls_back_when_app_missing() -> None:
    from memory_agent_eval_kit.adapters import LangGraphAdapter

    adapter = LangGraphAdapter(fallback=SimpleMemoryAgent())
    assert not adapter.available
    adapter.add_memory({"memory_id": "lg-local", "content": "LangGraph fallback city is Pune"})
    assert "Pune" in adapter.query("What is the LangGraph fallback city?")
    adapter.delete_memory("lg-local")
    assert "I do not know" in adapter.query("What is the LangGraph fallback city?")


def test_langgraph_adapter_uses_configured_graph() -> None:
    from memory_agent_eval_kit.adapters import LangGraphAdapter

    class FakeGraph:
        def __init__(self) -> None:
            self.memories: list[str] = []
            self.deleted: list[str] = []

        def invoke(self, payload: dict[str, object]) -> dict[str, object]:
            return {"messages": [("assistant", "\n".join(self.memories))]}

        def add_memory(self, memory: dict[str, object]) -> None:
            self.memories.append(str(memory["content"]))

        def delete_memory(self, memory_id: str) -> None:
            self.deleted.append(memory_id)

    graph = FakeGraph()
    adapter = LangGraphAdapter(graph=graph)
    assert adapter.available
    adapter.add_memory({"memory_id": "m1", "content": "LangGraph graph fact is real"})
    assert "real" in adapter.query("What is the LangGraph graph fact?")
    adapter.delete_memory("m1")
    assert graph.deleted == ["m1"]
