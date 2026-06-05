# Benchmark Design

Each scenario is a JSON object containing:

- `scenario_id`: stable identifier
- `category`: one of the seven benchmark categories
- `memory_events`: memory writes/deletes/corrections applied before the query
- `query`: user prompt sent to the agent
- `expected_answer`: substring expected in a successful answer
- `expected_absent`: optional substrings that must not appear

The default benchmark contains 70 scenarios, split evenly across recall, contradiction detection, correction handling, forgetting, temporal memory, stale memory handling, and continuity.

Scenario scoring is intentionally transparent: a result succeeds when the expected answer is present and forbidden stale/deleted strings are absent.
