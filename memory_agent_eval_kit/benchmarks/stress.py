"""Synthetic memory stress benchmark generation."""

from __future__ import annotations

from memory_agent_eval_kit.models import BenchmarkScenario, MemoryEvent

STRESS_SCALES = (10, 100, 1000)


def generate_stress_scenarios(scales: tuple[int, ...] = STRESS_SCALES) -> list[BenchmarkScenario]:
    """Generate deterministic scale scenarios for recall/latency degradation checks."""

    scenarios: list[BenchmarkScenario] = []
    for scale in scales:
        target = scale - 1
        events = [
            MemoryEvent(
                type="fact",
                memory_id=f"stress_{scale}_{index}",
                content=f"Stress memory item {index} has value value-{index}",
            )
            for index in range(scale)
        ]
        scenarios.append(
            BenchmarkScenario.from_dict(
                {
                    "scenario_id": f"stress_{scale:04d}",
                    "category": "stress",
                    "events": [event.to_memory() for event in events],
                    "query": f"What value belongs to stress memory item {target}?",
                    "expected_answer": f"value-{target}",
                    "expected_behavior": {
                        "answer": f"value-{target}",
                        "rationale": f"Recall target among {scale} stored memories.",
                    },
                    "scoring_rules": {"mode": "exact"},
                    "description": f"Synthetic recall stress test at {scale} memories.",
                    "memory_scale": scale,
                }
            )
        )
    return scenarios
