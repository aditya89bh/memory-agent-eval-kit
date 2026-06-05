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
