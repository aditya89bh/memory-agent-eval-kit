# Changelog

## v0.6.0 - 2026-06-05

- Added Mem0 and LangGraph adapter benchmark artifacts with explicit fallback metadata when optional provider packages are not installed.
- Added benchmark comparison dashboard outputs for side-by-side agent analysis.
- Added confidence interval reporting, bootstrap resampling support, and statistical significance testing helpers.
- Added large-scale memory benchmark artifacts for 100, 1,000, 10,000, and 100,000 stored memories.
- Added profiling support for memory usage, CPU usage, and latency breakdowns.
- Added benchmark result exchange format for third-party submissions.
- Added benchmark registry and plugin system for external suites.
- Added 5-minute benchmark quickstart notebook.
- Regenerated reports, leaderboards, comparison assets, scale artifacts, and profiling artifacts for the v0.6.0 release.

## v0.5.0 - 2026-06-05

- Added benchmark methodology documentation and corpus statistics.
- Added benchmark difficulty classification, coverage reporting, confidence metrics, and reproducibility reporting.
- Added hallucination leaderboard outputs and benchmark submission examples.
- Added contributor onboarding, scenario authoring guidance, architecture diagram, and refreshed repository presentation.
- Regenerated release reports and leaderboard artifacts for the v0.5.0 authority-building release.

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
