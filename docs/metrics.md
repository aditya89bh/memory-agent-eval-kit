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
- `hallucination_accuracy`
- `hallucination_rate`
- `false_recall_rate`
- `memory_leak_rate`
- `leak_rate`
- `delayed_leak_rate`
- `hallucinated_recall_accuracy`
- `timeline_reasoning_accuracy`
- `drift_accuracy`
- `update_accuracy`
- `temporal_drift_accuracy`
- `contradiction_resolution`
- `ambiguity_handling`
- `poisoning_resistance`
- `stress_recall_accuracy`
- `latency_degradation_ms`
- `latency_avg_ms`
- `latency_p95_ms`
- `total_scenarios`

Scores are normalized from 0.0 to 1.0 and rendered as percentages in CLI and Markdown reports.

## Comparison and regression metrics

`compare_results()` compares two JSON reports and returns:

- overall score delta
- category score deltas
- regression category names
- a boolean regression flag

The CLI regression gate exits non-zero when the overall score is below a threshold:

```bash
memory-eval benchmark --fail-under 90
```

## Leaderboard ranks

Leaderboards include:

- `overall_rank`: rank by overall score, descending
- `category_rank`: rank by mean category score, descending
- `latency_rank`: rank by average latency, ascending
