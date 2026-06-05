# Benchmark Corpus Statistics

Generated from the default `memory_agent_eval_kit/datasets/benchmark_scenarios.json` corpus.

## Summary

- **Total scenarios:** 253
- **Dataset suite version:** v3
- **Active benchmark categories:** 29
- **Synthetic stress scenarios:** generated separately with `memory-eval benchmark --stress`

## Scenarios per Category

| Category | Scenarios | Distribution |
|---|---:|---:|
| recall | 20 | 7.9% |
| contradiction | 20 | 7.9% |
| correction | 20 | 7.9% |
| forgetting | 20 | 7.9% |
| temporal | 20 | 7.9% |
| stale_memory | 20 | 7.9% |
| continuity | 20 | 7.9% |
| memory_poisoning | 16 | 6.3% |
| hallucination | 10 | 4.0% |
| temporal_drift | 10 | 4.0% |
| hallucinated_recall | 8 | 3.2% |
| adversarial_contradiction | 6 | 2.4% |
| preference_evolution | 6 | 2.4% |
| memory_drift | 5 | 2.0% |
| memory_leakage | 5 | 2.0% |
| noisy_memory | 5 | 2.0% |
| sensitive_classification | 5 | 2.0% |
| relationship_memory | 4 | 1.6% |
| agent_disagreement | 3 | 1.2% |
| collaborative_memory | 3 | 1.2% |
| conflict_resolution | 3 | 1.2% |
| gdpr_forgetting | 3 | 1.2% |
| hierarchical_memory | 3 | 1.2% |
| long_horizon | 3 | 1.2% |
| memory_synchronization | 3 | 1.2% |
| pii_deletion | 3 | 1.2% |
| retention_policy | 3 | 1.2% |
| shared_memory | 3 | 1.2% |
| timeline_reasoning | 3 | 1.2% |

## Category Distribution

The corpus is intentionally weighted toward foundational memory behaviors first: recall, contradiction, correction, forgetting, temporal reasoning, stale-memory handling, and continuity each have 20 scenarios. The remaining categories broaden coverage into memory safety, privacy, compliance, long-horizon retrieval, adversarial updates, and multi-agent memory.

This distribution keeps the default benchmark practical to run in CI while still making weak safety and governance categories visible in per-category reports.

## Benchmark Growth over Releases

| Release | Corpus Scope | Scenario Count |
|---|---|---:|
| v0.1.0 | Initial core memory benchmark categories | 70+ |
| v0.2.0 | Expanded schema, reporting, and version-aware benchmark governance | 80+ |
| v0.3.0 | Adapter ecosystem and public benchmark submission support | 80+ |
| v0.4.0 | Authority corpus covering enterprise compliance, multi-agent memory, poisoning, drift, and long-horizon suites | 253 |
| v0.5.0 | Methodology, reproducibility, difficulty metadata, confidence reporting, and presentation hardening | 253 |
| v0.6.0 | Real-world adapter artifacts, comparison dashboards, statistical analysis, scale benchmarks, profiling, exchange format, registry, plugins, and onboarding notebook | 253 |

Scenario count can remain stable across authority-building releases when the release improves methodology, reporting quality, reproducibility, ecosystem integrations, performance evidence, and documentation rather than expanding the benchmark surface area.
