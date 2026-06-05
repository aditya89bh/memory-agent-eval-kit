"""Validation for public benchmark result submissions."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REQUIRED_SUBMISSION_FIELDS = {
    "agent_name",
    "adapter_name",
    "suite_version",
    "benchmark_score",
    "scenario_count",
    "results",
}


@dataclass(frozen=True)
class SubmissionValidationResult:
    """Validation result for an external benchmark submission."""

    valid: bool
    errors: list[str] = field(default_factory=list)


def validate_submission(submission: dict[str, Any] | str | Path) -> SubmissionValidationResult:
    """Validate a public benchmark submission before acceptance."""

    payload = _load_submission(submission)
    errors: list[str] = []
    missing = sorted(REQUIRED_SUBMISSION_FIELDS - set(payload))
    errors.extend(f"Missing required field: {field_name}" for field_name in missing)
    if "benchmark_score" in payload and not _score_valid(payload["benchmark_score"]):
        errors.append("benchmark_score must be a number between 0 and 1")
    if "scenario_count" in payload and not _positive_int(payload["scenario_count"]):
        errors.append("scenario_count must be a positive integer")
    if "results" in payload:
        errors.extend(_result_errors(payload["results"]))
    for text_field in ("agent_name", "adapter_name", "suite_version"):
        if text_field in payload and not str(payload[text_field]).strip():
            errors.append(f"{text_field} must be non-empty")
    return SubmissionValidationResult(valid=not errors, errors=errors)


def _load_submission(submission: dict[str, Any] | str | Path) -> dict[str, Any]:
    if isinstance(submission, dict):
        return submission
    payload = json.loads(Path(submission).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Submission must be a JSON object")
    return payload


def _score_valid(value: object) -> bool:
    if not isinstance(value, int | float):
        return False
    return 0.0 <= float(value) <= 1.0


def _positive_int(value: object) -> bool:
    return isinstance(value, int) and value > 0


def _result_errors(results: object) -> list[str]:
    if not isinstance(results, list) or not results:
        return ["results must be a non-empty list"]
    errors: list[str] = []
    for index, item in enumerate(results):
        if not isinstance(item, dict):
            errors.append(f"results[{index}] must be an object")
            continue
        for field_name in ("scenario_id", "category", "score"):
            if field_name not in item:
                errors.append(f"results[{index}] missing {field_name}")
        if "score" in item and not _score_valid(item["score"]):
            errors.append(f"results[{index}].score must be between 0 and 1")
    return errors
