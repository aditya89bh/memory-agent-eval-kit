"""Optional LangGraph adapter."""

from __future__ import annotations

from typing import Any

from memory_agent_eval_kit.adapters.base import MemoryAgentAdapter, MemoryRecord


class LangGraphAdapter(MemoryAgentAdapter):
    """Adapter for configured LangGraph apps with graceful fallback.

    LangGraph does not define one universal memory API, so this adapter expects a
    supplied graph/app object that exposes ``invoke`` plus optional ``add_memory``
    and ``delete_memory`` hooks. If the optional dependency is unavailable and no
    app is supplied, it delegates to an explicit fallback or raises clearly.
    """

    def __init__(
        self,
        graph: Any | None = None,
        *,
        fallback: MemoryAgentAdapter | None = None,
        input_key: str = "messages",
    ) -> None:
        self.fallback = fallback
        self.input_key = input_key
        self._graph = graph if graph is not None else self._load_default_graph()

    @property
    def available(self) -> bool:
        """Whether a real LangGraph app is configured."""

        return self._graph is not None

    def query(self, prompt: str) -> str:
        if self._graph is None:
            return self._fallback().query(prompt)
        result = self._graph.invoke({self.input_key: [("user", prompt)]})
        return _extract_response(result)

    def add_memory(self, memory: MemoryRecord) -> None:
        if self._graph is None:
            self._fallback().add_memory(memory)
            return
        add_memory = getattr(self._graph, "add_memory", None)
        if add_memory is None:
            raise RuntimeError(
                "Configured LangGraph app does not expose add_memory(); pass a memory-aware app "
                "or an explicit fallback adapter for local smoke tests."
            )
        add_memory(memory)

    def delete_memory(self, memory_id: str) -> None:
        if self._graph is None:
            self._fallback().delete_memory(memory_id)
            return
        delete_memory = getattr(self._graph, "delete_memory", None)
        if delete_memory is None:
            raise RuntimeError(
                "Configured LangGraph app does not expose delete_memory(); pass a memory-aware app "
                "or an explicit fallback adapter for local smoke tests."
            )
        delete_memory(memory_id)

    @staticmethod
    def _load_default_graph() -> Any | None:
        try:
            import langgraph  # type: ignore[import-not-found]  # noqa: F401
        except ImportError:
            return None
        return None

    def _fallback(self) -> MemoryAgentAdapter:
        if self.fallback is None:
            raise RuntimeError(
                "LangGraph optional dependency/app is not configured and no fallback adapter was "
                "provided. Install langgraph and pass a compiled app, or pass fallback=."
            )
        return self.fallback


def _extract_response(result: object) -> str:
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        messages = result.get("messages")
        if isinstance(messages, list) and messages:
            last = messages[-1]
            content = getattr(last, "content", None)
            if content is not None:
                return str(content)
            if isinstance(last, tuple) and len(last) >= 2:
                return str(last[1])
            if isinstance(last, dict) and last.get("content") is not None:
                return str(last["content"])
        for key in ("response", "answer", "output"):
            value = result.get(key)
            if value is not None:
                return str(value)
    return str(result)
