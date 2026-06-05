"""Historical benchmark archive support."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class BenchmarkArchiveRecord:
    """Metadata for an archived benchmark result."""

    archive_path: str
    suite_version: str
    created_at: str
    scenario_count: int
    overall_score: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def archive_benchmark_report(
    report: dict[str, Any] | str | Path,
    archive_dir: str | Path = "archives",
    *,
    suite_version: str = "v3",
    created_at: datetime | None = None,
) -> BenchmarkArchiveRecord:
    """Store a benchmark report snapshot under ``archives/``.

    The archive is deterministic for a supplied ``created_at`` and contains both
    benchmark payload and archive metadata for later historical analysis.
    """

    payload = _load_report(report)
    timestamp = (created_at or datetime.now(tz=UTC)).astimezone(UTC)
    stamp = timestamp.strftime("%Y%m%dT%H%M%SZ")
    destination_dir = Path(archive_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    archive_path = destination_dir / f"benchmark-{suite_version}-{stamp}.json"
    metrics = payload.get("metrics", {}) if isinstance(payload.get("metrics", {}), dict) else {}
    record = BenchmarkArchiveRecord(
        archive_path=str(archive_path),
        suite_version=suite_version,
        created_at=timestamp.isoformat().replace("+00:00", "Z"),
        scenario_count=int(metrics.get("total_scenarios", 0)),
        overall_score=float(metrics.get("overall_score", 0.0)),
    )
    archive_payload = {"archive": record.to_dict(), "report": payload}
    archive_path.write_text(json.dumps(archive_payload, indent=2), encoding="utf-8")
    return record


def list_benchmark_archives(archive_dir: str | Path = "archives") -> list[Path]:
    """Return benchmark archive files sorted by name."""

    path = Path(archive_dir)
    if not path.exists():
        return []
    return sorted(path.glob("benchmark-*.json"))


def _load_report(report: dict[str, Any] | str | Path) -> dict[str, Any]:
    if isinstance(report, dict):
        return report
    payload = json.loads(Path(report).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Benchmark archive input must be a JSON object")
    return payload
