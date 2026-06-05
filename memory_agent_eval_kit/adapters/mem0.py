"""Optional Mem0 adapter."""

from __future__ import annotations

from typing import Any

from memory_agent_eval_kit.adapters.base import MemoryAgentAdapter, MemoryRecord


class Mem0Adapter(MemoryAgentAdapter):
    """Adapter for Mem0 memory clients with explicit graceful fallback.

    The adapter accepts an already configured Mem0-compatible client to avoid
    imposing paid API assumptions. If no client is provided and the optional
    ``mem0ai`` package is unavailable, calls can fall back to a supplied local
    adapter; otherwise they raise a clear dependency error.
    """

    def __init__(
        self,
        client: Any | None = None,
        *,
        user_id: str = "memory-agent-eval-kit",
        fallback: MemoryAgentAdapter | None = None,
    ) -> None:
        self.user_id = user_id
        self.fallback = fallback
        self._client = client if client is not None else self._load_default_client()

    @property
    def available(self) -> bool:
        """Whether a real Mem0-compatible client is configured."""

        return self._client is not None

    def query(self, prompt: str) -> str:
        if self._client is None:
            return self._fallback().query(prompt)
        result = self._client.search(prompt, user_id=self.user_id)
        if isinstance(result, str):
            return result
        if isinstance(result, list):
            return "\n".join(_memory_text(item) for item in result)
        if isinstance(result, dict):
            memories = result.get("results", result.get("memories", result))
            if isinstance(memories, list):
                return "\n".join(_memory_text(item) for item in memories)
        return str(result)

    def add_memory(self, memory: MemoryRecord) -> None:
        if self._client is None:
            self._fallback().add_memory(memory)
            return
        metadata = {key: value for key, value in memory.items() if key != "content"}
        self._client.add(str(memory.get("content", "")), user_id=self.user_id, metadata=metadata)

    def delete_memory(self, memory_id: str) -> None:
        if self._client is None:
            self._fallback().delete_memory(memory_id)
            return
        delete = getattr(self._client, "delete", None)
        if delete is None:
            raise RuntimeError("Configured Mem0 client does not expose delete().")
        delete(memory_id=memory_id, user_id=self.user_id)

    @staticmethod
    def _load_default_client() -> Any | None:
        try:
            from mem0 import Memory  # type: ignore[import-not-found]
        except ImportError:
            return None
        return Memory()

    def _fallback(self) -> MemoryAgentAdapter:
        if self.fallback is None:
            raise RuntimeError(
                "Mem0 optional dependency is not installed and no fallback adapter was provided. "
                "Install mem0ai or pass a configured Mem0 client/fallback."
            )
        return self.fallback


def _memory_text(item: object) -> str:
    if isinstance(item, dict):
        for key in ("memory", "content", "text"):
            value = item.get(key)
            if value is not None:
                return str(value)
    return str(item)
