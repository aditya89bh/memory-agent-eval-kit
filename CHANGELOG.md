# Changelog

## v0.4.0 - 2026-06-05

- Added benchmark authority suites: long-horizon, noisy memory, preference evolution, relationship memory, and hierarchical memory.
- Added enterprise privacy/compliance suites and aggregate compliance metrics.
- Added multi-agent memory suites for shared stores, synchronization, disagreement, conflict resolution, and collaborative recall.
- Added benchmark suite version metadata, dataset changelog generation, scenario deprecation support, version comparison, and historical archives.
- Added optional Mem0 and LangGraph adapters with graceful fallback behavior.
- Added adapter template generation via `memory-eval create-adapter my_adapter`.
- Added public benchmark submission format and validation.
- Regenerated reports, leaderboard, and visualization assets for the v0.4.0 benchmark suite.

## v0.3.0 - 2026-06-05

- Expanded the benchmark corpus and added dataset validation via `memory-eval validate`.
- Added memory leakage, hallucinated recall, timeline reasoning, and memory drift benchmark suites.
- Expanded memory poisoning coverage with malicious updates, conflicting updates, and source-trust scenarios.
- Added reproducible benchmark execution with `memory-eval benchmark --seed`.
- Added benchmark comparison reports with score deltas, category deltas, and regression detection.
- Added `memory-eval benchmark --fail-under` for CI regression gates.
- Improved leaderboard output with overall, category, and latency ranks.
- Added dependency-free SVG visualization assets under `assets/benchmark_visuals/`.
- Refreshed documentation, reports, leaderboards, and release artifacts.

## v0.2.0 - 2026-06-05

- Expanded scenario schema with sessions, timestamps, behavior expectations, scoring rules, and negative assertions.
- Added hallucination, stress, temporal drift, adversarial contradiction, and memory poisoning suites.
- Strengthened forgetting with delayed leak checks and memory leak metrics.
- Added semantic scoring utilities, suite configuration, leaderboards, additional adapter examples, and richer reports.

## v0.1.0 - 2026-06-05

- Initial release with 70 benchmark scenarios, adapter interface, CLI, reports, docs, CI, and example in-memory agent.
