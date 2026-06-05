"""Dataset loading utilities."""

from __future__ import annotations

import json
from collections.abc import Iterable
from importlib.resources import files
from pathlib import Path

from memory_agent_eval_kit.models import BenchmarkScenario, Category, ScenarioStatus

DEFAULT_DATASET = "benchmark_scenarios.json"


class DatasetError(ValueError):
    """Raised when a benchmark dataset is malformed."""


def _load_json(path: Path | None = None) -> list[dict[str, object]]:
    if path is None:
        resource = files("memory_agent_eval_kit.datasets").joinpath(DEFAULT_DATASET)
        with resource.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    else:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    if not isinstance(payload, list):
        raise DatasetError("Dataset root must be a list of scenarios.")
    return [item for item in payload if isinstance(item, dict)]


def load_scenarios(
    path: Path | str | None = None,
    categories: Iterable[Category] | None = None,
    statuses: Iterable[ScenarioStatus] | None = None,
) -> list[BenchmarkScenario]:
    selected = set(categories) if categories is not None else None
    selected_statuses = set(statuses) if statuses is not None else None
    raw = _load_json(None if path is None else Path(path))
    scenarios = [BenchmarkScenario.from_dict(item) for item in raw]
    if selected is not None:
        scenarios = [scenario for scenario in scenarios if scenario.category in selected]
    if selected_statuses is not None:
        scenarios = [scenario for scenario in scenarios if scenario.status in selected_statuses]
    ids = [scenario.scenario_id for scenario in scenarios]
    if len(ids) != len(set(ids)):
        raise DatasetError("Scenario IDs must be unique.")
    return scenarios
