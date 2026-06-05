"""Typed domain models for benchmark scenarios."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, TypeAlias, cast

Category: TypeAlias = Literal[
    "recall",
    "contradiction",
    "correction",
    "forgetting",
    "temporal",
    "stale_memory",
    "continuity",
    "hallucination",
    "stress",
    "temporal_drift",
    "adversarial_contradiction",
    "memory_poisoning",
    "memory_leakage",
    "hallucinated_recall",
]


@dataclass(frozen=True)
class MemoryEvent:
    """A memory operation executed before a scenario query."""

    type: str
    content: str
    memory_id: str | None = None
    session_id: str | None = None
    timestamp: str | None = None
    active: bool = True
    supersedes: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MemoryEvent:
        known = {"type", "content", "memory_id", "session_id", "timestamp", "active", "supersedes"}
        metadata = {key: value for key, value in data.items() if key not in known}
        return cls(
            type=str(data["type"]),
            content=str(data["content"]),
            memory_id=None if data.get("memory_id") is None else str(data.get("memory_id")),
            session_id=None if data.get("session_id") is None else str(data.get("session_id")),
            timestamp=None if data.get("timestamp") is None else str(data.get("timestamp")),
            active=bool(data.get("active", True)),
            supersedes=None if data.get("supersedes") is None else str(data.get("supersedes")),
            metadata=metadata,
        )

    def to_memory(self) -> dict[str, Any]:
        memory: dict[str, Any] = {
            "type": self.type,
            "content": self.content,
            "active": self.active,
            **self.metadata,
        }
        if self.memory_id is not None:
            memory["memory_id"] = self.memory_id
        if self.session_id is not None:
            memory["session_id"] = self.session_id
        if self.timestamp is not None:
            memory["timestamp"] = self.timestamp
        if self.supersedes is not None:
            memory["supersedes"] = self.supersedes
        return memory


@dataclass(frozen=True)
class ExpectedBehavior:
    """Human-readable and machine-checkable expected behavior."""

    answer: str
    should_know: bool = True
    should_refuse: bool = False
    rationale: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_raw(cls, raw: object, fallback_answer: str) -> ExpectedBehavior:
        if raw is None:
            return cls(answer=fallback_answer)
        if isinstance(raw, str):
            return cls(answer=raw)
        if isinstance(raw, dict):
            known = {"answer", "should_know", "should_refuse", "rationale"}
            return cls(
                answer=str(raw.get("answer", fallback_answer)),
                should_know=bool(raw.get("should_know", True)),
                should_refuse=bool(raw.get("should_refuse", False)),
                rationale=str(raw.get("rationale", "")),
                metadata={key: value for key, value in raw.items() if key not in known},
            )
        return cls(answer=fallback_answer)

    def to_dict(self) -> dict[str, Any]:
        return {
            "answer": self.answer,
            "should_know": self.should_know,
            "should_refuse": self.should_refuse,
            "rationale": self.rationale,
            **self.metadata,
        }


@dataclass(frozen=True)
class ScoringRules:
    """Per-scenario scoring controls."""

    mode: str = "exact"
    threshold: float = 1.0
    require_all_assertions: bool = True
    allow_partial: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_raw(cls, raw: object) -> ScoringRules:
        if not isinstance(raw, dict):
            return cls()
        known = {"mode", "threshold", "require_all_assertions", "allow_partial"}
        return cls(
            mode=str(raw.get("mode", "exact")),
            threshold=float(raw.get("threshold", 1.0)),
            require_all_assertions=bool(raw.get("require_all_assertions", True)),
            allow_partial=bool(raw.get("allow_partial", False)),
            metadata={key: value for key, value in raw.items() if key not in known},
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "threshold": self.threshold,
            "require_all_assertions": self.require_all_assertions,
            "allow_partial": self.allow_partial,
            **self.metadata,
        }


@dataclass(frozen=True)
class BenchmarkScenario:
    """A single benchmark case.

    The model accepts both v0.1 fields (``memory_events``, ``expected_answer``,
    ``expected_absent``) and the richer v0.2 schema (``events``, ``sessions``,
    ``timestamps``, ``expected_behavior``, ``scoring_rules``,
    ``negative_assertions``).
    """

    scenario_id: str
    category: Category
    memory_events: list[MemoryEvent]
    query: str
    expected_answer: str
    expected_absent: list[str] = field(default_factory=list)
    description: str = ""
    sessions: list[str] = field(default_factory=list)
    timestamps: list[str] = field(default_factory=list)
    expected_behavior: ExpectedBehavior = field(default_factory=lambda: ExpectedBehavior(answer=""))
    scoring_rules: ScoringRules = field(default_factory=ScoringRules)
    negative_assertions: list[str] = field(default_factory=list)

    @property
    def events(self) -> list[MemoryEvent]:
        """Alias for richer v0.2 schema naming."""

        return self.memory_events

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BenchmarkScenario:
        raw_events = data.get("events", data.get("memory_events", []))
        memory_events = [MemoryEvent.from_dict(event) for event in raw_events]
        expected_answer = str(data.get("expected_answer", ""))
        expected_behavior = ExpectedBehavior.from_raw(
            data.get("expected_behavior"),
            fallback_answer=expected_answer,
        )
        if not expected_answer:
            expected_answer = expected_behavior.answer
        negative_assertions = [
            str(item) for item in data.get("negative_assertions", data.get("expected_absent", []))
        ]
        sessions = [str(item) for item in data.get("sessions", [])]
        if not sessions:
            sessions = sorted({event.session_id for event in memory_events if event.session_id})
        timestamps = [str(item) for item in data.get("timestamps", [])]
        if not timestamps:
            timestamps = [event.timestamp for event in memory_events if event.timestamp]
        return cls(
            scenario_id=str(data["scenario_id"]),
            category=cast(Category, str(data["category"])),
            memory_events=memory_events,
            query=str(data["query"]),
            expected_answer=expected_answer,
            expected_absent=negative_assertions,
            description=str(data.get("description", "")),
            sessions=sessions,
            timestamps=timestamps,
            expected_behavior=expected_behavior,
            scoring_rules=ScoringRules.from_raw(data.get("scoring_rules")),
            negative_assertions=negative_assertions,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "category": self.category,
            "events": [event.to_memory() for event in self.memory_events],
            "memory_events": [event.to_memory() for event in self.memory_events],
            "sessions": self.sessions,
            "timestamps": self.timestamps,
            "query": self.query,
            "expected_answer": self.expected_answer,
            "expected_behavior": self.expected_behavior.to_dict(),
            "scoring_rules": self.scoring_rules.to_dict(),
            "negative_assertions": self.negative_assertions,
            "expected_absent": self.expected_absent,
            "description": self.description,
        }
