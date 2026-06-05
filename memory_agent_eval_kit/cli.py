"""Command line interface for memory-agent-eval-kit."""

from __future__ import annotations

import argparse
from pathlib import Path

from memory_agent_eval_kit.adapters.simple import SimpleMemoryAgent
from memory_agent_eval_kit.benchmarks import BenchmarkRunner
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
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "benchmark":
        adapter = SimpleMemoryAgent()
        runner = BenchmarkRunner(adapter=adapter, dataset_path=args.dataset)
        categories = None if args.category is None else list(args.category)
        run = runner.run(categories=categories, report_dir=args.report_dir)
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
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
