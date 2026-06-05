"""Run the full benchmark suite with a local in-memory agent.

Usage:
    python examples/simple_memory_agent.py
"""

from __future__ import annotations

from memory_agent_eval_kit.adapters.simple import SimpleMemoryAgent
from memory_agent_eval_kit.benchmarks import BenchmarkRunner
from memory_agent_eval_kit.cli import _format_summary


def main() -> int:
    runner = BenchmarkRunner(SimpleMemoryAgent())
    run = runner.run(report_dir="reports")
    print(_format_summary(run.metrics))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
