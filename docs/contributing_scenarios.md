# Contributing Benchmark Scenarios

This guide explains how to add benchmark scenarios while keeping the corpus reproducible, reviewable, and backward compatible.

## Where Scenarios Live

Default scenarios live in:

```text
memory_agent_eval_kit/datasets/benchmark_scenarios.json
```

A scenario is a JSON object with a stable `scenario_id`, a supported `category`, memory setup events, a query, and expected behavior.

## Minimal Scenario Shape

```json
{
  "scenario_id": "recall_021",
  "category": "recall",
  "difficulty": "easy",
  "memory_events": [
    {
      "type": "fact",
      "memory_id": "recall_021_memory",
      "content": "Preferred simulator is Gazebo"
    }
  ],
  "query": "What simulator do I prefer?",
  "expected_answer": "Gazebo",
  "description": "Recall a stored simulator preference.",
  "suite_version": "v3"
}
```

## Required Fields

- `scenario_id`: unique, stable identifier. Prefer `<category>_<number>`.
- `category`: one of the supported benchmark categories.
- `difficulty`: `easy`, `medium`, or `hard`. Omitted scenarios default to `medium` for backward compatibility.
- `memory_events` or `events`: list of memory operations available before the query.
- `query`: user-facing benchmark prompt.
- `expected_answer`: canonical answer or key phrase.

## Optional Fields

- `expected_behavior`: richer machine-checkable behavior, including refusal expectations and rationale.
- `negative_assertions`: strings that must not appear in the answer.
- `scoring_rules`: evaluator-specific scoring controls.
- `sessions`: explicit session IDs for continuity or multi-agent scenarios.
- `timestamps`: explicit event timestamps for temporal scenarios.
- `status`: `active` or `deprecated`.
- `deprecation_reason`: required when `status` is `deprecated`.

## Adding a Scenario

1. Choose the narrowest category that matches the behavior being tested.
2. Pick a unique `scenario_id` and stable memory IDs.
3. Add only the memories needed for the behavior under test.
4. Include `difficulty` based on the guidelines in `docs/scenario_authoring.md`.
5. Run dataset validation.
6. Run the relevant category benchmark.
7. Run the full validation gate before committing.

## Validation

Run:

```bash
memory-eval validate
ruff check .
mypy memory_agent_eval_kit
pytest
```

For a targeted category check:

```bash
memory-eval benchmark --category recall --seed 42
```

## Testing Expectations

Scenario changes should preserve existing tests and benchmark determinism. Add or update tests when you introduce new schema behavior, evaluator behavior, report fields, or validation rules.

## Review Checklist

Before opening or merging a scenario change, confirm:

- The scenario has a unique ID.
- The category is supported.
- The expected answer is specific enough to score.
- Negative assertions cover likely unsafe leakage or stale recall.
- The difficulty label is justified.
- The scenario does not encode private, real user data.
- `memory-eval validate`, `ruff`, `mypy`, and `pytest` pass.
