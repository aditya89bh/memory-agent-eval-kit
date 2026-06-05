"""Typed domain models for benchmark scenarios."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

Category = Literal[
    "recall",
    "contradiction",
    "correction",
    "forgetting",
    "temporal",
    "stale_memory",
    "continuity",
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
class BenchmarkScenario:
    """A single benchmark case."""

    scenario_id: str
    category: Category
    memory_events: list[MemoryEvent]
    query: str
    expected_answer: str
    expected_absent: list[str] = field(default_factory=list)
    description: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BenchmarkScenario:
        return cls(
            scenario_id=str(data["scenario_id"]),
            category=data["category"],
            memory_events=[MemoryEvent.from_dict(event) for event in data.get("memory_events", [])],
            query=str(data["query"]),
            expected_answer=str(data["expected_answer"]),
            expected_absent=[str(item) for item in data.get("expected_absent", [])],
            description=str(data.get("description", "")),
        )
