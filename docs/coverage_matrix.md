# Benchmark Coverage Matrix

This matrix summarizes what the default benchmark corpus exercises today and where future benchmark expansion can add more evidence. It is a coverage report, not a claim of exhaustive safety certification.

## Capabilities Tested

| Capability | Covered Categories | What the Benchmark Checks |
|---|---|---|
| recall | `recall`, `long_horizon`, `relationship_memory`, `hierarchical_memory` | Retrieval of stored facts, role facts, nested organizational facts, and recall under larger memory sets. |
| contradiction | `contradiction`, `adversarial_contradiction`, `agent_disagreement`, `conflict_resolution` | Detection of conflicting memories, ambiguous updates, multi-agent disagreement, and resolution behavior. |
| correction | `correction`, `memory_drift`, `preference_evolution`, `temporal_drift` | Superseding obsolete facts, tracking evolving preferences, and preserving current-vs-previous distinctions. |
| forgetting | `forgetting`, `pii_deletion`, `gdpr_forgetting`, `memory_leakage` | Deletion behavior, refusal to reveal removed facts, privacy deletion, and delayed leakage checks. |
| temporal reasoning | `temporal`, `timeline_reasoning`, `temporal_drift`, `stale_memory` | Recency, event ordering, outdated memory suppression, and timeline-sensitive answers. |
| poisoning | `memory_poisoning`, `noisy_memory`, `adversarial_contradiction` | Malicious or low-trust updates, distractor memories, contradictory injections, and retrieval robustness. |
| continuity | `continuity`, `shared_memory`, `memory_synchronization` | Multi-session recall, shared memory propagation, and synchronization consistency. |
| compliance | `pii_deletion`, `gdpr_forgetting`, `retention_policy`, `sensitive_classification` | PII deletion, GDPR-style forgetting, retention policy enforcement, and sensitive memory classification. |
| multi-agent memory | `shared_memory`, `memory_synchronization`, `agent_disagreement`, `conflict_resolution`, `collaborative_memory` | Shared state, propagation, disagreement detection, conflict handling, and collaborative recall. |
| hallucination resistance | `hallucination`, `hallucinated_recall` | Refusal to invent unsupported memories and avoidance of false recall. |
| latency and stress behavior | `stress`, `long_horizon`, synthetic stress suite | Latency visibility and recall behavior as memory volume increases. |

## Capabilities Not Yet Tested

The following areas are intentionally listed as future coverage candidates:

- Cross-lingual memory recall and correction.
- Multimodal memory inputs such as images, audio, and documents.
- Tool-mediated memory writes from calendars, email, files, or browsers.
- Multi-user permission boundaries beyond the current shared-memory scenarios.
- Long-running production drift across days or weeks of organic conversations.
- Embedding-index corruption, vector-store outages, and partial retrieval failures.
- Prompt-injection attacks delivered through external documents or web pages.
- Cost-aware retrieval strategies and memory compression quality.
- Human-in-the-loop approval workflows for sensitive memories.
- Domain-specific regulated workflows beyond general privacy and retention scenarios.

## How to Use This Matrix

Use the matrix to decide whether a benchmark result is relevant to your deployment. If your product depends on a capability listed as not yet tested, add targeted scenarios before using the overall score as release evidence. If your product is privacy-sensitive, inspect the compliance, forgetting, hallucination, and leakage categories directly rather than relying only on the aggregate score.
