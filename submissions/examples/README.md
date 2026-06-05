# Benchmark Submission Examples

This directory contains minimal public submission examples.

- `valid_submission.json` shows the required top-level fields and a small set of per-scenario results.
- `invalid_submission.json` intentionally fails validation because the score is outside the `0..1` range and no scenario results are provided.

A submission is a JSON object with:

- `agent_name`: public agent or system name.
- `adapter_name`: adapter implementation used to run the benchmark.
- `suite_version`: benchmark dataset suite version, for example `v3`.
- `benchmark_score`: aggregate score between `0` and `1`.
- `scenario_count`: number of evaluated scenarios.
- `results`: non-empty list of scenario result objects.

Each result object must include:

- `scenario_id`
- `category`
- `score` between `0` and `1`

Validate submissions before publication:

```bash
python - <<'PY'
from pathlib import Path
from memory_agent_eval_kit.submissions import validate_submission

result = validate_submission(Path('submissions/examples/valid_submission.json'))
print(result.valid, result.errors)
PY
```
