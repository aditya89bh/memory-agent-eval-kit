# Benchmark Comparison Dashboard

| Rank | Agent | Overall | Scenarios | Hallucination Rate | False Recall Rate | Avg Latency ms | P95 Latency ms |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | SimpleMemoryAgent | 93.48% | 253 | 0.00% | 0.00% | 0.02 | 0.04 |
| 2 | Mem0Adapter (fallback) | 93.48% | 253 | 0.00% | 0.00% | 0.02 | 0.03 |
| 3 | LangGraphAdapter (fallback) | 93.48% | 253 | 0.00% | 0.00% | 0.02 | 0.03 |

## Category Scores

| Agent | adversarial_contradiction | agent_disagreement | collaborative_memory | conflict_resolution | continuity | contradiction | correction | forgetting | gdpr_forgetting | hallucinated_recall | hallucination | hierarchical_memory | long_horizon | memory_drift | memory_leakage | memory_poisoning | memory_synchronization | noisy_memory | pii_deletion | preference_evolution | recall | relationship_memory | retention_policy | sensitive_classification | shared_memory | stale_memory | temporal | temporal_drift | timeline_reasoning |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SimpleMemoryAgent | 100% | 100% | 100% | 100% | 50% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 72% | 95% | 100% | 100% |
| Mem0Adapter (fallback) | 100% | 100% | 100% | 100% | 50% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 72% | 95% | 100% | 100% |
| LangGraphAdapter (fallback) | 100% | 100% | 100% | 100% | 50% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 72% | 95% | 100% | 100% |
