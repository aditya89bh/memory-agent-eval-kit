# Adapter Integrations

`memory-agent-eval-kit` keeps external integrations optional. The core benchmark suite runs locally without paid APIs or vendor credentials.

## Mem0

`Mem0Adapter` wraps a configured Mem0-compatible client when you want to benchmark a real Mem0-backed memory system.

```python
from memory_agent_eval_kit.adapters import Mem0Adapter
from memory_agent_eval_kit.benchmarks import BenchmarkRunner

adapter = Mem0Adapter(client=my_mem0_client, user_id="benchmark-user")
run = BenchmarkRunner(adapter).run()
```

If the optional `mem0ai` package is not installed and no client is passed, the adapter does not pretend to be Mem0. It either delegates to an explicit fallback adapter or raises a clear runtime error.

```python
from memory_agent_eval_kit.adapters import Mem0Adapter, SimpleMemoryAgent

adapter = Mem0Adapter(fallback=SimpleMemoryAgent())
```

This fallback path is intended for local smoke tests only; benchmark submissions should disclose whether a real Mem0 client was used.
