"""Benchmark profiling utilities."""

from __future__ import annotations

import json
import time
import tracemalloc
from dataclasses import asdict, dataclass
from pathlib import Path

from memory_agent_eval_kit.adapters import MemoryAgentAdapter, SimpleMemoryAgent
from memory_agent_eval_kit.benchmarks.runner import BenchmarkRunner
from memory_agent_eval_kit.models import Category


@dataclass(frozen=True)
class BenchmarkProfile:
    """Resource profile for one benchmark run."""

    wall_time_ms: float
    cpu_time_ms: float
    peak_memory_kb: float
    avg_latency_ms: float
    p95_latency_ms: float
    scenario_count: int

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def profile_benchmark(
    *,
    categories: list[Category] | None = None,
    adapter: MemoryAgentAdapter | None = None,
    output_dir: Path | None = None,
) -> BenchmarkProfile:
    """Run a benchmark and capture wall time, CPU time, memory, and latency."""

    benchmark_adapter = adapter or SimpleMemoryAgent()
    tracemalloc.start()
    start_wall = time.perf_counter()
    start_cpu = time.process_time()
    run = BenchmarkRunner(benchmark_adapter).run(categories=categories, report_dir=None, seed=42)
    cpu_time_ms = (time.process_time() - start_cpu) * 1000
    wall_time_ms = (time.perf_counter() - start_wall) * 1000
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    profile = BenchmarkProfile(
        wall_time_ms=wall_time_ms,
        cpu_time_ms=cpu_time_ms,
        peak_memory_kb=peak_bytes / 1024,
        avg_latency_ms=run.metrics.latency_avg_ms,
        p95_latency_ms=run.metrics.latency_p95_ms,
        scenario_count=run.metrics.total_scenarios,
    )
    if output_dir is not None:
        write_profile_report(profile, output_dir)
    return profile


def write_profile_report(profile: BenchmarkProfile, output_dir: Path) -> list[Path]:
    """Write benchmark profile artifacts."""

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "profile.json"
    markdown_path = output_dir / "profile.md"
    json_path.write_text(json.dumps(profile.to_dict(), indent=2), encoding="utf-8")
    lines = [
        "# Benchmark Profile",
        "",
        f"- Wall time: {profile.wall_time_ms:.2f} ms",
        f"- CPU time: {profile.cpu_time_ms:.2f} ms",
        f"- Peak memory: {profile.peak_memory_kb:.2f} KiB",
        f"- Average scenario latency: {profile.avg_latency_ms:.2f} ms",
        f"- P95 scenario latency: {profile.p95_latency_ms:.2f} ms",
        f"- Scenario count: {profile.scenario_count}",
    ]
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return [json_path, markdown_path]
