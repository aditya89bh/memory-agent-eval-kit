# Metrics

`EvaluationResult` fields:

- `scenario_id`
- `category`
- `success`
- `score`
- `latency_ms`
- `details`

Aggregate metrics:

- `overall_score`
- `recall_accuracy`
- `contradiction_accuracy`
- `correction_accuracy`
- `forgetting_accuracy`
- `temporal_accuracy`
- `stale_memory_accuracy`
- `continuity_accuracy`
- `latency_avg_ms`
- `latency_p95_ms`
- `total_scenarios`

Scores are normalized from 0.0 to 1.0 and rendered as percentages in CLI and Markdown reports.


## v0.2.0 metrics

New metrics include hallucination rate, false recall rate, memory leak rate, temporal drift accuracy, contradiction resolution, ambiguity handling, poisoning resistance, stress recall accuracy, and latency degradation.
