# Adapter Guide

Implement `MemoryAgentAdapter` for your agent:

```python
from memory_agent_eval_kit.adapters import MemoryAgentAdapter

class MyAgentAdapter(MemoryAgentAdapter):
    def query(self, prompt: str) -> str:
        return my_agent.ask(prompt)

    def add_memory(self, memory: dict) -> None:
        my_memory_store.upsert(memory)

    def delete_memory(self, memory_id: str) -> None:
        my_memory_store.delete(memory_id)
```

Guidelines:

- Preserve `memory_id` for deterministic deletion and correction tests.
- Treat `active=False` as stale/inactive memory.
- Honor `supersedes` when possible.
- Keep operations idempotent; benchmarks may be rerun.
- Avoid leaking deleted memories in `query` responses.

## Included local examples

### File-backed adapter

`FileBackedMemoryAgent` persists records to a JSON file. It is useful for local demos and deterministic tests without paid APIs.

### Session adapter

`SessionMemoryAgent` adds a default `session_id` to new memories, showing how cross-session continuity can be modeled.

## Future integrations

- **Mem0**: implement `add_memory` as a Mem0 memory write, `delete_memory` as a Mem0 delete, and `query` as your application agent call with Mem0 context retrieval.
- **LangGraph**: wrap a compiled graph in `query`, and map memory events to graph state/store updates.
- **Custom agents**: keep the adapter boundary thin. The benchmark should not know about your transport, prompt format, vector store, or model provider.

No external API dependency is required by the core framework.
