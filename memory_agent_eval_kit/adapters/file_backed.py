"""File-backed memory adapter example."""

from __future__ import annotations

import json
from pathlib import Path

from memory_agent_eval_kit.adapters.base import MemoryRecord
from memory_agent_eval_kit.adapters.simple import SimpleMemoryAgent


class FileBackedMemoryAgent(SimpleMemoryAgent):
    """Persist SimpleMemoryAgent memory records to a local JSON file."""

    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path
        self._load()

    def add_memory(self, memory: MemoryRecord) -> None:
        super().add_memory(memory)
        self._save()

    def delete_memory(self, memory_id: str) -> None:
        super().delete_memory(memory_id)
        self._save()

    def _load(self) -> None:
        if not self.path.exists():
            return
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            for item in payload:
                if isinstance(item, dict):
                    super().add_memory(item)

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        records = list(self._memories.values())
        self.path.write_text(json.dumps(records, indent=2), encoding="utf-8")
