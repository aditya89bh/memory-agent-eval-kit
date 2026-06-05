# Scenario Authoring Guide

Good benchmark scenarios are small, auditable tests of one memory behavior. They should help contributors explain why an agent passed or failed without needing to inspect hidden prompts or model internals.

## Good Benchmark Design

A strong scenario has:

- **One primary capability:** test recall, correction, forgetting, poisoning resistance, or another specific behavior without mixing unrelated failures.
- **Clear memory setup:** include only the memory events required to answer the query.
- **Specific expected behavior:** use concrete expected answers, refusal expectations, and negative assertions.
- **Stable wording:** avoid phrasing that depends on current events, private context, or ambiguous real-world facts.
- **Reviewable rationale:** descriptions should explain why the case matters.
- **Deterministic scoring:** the expected answer and negative assertions should be machine-checkable.

## Common Mistakes

Avoid these patterns:

- **Testing multiple behaviors at once:** a scenario that mixes deletion, temporal ordering, and poisoning may be hard to diagnose.
- **Over-broad expected answers:** `the correct project` is less useful than `Project Atlas`.
- **Missing negative assertions:** forgetting and hallucination tests should name what must not be returned.
- **Private or identifying data:** use synthetic names, emails, and IDs.
- **Unclear correction semantics:** if one fact supersedes another, mark it with `type: "correction"` and `supersedes` when appropriate.
- **Ambiguous timestamps:** temporal scenarios should use explicit ISO-like timestamps.
- **Brittle natural language:** do not require exact phrasing when a category evaluator is intended to check semantic content.

## Difficulty Guidelines

Use difficulty to communicate expected challenge, not importance.

### Easy

Use `easy` when the scenario tests a direct, isolated behavior.

Examples:

- One stored fact and one direct recall query.
- One deleted memory and one query that should be refused.
- One simple correction where the superseding memory is explicit.

### Medium

Use `medium` when the scenario requires filtering, ordering, or simple conflict handling.

Examples:

- Multiple memories with one relevant answer.
- A current and previous preference that must be distinguished.
- A contradiction that should be surfaced rather than collapsed.
- A privacy-sensitive memory that must be classified before answering.

### Hard

Use `hard` when the scenario combines scale, adversarial pressure, multi-step reasoning, or multi-agent state.

Examples:

- Poisoned updates mixed with legitimate memories.
- Long-horizon recall with many distractors.
- Multi-agent synchronization or disagreement cases.
- Timeline reasoning requiring current, previous, and chronological answers.
- Compliance scenarios involving deletion, retention, and leakage risk.

## Expected Behavior Patterns

Prefer this richer structure when the answer requires more than a string match:

```json
"expected_behavior": {
  "answer": "I do not know that information.",
  "should_know": false,
  "should_refuse": true,
  "rationale": "The relevant memory was deleted and must not be revealed."
}
```

Use `negative_assertions` for stale or unsafe content:

```json
"negative_assertions": ["old@example.com", "previous address"]
```

## Scenario Review Questions

Before committing a scenario, ask:

1. What single capability does this test?
2. What would a false pass look like?
3. What would a false failure look like?
4. Are the memory events sufficient but minimal?
5. Is the difficulty label defensible?
6. Would this scenario still make sense a year from now?

## Release Discipline

Scenario authoring changes should remain backward compatible. If a schema field is added, provide a default path for older scenarios, update validation, update reports when useful, and add tests for the new behavior.
