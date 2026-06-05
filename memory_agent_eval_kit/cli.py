"""Command line interface for memory-agent-eval-kit."""

from __future__ import annotations

import argparse
from pathlib import Path

from memory_agent_eval_kit.adapters.simple import SimpleMemoryAgent
from memory_agent_eval_kit.benchmarks import BenchmarkRunner
from memory_agent_eval_kit.datasets import validate_dataset
from memory_agent_eval_kit.leaderboards import LeaderboardGenerator
from memory_agent_eval_kit.metrics import AggregateMetrics
from memory_agent_eval_kit.models import Category

CATEGORY_CHOICES: tuple[Category, ...] = (
    "recall",
    "contradiction",
    "correction",
    "forgetting",
    "temporal",
    "stale_memory",
    "continuity",
    "hallucination",
    "stress",
    "temporal_drift",
    "adversarial_contradiction",
    "memory_poisoning",
    "memory_leakage",
    "hallucinated_recall",
    "timeline_reasoning",
    "memory_drift",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="memory-eval")
    subparsers = parser.add_subparsers(dest="command", required=True)
    benchmark = subparsers.add_parser("benchmark", help="Run memory agent benchmarks")
    benchmark.add_argument("--dataset", type=Path, default=None, help="Optional JSON dataset path")
    benchmark.add_argument(
        "--report-dir",
        type=Path,
        default=Path("reports"),
        help="Report output directory",
    )
    benchmark.add_argument(
        "--category",
        choices=CATEGORY_CHOICES,
        action="append",
        help="Run one or more categories",
    )
    benchmark.add_argument(
        "--stress", action="store_true", help="Run synthetic memory stress suite"
    )
    benchmark.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Deterministic scenario order seed",
    )
    validate = subparsers.add_parser("validate", help="Validate benchmark dataset")
    validate.add_argument("--dataset", type=Path, default=None)

    leaderboard = subparsers.add_parser("leaderboard", help="Generate leaderboard files")
    leaderboard.add_argument("--report", type=Path, default=Path("reports/results.json"))
    leaderboard.add_argument("--output-dir", type=Path, default=Path("leaderboards"))
    leaderboard.add_argument("--agent-name", default="SimpleMemoryAgent")
    leaderboard.add_argument("--suite-name", default="default")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "validate":
        result = validate_dataset(args.dataset)
        if result.valid:
            print(f"Dataset valid: {result.scenario_count} scenarios")
            return 0
        print("Dataset invalid:")
        for error in result.errors:
            print(f"- {error}")
        return 1
    if args.command == "leaderboard":
        generator = LeaderboardGenerator(args.output_dir)
        entry = generator.from_report(args.report, args.agent_name, args.suite_name)
        generator.write([entry])
        print(f"Leaderboard written to {args.output_dir}")
        return 0
    if args.command == "benchmark":
        adapter = SimpleMemoryAgent()
        runner = BenchmarkRunner(adapter=adapter, dataset_path=args.dataset)
        categories = None if args.category is None else list(args.category)
        run = runner.run(
            categories=categories,
            report_dir=args.report_dir,
            stress=args.stress,
            seed=args.seed,
        )
        print(_format_summary(run.metrics))
        return 0
    parser.error("Unknown command")
    return 2


def _format_summary(metrics: AggregateMetrics) -> str:
    def pct(value: float) -> str:
        return f"{value * 100:.0f}%"

    return "\n".join(
        [
            f"Overall Score: {pct(metrics.overall_score)}",
            "",
            f"Recall: {pct(metrics.recall_accuracy)}",
            f"Contradictions: {pct(metrics.contradiction_accuracy)}",
            f"Corrections: {pct(metrics.correction_accuracy)}",
            f"Forgetting: {pct(metrics.forgetting_accuracy)}",
            f"Temporal: {pct(metrics.temporal_accuracy)}",
            f"Stale Memory: {pct(metrics.stale_memory_accuracy)}",
            f"Continuity: {pct(metrics.continuity_accuracy)}",
            f"Hallucination Rate: {pct(metrics.hallucination_rate)}",
            f"False Recall Rate: {pct(metrics.false_recall_rate)}",
            f"Stress Recall: {pct(metrics.stress_recall_accuracy)}",
            f"Latency Degradation: {metrics.latency_degradation_ms:.2f} ms",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
