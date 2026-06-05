"""Adapter interfaces for memory-enabled agents."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

MemoryRecord = dict[str, Any]


class MemoryAgentAdapter(ABC):
    """Stable contract that keeps benchmarks independent of any agent vendor.

    Implementations can wrap Mem0, LangGraph, OpenAI Memory, a personal
    continuity agent, Memory Agent SDK, Decision Memory Agent, or a custom
    research prototype. The benchmark runner only depends on these methods.
    """

    @abstractmethod
    def query(self, prompt: str) -> str:
        """Return the agent response for a user prompt."""

    @abstractmethod
    def add_memory(self, memory: MemoryRecord) -> None:
        """Add or update a memory record.

        Adapters should treat an existing ``memory_id`` as an update when the
        backing system supports upserts.
        """

    @abstractmethod
    def delete_memory(self, memory_id: str) -> None:
        """Delete or forget a memory record by stable identifier."""
