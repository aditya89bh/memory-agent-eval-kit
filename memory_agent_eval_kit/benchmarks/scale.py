"""Large-scale memory benchmark helpers."""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from memory_agent_eval_kit.adapters import MemoryAgentAdapter, SimpleMemoryAgent

DEFAULT_MEMORY_SCALES = (100, 1_000, 10_000, 100_000)


@dataclass(frozen=True)
class MemoryScaleResult:
    """Result for one memory scale benchmark run."""

    memory_count: int
    add_ms: float
    query_ms: float
    success: bool
    answer: str

    def to_dict(self) -> dict[str, float | int | bool | str]:
        return asdict(self)


def run_memory_scale_benchmark(
    scales: tuple[int, ...] = DEFAULT_MEMORY_SCALES,
    *,
    output_dir: Path | None = None,
    adapter_factory: type[MemoryAgentAdapter] = SimpleMemoryAgent,
) -> list[MemoryScaleResult]:
    """Run recall checks after loading increasingly large memory sets."""

    results = [_run_scale(scale, adapter_factory()) for scale in scales]
    if output_dir is not None:
        write_memory_scale_report(results, output_dir)
    return results


def write_memory_scale_report(results: list[MemoryScaleResult], output_dir: Path) -> list[Path]:
    """Write JSON and Markdown artifacts for memory scale benchmark results."""

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "results.json"
    markdown_path = output_dir / "results.md"
    json_path.write_text(
        json.dumps([result.to_dict() for result in results], indent=2),
        encoding="utf-8",
    )
    lines = [
        "# Memory Scale Benchmark",
        "",
        "| Memories | Add ms | Query ms | Success |",
        "|---:|---:|---:|---:|",
    ]
    for result in results:
        lines.append(
            f"| {result.memory_count} | {result.add_ms:.2f} | "
            f"{result.query_ms:.2f} | {result.success} |"
        )
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return [json_path, markdown_path]


def _run_scale(memory_count: int, adapter: MemoryAgentAdapter) -> MemoryScaleResult:
    target = f"scale-target-{memory_count}"
    start_add = time.perf_counter()
    for index in range(memory_count - 1):
        adapter.add_memory(
            {
                "memory_id": f"scale_{memory_count}_{index}",
                "content": f"Distractor memory {index} for scale benchmark",
            }
        )
    adapter.add_memory(
        {
            "memory_id": f"scale_{memory_count}_target",
            "content": f"Large scale benchmark target is {target}",
        }
    )
    add_ms = (time.perf_counter() - start_add) * 1000
    start_query = time.perf_counter()
    answer = adapter.query("What is the large scale benchmark target?")
    query_ms = (time.perf_counter() - start_query) * 1000
    return MemoryScaleResult(
        memory_count=memory_count,
        add_ms=add_ms,
        query_ms=query_ms,
        success=target in answer,
        answer=answer,
    )
