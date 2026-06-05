"""Dataset changelog generation."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DatasetChangelog:
    """Added, removed, and modified scenario IDs between two datasets."""

    added: list[str]
    removed: list[str]
    modified: list[str]

    def to_dict(self) -> dict[str, list[str]]:
        return asdict(self)


def generate_dataset_changelog(
    before: Path | str | list[dict[str, Any]],
    after: Path | str | list[dict[str, Any]],
) -> DatasetChangelog:
    """Generate a scenario-level changelog between two dataset snapshots."""

    before_map = _scenario_map(before)
    after_map = _scenario_map(after)
    before_ids = set(before_map)
    after_ids = set(after_map)
    common = before_ids & after_ids
    return DatasetChangelog(
        added=sorted(after_ids - before_ids),
        removed=sorted(before_ids - after_ids),
        modified=sorted(
            scenario_id
            for scenario_id in common
            if _stable_json(before_map[scenario_id]) != _stable_json(after_map[scenario_id])
        ),
    )


def write_dataset_changelog(
    before: Path | str | list[dict[str, Any]],
    after: Path | str | list[dict[str, Any]],
    output_path: Path | str,
) -> DatasetChangelog:
    """Write a dataset changelog JSON document and return it."""

    changelog = generate_dataset_changelog(before, after)
    Path(output_path).write_text(json.dumps(changelog.to_dict(), indent=2), encoding="utf-8")
    return changelog


def _scenario_map(source: Path | str | list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    payload = _load(source)
    return {str(item["scenario_id"]): item for item in payload if "scenario_id" in item}


def _load(source: Path | str | list[dict[str, Any]]) -> list[dict[str, Any]]:
    if isinstance(source, list):
        return source
    payload = json.loads(Path(source).read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        raw = payload.get("scenarios", [])
    else:
        raw = payload
    if not isinstance(raw, list):
        raise ValueError("Dataset changelog input must contain a scenario list")
    return [item for item in raw if isinstance(item, dict)]


def _stable_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))
