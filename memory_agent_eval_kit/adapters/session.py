"""Session-scoped memory adapter example."""

from __future__ import annotations

from memory_agent_eval_kit.adapters.base import MemoryRecord
from memory_agent_eval_kit.adapters.simple import SimpleMemoryAgent


class SessionMemoryAgent(SimpleMemoryAgent):
    """Simple agent that records a default session for new memories."""

    def __init__(self, session_id: str) -> None:
        super().__init__()
        self.session_id = session_id

    def add_memory(self, memory: MemoryRecord) -> None:
        record = dict(memory)
        record.setdefault("session_id", self.session_id)
        super().add_memory(record)

    def query_session(self, prompt: str, session_id: str) -> str:
        original = self.session_id
        self.session_id = session_id
        try:
            return self.query(prompt)
        finally:
            self.session_id = original
