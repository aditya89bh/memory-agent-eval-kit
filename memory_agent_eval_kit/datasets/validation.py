"""Benchmark dataset validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, get_args

from memory_agent_eval_kit.datasets.loader import load_scenarios
from memory_agent_eval_kit.models import Category, Difficulty, ScenarioStatus

VALID_CATEGORIES = set(get_args(Category))
VALID_STATUSES = set(get_args(ScenarioStatus))
VALID_DIFFICULTIES = set(get_args(Difficulty))


@dataclass(frozen=True)
class DatasetValidationResult:
    """Validation outcome for a dataset."""

    valid: bool
    errors: list[str] = field(default_factory=list)
    scenario_count: int = 0


def validate_dataset(path: Path | str | None = None) -> DatasetValidationResult:
    """Validate scenario schema, duplicate IDs, and category consistency."""

    errors: list[str] = []
    try:
        scenarios = load_scenarios(path)
    except Exception as exc:  # noqa: BLE001 - validation should report all load failures
        return DatasetValidationResult(valid=False, errors=[str(exc)], scenario_count=0)

    seen: set[str] = set()
    for scenario in scenarios:
        if scenario.scenario_id in seen:
            errors.append(f"Duplicate scenario_id: {scenario.scenario_id}")
        seen.add(scenario.scenario_id)
        if scenario.category not in VALID_CATEGORIES:
            errors.append(f"Invalid category for {scenario.scenario_id}: {scenario.category}")
        if scenario.status not in VALID_STATUSES:
            errors.append(f"Invalid status for {scenario.scenario_id}: {scenario.status}")
        if scenario.difficulty not in VALID_DIFFICULTIES:
            errors.append(f"Invalid difficulty for {scenario.scenario_id}: {scenario.difficulty}")
        errors.extend(_schema_errors(scenario.to_dict()))
    return DatasetValidationResult(
        valid=not errors,
        errors=errors,
        scenario_count=len(scenarios),
    )


def _schema_errors(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    scenario_id = str(payload.get("scenario_id", "<unknown>"))
    required = ["scenario_id", "category", "query", "expected_answer", "events"]
    for field_name in required:
        if field_name not in payload:
            errors.append(f"{scenario_id}: missing {field_name}")
    status = str(payload.get("status", "active"))
    if status not in VALID_STATUSES:
        errors.append(f"{scenario_id}: status must be active or deprecated")
    if status == "deprecated" and not payload.get("deprecation_reason"):
        errors.append(f"{scenario_id}: deprecated scenarios need deprecation_reason")
    difficulty = str(payload.get("difficulty", "medium"))
    if difficulty not in VALID_DIFFICULTIES:
        errors.append(f"{scenario_id}: difficulty must be easy, medium, or hard")
    if not isinstance(payload.get("events", []), list):
        errors.append(f"{scenario_id}: events must be a list")
    if not isinstance(payload.get("negative_assertions", []), list):
        errors.append(f"{scenario_id}: negative_assertions must be a list")
    scoring = payload.get("scoring_rules", {})
    if not isinstance(scoring, dict):
        errors.append(f"{scenario_id}: scoring_rules must be an object")
    behavior = payload.get("expected_behavior", {})
    if not isinstance(behavior, dict):
        errors.append(f"{scenario_id}: expected_behavior must be an object")
    return errors
