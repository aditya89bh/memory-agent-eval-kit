# Benchmark Methodology

## Benchmark Philosophy

`memory-agent-eval-kit` treats memory as a product-critical behavior, not a convenience feature. The benchmark is designed to expose whether a memory-enabled agent can preserve useful context, update stale context, reject unsupported claims, and respect deletion or privacy constraints across realistic interaction patterns.

The suite favors deterministic, inspectable scenarios over opaque model-graded judgments. Each scenario is small enough to audit manually, but the full corpus spans enough categories to reveal regressions that single demo conversations miss.

## Evaluation Goals

The benchmark measures whether an agent can:

- Recall explicitly stored facts when recall is appropriate.
- Prefer corrected, recent, or authoritative memories over obsolete ones.
- Detect contradictions instead of flattening conflicting facts into one answer.
- Forget or suppress memories that are deleted, inactive, expired, or privacy-sensitive.
- Reason over temporal order, continuity, and multi-session context.
- Resist hallucinated, poisoned, noisy, or low-trust memory inputs.
- Maintain usable behavior across enterprise compliance and multi-agent memory scenarios.

## Scoring Principles

Scores are scenario-level and then aggregated into category and overall metrics.

- **Deterministic assertions first:** scenarios define expected answers, negative assertions, refusal expectations, and category-specific checks.
- **Pass/fail clarity:** a successful scenario returns the expected behavior without violating negative assertions.
- **Partial support where explicit:** scoring rules may allow partial credit only when a category evaluator defines it clearly.
- **Category transparency:** category scores are reported separately so high performance in one area cannot hide weak memory safety in another.
- **Latency visibility:** latency is reported alongside correctness because memory quality and retrieval cost both matter in production.
- **Regression usefulness:** scores are intended to compare the same agent across versions or configurations, not to overclaim universal capability.

## v0.6.0 Evidence Layers

The v0.6.0 release adds evidence beyond a single default benchmark score:

- **Adapter artifacts:** Mem0 and LangGraph benchmark reports are generated separately from the default run, with metadata documenting whether a live provider client or fallback adapter was used.
- **Comparison dashboards:** multiple agents can be viewed side-by-side with overall score, latency, hallucination rate, and false-recall rate.
- **Statistical analysis:** Wilson confidence intervals, bootstrap score intervals, and score-difference significance tests help distinguish noise from meaningful movement.
- **Performance evidence:** scale and profiling reports expose retrieval latency, CPU time, wall time, and peak memory usage.
- **Ecosystem evidence:** exchange packages, suite registries, and plugin entry points make third-party benchmark submissions reproducible and auditable.

## Benchmark Limitations

The benchmark does not prove that an agent is safe, truthful, or reliable in every deployment. Important limitations include:

- The default adapter is deterministic and intentionally simple; external LLM behavior may vary by model, prompt, and provider.
- Scenario wording is finite and cannot cover every real user phrasing.
- Some capabilities are tested through targeted examples rather than exhaustive adversarial search.
- Scores are sensitive to adapter implementation choices, retrieval policy, and memory normalization.
- The benchmark does not replace human review, red-team evaluation, privacy review, or production monitoring.

## Benchmark Assumptions

The benchmark assumes that:

- Memory events represent the information available to the agent before the query.
- Deleted or inactive memories should not influence answers unless a scenario explicitly says otherwise.
- More recent corrections generally supersede older facts when the scenario marks them as corrections or temporal updates.
- Agents should say they do not know when a scenario expects refusal or when no supported memory exists.
- Each scenario can be evaluated independently unless the category explicitly models continuity, synchronization, or multi-agent state.

## Interpretation of Scores

Use scores as evidence, not as a certification.

- **90-100%:** strong behavior on the covered corpus; still review weak categories and privacy-critical failures.
- **75-89%:** useful baseline with visible gaps; suitable for targeted iteration before deployment claims.
- **50-74%:** mixed behavior; likely fails important memory edge cases.
- **Below 50%:** poor benchmark fit or major adapter/scoring mismatch.

A high overall score should always be read with the category breakdown. For example, an agent can score well on recall while still failing forgetting, poisoning resistance, or compliance. For release decisions, treat privacy, deletion, hallucination, and contradiction failures as higher severity than ordinary recall misses.
