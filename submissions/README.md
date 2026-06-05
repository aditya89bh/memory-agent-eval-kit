# Public Benchmark Submissions

External benchmark submissions should be JSON objects with:

- `agent_name`
- `adapter_name`
- `suite_version`
- `benchmark_score` between 0 and 1
- `scenario_count`
- `results`, a non-empty list of per-scenario objects containing `scenario_id`, `category`, and `score`

Validate submissions with `memory_agent_eval_kit.submissions.validate_submission` before accepting them into a public leaderboard.
