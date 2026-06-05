# Memory Agent Benchmark Results

## Summary

- Overall Score: 93%
- Total Scenarios: 253
- Average Latency: 0.02 ms
- P95 Latency: 0.04 ms
- Compliance Score: 100%
- Deletion Score: 100%
- Retention Score: 100%
- Privacy Score: 100%

## Confidence Metrics

- Overall 95% CI: 87% to 94%
- Overall estimate: 91%
- Method: Wilson score interval over scenario pass/fail outcomes.

## Category Breakdown

| Category | Pass | Fail | Score | 95% CI | Avg Latency ms |
|---|---:|---:|---:|---:|---:|
| adversarial_contradiction | 6 | 0 | 100% | 61%-100% | 0.02 |
| agent_disagreement | 3 | 0 | 100% | 44%-100% | 0.03 |
| collaborative_memory | 3 | 0 | 100% | 44%-100% | 0.05 |
| conflict_resolution | 3 | 0 | 100% | 44%-100% | 0.02 |
| continuity | 10 | 10 | 50% | 30%-70% | 0.01 |
| contradiction | 20 | 0 | 100% | 84%-100% | 0.02 |
| correction | 20 | 0 | 100% | 84%-100% | 0.02 |
| forgetting | 20 | 0 | 100% | 84%-100% | 0.02 |
| gdpr_forgetting | 3 | 0 | 100% | 44%-100% | 0.01 |
| hallucinated_recall | 8 | 0 | 100% | 68%-100% | 0.01 |
| hallucination | 10 | 0 | 100% | 72%-100% | 0.01 |
| hierarchical_memory | 3 | 0 | 100% | 44%-100% | 0.02 |
| long_horizon | 3 | 0 | 100% | 44%-100% | 0.35 |
| memory_drift | 5 | 0 | 100% | 57%-100% | 0.02 |
| memory_leakage | 5 | 0 | 100% | 57%-100% | 0.02 |
| memory_poisoning | 16 | 0 | 100% | 81%-100% | 0.02 |
| memory_synchronization | 3 | 0 | 100% | 44%-100% | 0.02 |
| noisy_memory | 5 | 0 | 100% | 57%-100% | 0.08 |
| pii_deletion | 3 | 0 | 100% | 44%-100% | 0.01 |
| preference_evolution | 6 | 0 | 100% | 61%-100% | 0.02 |
| recall | 20 | 0 | 100% | 84%-100% | 0.02 |
| relationship_memory | 4 | 0 | 100% | 51%-100% | 0.02 |
| retention_policy | 3 | 0 | 100% | 44%-100% | 0.01 |
| sensitive_classification | 5 | 0 | 100% | 57%-100% | 0.02 |
| shared_memory | 3 | 0 | 100% | 44%-100% | 0.02 |
| stale_memory | 9 | 11 | 72% | 26%-66% | 0.01 |
| temporal | 19 | 1 | 95% | 76%-99% | 0.03 |
| temporal_drift | 10 | 0 | 100% | 72%-100% | 0.02 |
| timeline_reasoning | 3 | 0 | 100% | 44%-100% | 0.03 |

## Difficulty Breakdown

| Difficulty | Pass | Fail | Score | Avg Latency ms |
|---|---:|---:|---:|---:|
| easy | 0 | 0 | 0% | 0.00 |
| medium | 231 | 22 | 93% | 0.02 |
| hard | 0 | 0 | 0% | 0.00 |

## Strongest Categories

- memory_drift: 100%
- memory_poisoning: 100%
- recall: 100%

## Weakest Categories

- continuity: 50%
- stale_memory: 72%
- temporal: 95%

## Pass/Fail Table

