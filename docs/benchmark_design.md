# Benchmark Design

Each scenario is a JSON object containing stable identifiers, category metadata, memory events, a query, scoring expectations, and optional negative assertions.

Core fields:

- `scenario_id`: stable identifier
- `category`: benchmark category
- `events` / `memory_events`: memory writes, deletes, corrections, and session events applied before the query
- `query`: user prompt sent to the agent
- `expected_answer`: substring expected in a successful answer
- `expected_behavior`: structured expectations such as refusal, ambiguity handling, or poisoning type
- `scoring_rules`: threshold and assertion behavior
- `negative_assertions`: substrings that must not appear

## v0.4.0 suites

The v0.4.0 corpus extends the v0.3.0 research toolkit into benchmark authority coverage. It includes long-horizon recall, noisy retrieval, preference evolution, relationship memory, hierarchical memory, enterprise deletion/retention/privacy compliance, and multi-agent shared memory, synchronization, disagreement, conflict resolution, and collaboration suites. Stress cases are generated programmatically rather than stored in the JSON dataset.

## Benchmark governance

Scenarios carry suite version metadata and active/deprecated status. Dataset changelog generation tracks added, removed, and modified scenarios. Version comparison reports compare score and category deltas across v1, v2, v3, and future suites. Historical benchmark snapshots can be archived under `archives/`.

Dataset validation checks schema shape, duplicate scenario IDs, supported categories, and category consistency. Run:

```bash
memory-eval validate
```

Scenario scoring is intentionally transparent: a result succeeds when the expected behavior is met and forbidden stale, deleted, poisoned, or hallucinated strings are absent.

## Reproducibility

`BenchmarkRunner` accepts a seed and the CLI exposes it as:

```bash
memory-eval benchmark --seed 42
```

The seed creates deterministic scenario ordering without changing scenario content or adapter behavior.
