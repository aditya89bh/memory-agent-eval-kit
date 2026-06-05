"""Benchmark result exchange format for third-party submissions."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

EXCHANGE_SCHEMA_VERSION = "benchmark-result-exchange/v1"


@dataclass(frozen=True)
class BenchmarkExchangePackage:
    """Portable benchmark result package."""

    schema_version: str
    agent_name: str
    suite_name: str
    benchmark_version: str
    report: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def export_benchmark_results(
    report_path: Path,
    output_path: Path,
    *,
    agent_name: str,
    suite_name: str = "default",
    benchmark_version: str = "unknown",
) -> BenchmarkExchangePackage:
    """Export a benchmark report into the exchange format."""

    package = BenchmarkExchangePackage(
        schema_version=EXCHANGE_SCHEMA_VERSION,
        agent_name=agent_name,
        suite_name=suite_name,
        benchmark_version=benchmark_version,
        report=json.loads(report_path.read_text(encoding="utf-8")),
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(package.to_dict(), indent=2), encoding="utf-8")
    return package


def import_benchmark_results(exchange_path: Path) -> BenchmarkExchangePackage:
    """Load and validate an exchanged benchmark result package."""

    payload = json.loads(exchange_path.read_text(encoding="utf-8"))
    schema_version = payload.get("schema_version")
    if schema_version != EXCHANGE_SCHEMA_VERSION:
        raise ValueError(f"Unsupported exchange schema_version: {schema_version}")
    report = payload.get("report")
    if not isinstance(report, dict) or "metrics" not in report:
        raise ValueError("Exchange package must include a report with metrics")
    return BenchmarkExchangePackage(
        schema_version=schema_version,
        agent_name=str(payload.get("agent_name", "")),
        suite_name=str(payload.get("suite_name", "")),
        benchmark_version=str(payload.get("benchmark_version", "unknown")),
        report=report,
    )