| Scenario | Category | Difficulty | Result | Score | Latency ms |
|---|---|---|---:|---:|---:|
| temporal_011 | temporal | medium | PASS | 1.00 | 0.05 |
| memory_drift_001 | memory_drift | medium | PASS | 1.00 | 0.02 |
| memory_poisoning_014 | memory_poisoning | medium | PASS | 1.00 | 0.02 |
| recall_010 | recall | medium | PASS | 1.00 | 0.02 |
| correction_015 | correction | medium | PASS | 1.00 | 0.02 |
| correction_014 | correction | medium | PASS | 1.00 | 0.02 |
| memory_poisoning_007 | memory_poisoning | medium | PASS | 1.00 | 0.02 |
| recall_011 | recall | medium | PASS | 1.00 | 0.02 |
| pii_deletion_001 | pii_deletion | medium | PASS | 1.00 | 0.01 |
| temporal_005 | temporal | medium | PASS | 1.00 | 0.03 |
| hallucination_003 | hallucination | medium | PASS | 1.00 | 0.01 |
| agent_disagreement_003 | agent_disagreement | medium | PASS | 1.00 | 0.04 |
| noisy_memory_005 | noisy_memory | medium | PASS | 1.00 | 0.09 |
| recall_004 | recall | medium | PASS | 1.00 | 0.02 |
| continuity_015 | continuity | medium | FAIL | 0.00 | 0.01 |
| long_horizon_010 | long_horizon | medium | PASS | 1.00 | 0.08 |
| continuity_019 | continuity | medium | FAIL | 0.00 | 0.01 |
| continuity_001 | continuity | medium | PASS | 1.00 | 0.02 |
| memory_leakage_001 | memory_leakage | medium | PASS | 1.00 | 0.02 |
| preference_evolution_001_previous | preference_evolution | medium | PASS | 1.00 | 0.02 |
| recall_017 | recall | medium | PASS | 1.00 | 0.02 |
| contradiction_012 | contradiction | medium | PASS | 1.00 | 0.02 |
| forgetting_012 | forgetting | medium | PASS | 1.00 | 0.02 |
| hierarchical_memory_001 | hierarchical_memory | medium | PASS | 1.00 | 0.02 |
| stale_memory_002 | stale_memory | medium | PASS | 1.00 | 0.01 |
| temporal_006 | temporal | medium | PASS | 1.00 | 0.02 |
| correction_010 | correction | medium | PASS | 1.00 | 0.02 |
| pii_deletion_003 | pii_deletion | medium | PASS | 1.00 | 0.01 |
| hallucinated_recall_001 | hallucinated_recall | medium | PASS | 1.00 | 0.01 |
| preference_evolution_001_current | preference_evolution | medium | PASS | 1.00 | 0.03 |
| hallucination_004 | hallucination | medium | PASS | 1.00 | 0.01 |
| correction_002 | correction | medium | PASS | 1.00 | 0.02 |
| memory_poisoning_013 | memory_poisoning | medium | PASS | 1.00 | 0.01 |
| hallucinated_recall_007 | hallucinated_recall | medium | PASS | 1.00 | 0.01 |
| contradiction_006 | contradiction | medium | PASS | 1.00 | 0.03 |
| continuity_006 | continuity | medium | PASS | 1.00 | 0.02 |
| continuity_002 | continuity | medium | PASS | 1.00 | 0.02 |
| temporal_drift_2_previous | temporal_drift | medium | PASS | 1.00 | 0.02 |
| collaborative_memory_002 | collaborative_memory | medium | PASS | 1.00 | 0.05 |
| memory_poisoning_016 | memory_poisoning | medium | PASS | 1.00 | 0.02 |
| hallucination_010 | hallucination | medium | PASS | 1.00 | 0.01 |
| hallucination_009 | hallucination | medium | PASS | 1.00 | 0.01 |
| contradiction_003 | contradiction | medium | PASS | 1.00 | 0.02 |
| retention_policy_001 | retention_policy | medium | PASS | 1.00 | 0.02 |
| temporal_drift_2_timeline | temporal_drift | medium | PASS | 1.00 | 0.03 |
| correction_008 | correction | medium | PASS | 1.00 | 0.02 |
| sensitive_classification_005 | sensitive_classification | medium | PASS | 1.00 | 0.02 |
| adversarial_contradiction_001 | adversarial_contradiction | medium | PASS | 1.00 | 0.02 |
| temporal_015 | temporal | medium | PASS | 1.00 | 0.03 |
| forgetting_015 | forgetting | medium | PASS | 1.00 | 0.03 |
| correction_019 | correction | medium | PASS | 1.00 | 0.02 |
| continuity_012 | continuity | medium | FAIL | 0.00 | 0.01 |
| temporal_003 | temporal | medium | PASS | 1.00 | 0.03 |
| memory_poisoning_006 | memory_poisoning | medium | PASS | 1.00 | 0.02 |
| relationship_memory_003 | relationship_memory | medium | PASS | 1.00 | 0.02 |
| contradiction_014 | contradiction | medium | PASS | 1.00 | 0.02 |
| memory_poisoning_005 | memory_poisoning | medium | PASS | 1.00 | 0.01 |
| contradiction_013 | contradiction | medium | PASS | 1.00 | 0.02 |
| recall_005 | recall | medium | PASS | 1.00 | 0.02 |
| stale_memory_003 | stale_memory | medium | PASS | 1.00 | 0.01 |
| timeline_reasoning_003 | timeline_reasoning | medium | PASS | 1.00 | 0.04 |
| stale_memory_017 | stale_memory | medium | FAIL | 0.50 | 0.01 |
| recall_006 | recall | medium | PASS | 1.00 | 0.02 |
| contradiction_001 | contradiction | medium | PASS | 1.00 | 0.02 |
| continuity_007 | continuity | medium | PASS | 1.00 | 0.02 |
| sensitive_classification_002 | sensitive_classification | medium | PASS | 1.00 | 0.02 |
| forgetting_001 | forgetting | medium | PASS | 1.00 | 0.02 |
| preference_evolution_003_previous | preference_evolution | medium | PASS | 1.00 | 0.02 |
| temporal_007 | temporal | medium | PASS | 1.00 | 0.02 |
| memory_poisoning_001 | memory_poisoning | medium | PASS | 1.00 | 0.01 |
| recall_003 | recall | medium | PASS | 1.00 | 0.02 |
| hallucinated_recall_005 | hallucinated_recall | medium | PASS | 1.00 | 0.01 |
| stale_memory_018 | stale_memory | medium | FAIL | 0.50 | 0.01 |
| continuity_016 | continuity | medium | FAIL | 0.00 | 0.01 |
| forgetting_013 | forgetting | medium | PASS | 1.00 | 0.02 |
| memory_poisoning_011 | memory_poisoning | medium | PASS | 1.00 | 0.02 |
| recall_015 | recall | medium | PASS | 1.00 | 0.01 |
| temporal_008 | temporal | medium | PASS | 1.00 | 0.02 |
| correction_012 | correction | medium | PASS | 1.00 | 0.01 |
| memory_synchronization_002 | memory_synchronization | medium | PASS | 1.00 | 0.02 |
| hallucination_008 | hallucination | medium | PASS | 1.00 | 0.01 |
| long_horizon_050 | long_horizon | medium | PASS | 1.00 | 0.33 |
| temporal_drift_1_previous | temporal_drift | medium | PASS | 1.00 | 0.02 |
| forgetting_009 | forgetting | medium | PASS | 1.00 | 0.02 |
| correction_011 | correction | medium | PASS | 1.00 | 0.02 |
| contradiction_004 | contradiction | medium | PASS | 1.00 | 0.02 |
| memory_poisoning_012 | memory_poisoning | medium | PASS | 1.00 | 0.01 |
| shared_memory_001 | shared_memory | medium | PASS | 1.00 | 0.02 |
| continuity_005 | continuity | medium | PASS | 1.00 | 0.02 |
| forgetting_004 | forgetting | medium | PASS | 1.00 | 0.02 |
| recall_001 | recall | medium | PASS | 1.00 | 0.02 |
| temporal_020 | temporal | medium | PASS | 1.00 | 0.03 |
| contradiction_020 | contradiction | medium | PASS | 1.00 | 0.02 |
| preference_evolution_002_current | preference_evolution | medium | PASS | 1.00 | 0.03 |
| forgetting_008 | forgetting | medium | PASS | 1.00 | 0.02 |
| recall_014 | recall | medium | PASS | 1.00 | 0.02 |
| preference_evolution_002_previous | preference_evolution | medium | PASS | 1.00 | 0.02 |
| temporal_drift_1_timeline | temporal_drift | medium | PASS | 1.00 | 0.03 |
| memory_poisoning_004 | memory_poisoning | medium | PASS | 1.00 | 0.02 |
| forgetting_005 | forgetting | medium | PASS | 1.00 | 0.02 |
| correction_016 | correction | medium | PASS | 1.00 | 0.02 |
| temporal_016 | temporal | medium | PASS | 1.00 | 0.02 |
| recall_016 | recall | medium | PASS | 1.00 | 0.01 |
| correction_013 | correction | medium | PASS | 1.00 | 0.01 |
| forgetting_011 | forgetting | medium | PASS | 1.00 | 0.02 |
| forgetting_019 | forgetting | medium | PASS | 1.00 | 0.02 |
| preference_evolution_003_current | preference_evolution | medium | PASS | 1.00 | 0.03 |
| conflict_resolution_002 | conflict_resolution | medium | PASS | 1.00 | 0.02 |
| forgetting_003 | forgetting | medium | PASS | 1.00 | 0.02 |
| forgetting_014 | forgetting | medium | PASS | 1.00 | 0.02 |
| memory_poisoning_010 | memory_poisoning | medium | PASS | 1.00 | 0.01 |
| contradiction_016 | contradiction | medium | PASS | 1.00 | 0.02 |
| temporal_009 | temporal | medium | PASS | 1.00 | 0.02 |
| hallucinated_recall_002 | hallucinated_recall | medium | PASS | 1.00 | 0.01 |
| temporal_019 | temporal | medium | PASS | 1.00 | 0.02 |
| hallucination_007 | hallucination | medium | PASS | 1.00 | 0.01 |
| agent_disagreement_001 | agent_disagreement | medium | PASS | 1.00 | 0.03 |
| noisy_memory_004 | noisy_memory | medium | PASS | 1.00 | 0.08 |
| hierarchical_memory_002 | hierarchical_memory | medium | PASS | 1.00 | 0.02 |
| temporal_drift_010 | temporal_drift | medium | PASS | 1.00 | 0.02 |
| stale_memory_014 | stale_memory | medium | FAIL | 0.50 | 0.01 |
| contradiction_010 | contradiction | medium | PASS | 1.00 | 0.02 |
| relationship_memory_002 | relationship_memory | medium | PASS | 1.00 | 0.02 |
| contradiction_011 | contradiction | medium | PASS | 1.00 | 0.02 |
| shared_memory_003 | shared_memory | medium | PASS | 1.00 | 0.02 |
| timeline_reasoning_002 | timeline_reasoning | medium | PASS | 1.00 | 0.03 |
| hierarchical_memory_003 | hierarchical_memory | medium | PASS | 1.00 | 0.02 |
| correction_017 | correction | medium | PASS | 1.00 | 0.02 |
| forgetting_016 | forgetting | medium | PASS | 1.00 | 0.02 |
| stale_memory_013 | stale_memory | medium | FAIL | 0.50 | 0.01 |
| hallucinated_recall_004 | hallucinated_recall | medium | PASS | 1.00 | 0.01 |
| temporal_017 | temporal | medium | PASS | 1.00 | 0.02 |
| recall_020 | recall | medium | PASS | 1.00 | 0.02 |
| stale_memory_020 | stale_memory | medium | FAIL | 0.50 | 0.01 |
| continuity_004 | continuity | medium | PASS | 1.00 | 0.02 |
| agent_disagreement_002 | agent_disagreement | medium | PASS | 1.00 | 0.03 |
| memory_drift_005 | memory_drift | medium | PASS | 1.00 | 0.02 |
| forgetting_007 | forgetting | medium | PASS | 1.00 | 0.02 |
| memory_drift_002 | memory_drift | medium | PASS | 1.00 | 0.02 |
| recall_012 | recall | medium | PASS | 1.00 | 0.02 |
| correction_018 | correction | medium | PASS | 1.00 | 0.01 |
| gdpr_forgetting_001 | gdpr_forgetting | medium | PASS | 1.00 | 0.01 |
| pii_deletion_002 | pii_deletion | medium | PASS | 1.00 | 0.01 |
| stale_memory_005 | stale_memory | medium | PASS | 1.00 | 0.01 |
| contradiction_007 | contradiction | medium | PASS | 1.00 | 0.02 |
| collaborative_memory_003 | collaborative_memory | medium | PASS | 1.00 | 0.05 |
| recall_013 | recall | medium | PASS | 1.00 | 0.01 |
| temporal_drift_1_current | temporal_drift | medium | PASS | 1.00 | 0.02 |
| sensitive_classification_003 | sensitive_classification | medium | PASS | 1.00 | 0.02 |
| memory_leakage_002 | memory_leakage | medium | PASS | 1.00 | 0.02 |
| contradiction_005 | contradiction | medium | PASS | 1.00 | 0.03 |
| temporal_drift_2_current | temporal_drift | medium | PASS | 1.00 | 0.02 |
| relationship_memory_004 | relationship_memory | medium | PASS | 1.00 | 0.02 |
| temporal_013 | temporal | medium | PASS | 1.00 | 0.03 |
| continuity_010 | continuity | medium | PASS | 1.00 | 0.02 |
| memory_poisoning_008 | memory_poisoning | medium | PASS | 1.00 | 0.01 |
| contradiction_019 | contradiction | medium | PASS | 1.00 | 0.02 |
| continuity_018 | continuity | medium | FAIL | 0.00 | 0.01 |
| conflict_resolution_001 | conflict_resolution | medium | PASS | 1.00 | 0.02 |
| forgetting_017 | forgetting | medium | PASS | 1.00 | 0.02 |
| temporal_004 | temporal | medium | PASS | 1.00 | 0.02 |
| stale_memory_016 | stale_memory | medium | FAIL | 0.50 | 0.01 |
| contradiction_009 | contradiction | medium | PASS | 1.00 | 0.02 |
| continuity_009 | continuity | medium | PASS | 1.00 | 0.01 |
| stale_memory_004 | stale_memory | medium | PASS | 1.00 | 0.01 |
| adversarial_contradiction_002 | adversarial_contradiction | medium | PASS | 1.00 | 0.02 |
| adversarial_contradiction_006 | adversarial_contradiction | medium | PASS | 1.00 | 0.02 |
| temporal_002 | temporal | medium | PASS | 1.00 | 0.03 |
| adversarial_contradiction_005 | adversarial_contradiction | medium | PASS | 1.00 | 0.02 |
| continuity_013 | continuity | medium | FAIL | 0.00 | 0.01 |
| contradiction_017 | contradiction | medium | PASS | 1.00 | 0.02 |
| noisy_memory_003 | noisy_memory | medium | PASS | 1.00 | 0.08 |
| memory_poisoning_015 | memory_poisoning | medium | PASS | 1.00 | 0.02 |
| correction_006 | correction | medium | PASS | 1.00 | 0.01 |
| retention_policy_002 | retention_policy | medium | PASS | 1.00 | 0.01 |
| memory_synchronization_001 | memory_synchronization | medium | PASS | 1.00 | 0.02 |
| hallucination_005 | hallucination | medium | PASS | 1.00 | 0.01 |
| stale_memory_009 | stale_memory | medium | PASS | 1.00 | 0.01 |
| continuity_020 | continuity | medium | FAIL | 0.00 | 0.01 |
| long_horizon_100 | long_horizon | medium | PASS | 1.00 | 0.64 |
| contradiction_008 | contradiction | medium | PASS | 1.00 | 0.03 |
| memory_leakage_005 | memory_leakage | medium | PASS | 1.00 | 0.02 |
| temporal_010 | temporal | medium | PASS | 1.00 | 0.03 |
| temporal_018 | temporal | medium | PASS | 1.00 | 0.02 |
| adversarial_contradiction_004 | adversarial_contradiction | medium | PASS | 1.00 | 0.02 |
| stale_memory_019 | stale_memory | medium | FAIL | 0.50 | 0.01 |
| continuity_011 | continuity | medium | FAIL | 0.00 | 0.01 |
| hallucination_006 | hallucination | medium | PASS | 1.00 | 0.01 |
| temporal_012 | temporal | medium | PASS | 1.00 | 0.02 |
| correction_001 | correction | medium | PASS | 1.00 | 0.02 |
| memory_poisoning_002 | memory_poisoning | medium | PASS | 1.00 | 0.02 |
| forgetting_002 | forgetting | medium | PASS | 1.00 | 0.02 |
| forgetting_018 | forgetting | medium | PASS | 1.00 | 0.02 |
| contradiction_018 | contradiction | medium | PASS | 1.00 | 0.03 |
| hallucinated_recall_006 | hallucinated_recall | medium | PASS | 1.00 | 0.01 |
| contradiction_002 | contradiction | medium | PASS | 1.00 | 0.02 |
| continuity_008 | continuity | medium | PASS | 1.00 | 0.01 |
| gdpr_forgetting_003 | gdpr_forgetting | medium | PASS | 1.00 | 0.01 |
| temporal_drift_3_timeline | temporal_drift | medium | PASS | 1.00 | 0.03 |
| adversarial_contradiction_003 | adversarial_contradiction | medium | PASS | 1.00 | 0.03 |
| correction_005 | correction | medium | PASS | 1.00 | 0.01 |
| memory_poisoning_003 | memory_poisoning | medium | PASS | 1.00 | 0.02 |
| sensitive_classification_001 | sensitive_classification | medium | PASS | 1.00 | 0.02 |
| memory_synchronization_003 | memory_synchronization | medium | PASS | 1.00 | 0.02 |
| temporal_drift_3_current | temporal_drift | medium | PASS | 1.00 | 0.02 |
| memory_drift_004 | memory_drift | medium | PASS | 1.00 | 0.02 |
| retention_policy_003 | retention_policy | medium | PASS | 1.00 | 0.01 |
| forgetting_010 | forgetting | medium | PASS | 1.00 | 0.03 |
| relationship_memory_001 | relationship_memory | medium | PASS | 1.00 | 0.02 |
| temporal_drift_3_previous | temporal_drift | medium | PASS | 1.00 | 0.02 |
| sensitive_classification_004 | sensitive_classification | medium | PASS | 1.00 | 0.02 |
| memory_leakage_003 | memory_leakage | medium | PASS | 1.00 | 0.02 |
| temporal_001 | temporal | medium | PASS | 1.00 | 0.03 |
| noisy_memory_001 | noisy_memory | medium | PASS | 1.00 | 0.08 |
| memory_drift_003 | memory_drift | medium | PASS | 1.00 | 0.02 |
| recall_002 | recall | medium | PASS | 1.00 | 0.02 |
| noisy_memory_002 | noisy_memory | medium | PASS | 1.00 | 0.08 |
| hallucination_002 | hallucination | medium | PASS | 1.00 | 0.01 |
| stale_memory_011 | stale_memory | medium | FAIL | 0.50 | 0.01 |
| contradiction_015 | contradiction | medium | PASS | 1.00 | 0.02 |
| stale_memory_007 | stale_memory | medium | PASS | 1.00 | 0.01 |
| recall_018 | recall | medium | PASS | 1.00 | 0.02 |
| shared_memory_002 | shared_memory | medium | PASS | 1.00 | 0.02 |
| memory_leakage_004 | memory_leakage | medium | PASS | 1.00 | 0.02 |
| continuity_017 | continuity | medium | FAIL | 0.00 | 0.01 |
| hallucinated_recall_003 | hallucinated_recall | medium | PASS | 1.00 | 0.01 |
| stale_memory_001 | stale_memory | medium | PASS | 1.00 | 0.01 |
| temporal_014 | temporal | medium | FAIL | 0.00 | 0.03 |
| collaborative_memory_001 | collaborative_memory | medium | PASS | 1.00 | 0.05 |
| stale_memory_015 | stale_memory | medium | FAIL | 0.50 | 0.01 |
| correction_020 | correction | medium | PASS | 1.00 | 0.02 |
| stale_memory_010 | stale_memory | medium | PASS | 1.00 | 0.01 |
| stale_memory_006 | stale_memory | medium | FAIL | 0.50 | 0.01 |
| correction_004 | correction | medium | PASS | 1.00 | 0.02 |
| recall_008 | recall | medium | PASS | 1.00 | 0.02 |
| recall_009 | recall | medium | PASS | 1.00 | 0.01 |
| recall_019 | recall | medium | PASS | 1.00 | 0.02 |
| stale_memory_012 | stale_memory | medium | FAIL | 0.50 | 0.01 |
| correction_003 | correction | medium | PASS | 1.00 | 0.02 |
| forgetting_020 | forgetting | medium | PASS | 1.00 | 0.02 |
| gdpr_forgetting_002 | gdpr_forgetting | medium | PASS | 1.00 | 0.01 |
| conflict_resolution_003 | conflict_resolution | medium | PASS | 1.00 | 0.02 |
| memory_poisoning_009 | memory_poisoning | medium | PASS | 1.00 | 0.02 |
| correction_007 | correction | medium | PASS | 1.00 | 0.01 |
| hallucinated_recall_008 | hallucinated_recall | medium | PASS | 1.00 | 0.01 |
| forgetting_006 | forgetting | medium | PASS | 1.00 | 0.01 |
| stale_memory_008 | stale_memory | medium | PASS | 1.00 | 0.02 |
| continuity_003 | continuity | medium | PASS | 1.00 | 0.02 |
| hallucination_001 | hallucination | medium | PASS | 1.00 | 0.01 |
| timeline_reasoning_001 | timeline_reasoning | medium | PASS | 1.00 | 0.03 |
| recall_007 | recall | medium | PASS | 1.00 | 0.01 |
| correction_009 | correction | medium | PASS | 1.00 | 0.01 |
| continuity_014 | continuity | medium | FAIL | 0.00 | 0.01 |
