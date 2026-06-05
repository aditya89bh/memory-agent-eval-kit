"""Deterministic in-memory adapter used for examples and smoke tests."""

from __future__ import annotations

import re
from datetime import UTC, datetime

from memory_agent_eval_kit.adapters.base import MemoryAgentAdapter, MemoryRecord

_WORD_RE = re.compile(r"[a-zA-Z0-9_./-]+")


class SimpleMemoryAgent(MemoryAgentAdapter):
    """Small rule-based memory agent with no external API dependency.

    It is intentionally simple but supports the behaviors benchmarks need:
    explicit deletion, correction supersession, inactive stale records, temporal
    recency, contradiction surfacing, and cross-session continuity.
    """

    def __init__(self) -> None:
        self._memories: dict[str, MemoryRecord] = {}
        self._counter = 0

    def query(self, prompt: str) -> str:
        candidates = [
            memory for memory in self._memories.values() if bool(memory.get("active", True))
        ]
        if self._asks_for_unknown(prompt) and not self._rank(prompt, candidates):
            return "I do not know."
        if _asks_for_timeline(prompt):
            timeline = self._timeline(prompt, candidates)
            if timeline:
                return " | ".join(timeline)
        rank_candidates = candidates
        if _asks_for_previous(prompt):
            rank_candidates = [
                memory
                for memory in candidates
                if not _is_current_memory(str(memory.get("content", "")))
            ]
        ranked = self._rank(prompt, rank_candidates)
        if not ranked:
            return "I do not know."
        top_score = ranked[0][0]
        top_memories = [memory for score, memory in ranked if score == top_score]
        if not _asks_for_previous(prompt) and self._looks_contradictory(prompt, top_memories):
            return "A contradiction is present in memory; this needs clarification."
        return str(ranked[0][1].get("content", "I do not know."))

    def add_memory(self, memory: MemoryRecord) -> None:
        record = dict(memory)
        memory_id = str(record.get("memory_id") or self._next_id())
        record["memory_id"] = memory_id
        supersedes = record.get("supersedes")
        if supersedes is not None:
            self.delete_memory(str(supersedes))
        if record.get("active", True) is False:
            self.delete_memory(memory_id)
            return
        if _is_untrusted(record) and self._has_trusted_overlap(record):
            return
        self._memories[memory_id] = record

    def delete_memory(self, memory_id: str) -> None:
        self._memories.pop(memory_id, None)

    @property
    def memory_count(self) -> int:
        return len(self._memories)

    def _has_trusted_overlap(self, record: MemoryRecord) -> bool:
        new_terms = _terms(str(record.get("content", "")))
        for memory in self._memories.values():
            if str(memory.get("source", "")).casefold() != "trusted":
                continue
            if len(new_terms & _terms(str(memory.get("content", "")))) >= 2:
                return True
        return False

    def _next_id(self) -> str:
        self._counter += 1
        return f"memory-{self._counter}"

    def _rank(self, prompt: str, memories: list[MemoryRecord]) -> list[tuple[float, MemoryRecord]]:
        query_terms = _terms(prompt)
        ranked: list[tuple[float, MemoryRecord]] = []
        for memory in memories:
            content = str(memory.get("content", ""))
            terms = _terms(content)
            overlap = len(query_terms & terms)
            if overlap == 0:
                continue
            score = float(overlap)
            if _is_current_memory(content):
                score += 2.0
            if _is_recent(memory):
                score += 1.0
            if memory.get("type") == "correction":
                score += 2.0
            ranked.append((score, memory))
        return sorted(
            ranked,
            key=lambda item: (item[0], _timestamp_value(item[1])),
            reverse=True,
        )

    def _timeline(self, prompt: str, memories: list[MemoryRecord]) -> list[str]:
        ranked = self._rank(prompt, memories)
        if not ranked:
            return []
        unique = {
            str(memory.get("memory_id", index)): memory for index, (_, memory) in enumerate(ranked)
        }
        ordered = sorted(unique.values(), key=_timestamp_value)
        return [str(memory.get("content", "")) for memory in ordered]

    def _looks_contradictory(self, prompt: str, memories: list[MemoryRecord]) -> bool:
        if len(memories) < 2:
            return False
        contents = [str(memory.get("content", "")).casefold() for memory in memories]
        if any("not " in content for content in contents) and any(
            "not " not in content for content in contents
        ):
            return True
        if any(
            word in prompt.casefold()
            for word in ("preferred", "favorite", "where", "when", "what", "which")
        ):
            endings = {_object_fragment(content) for content in contents}
            return len(endings) > 1
        return False

    def _asks_for_unknown(self, prompt: str) -> bool:
        return any(
            word in prompt.casefold()
            for word in ("password", "token", "otp", "door code", "api key")
        )


def _terms(text: str) -> set[str]:
    stop = {
        "what",
        "which",
        "when",
        "where",
        "do",
        "i",
        "is",
        "my",
        "the",
        "a",
        "an",
        "to",
        "be",
        "used",
        "now",
        "current",
        "latest",
        "across",
        "sessions",
        "in",
        "this",
        "new",
        "another",
        "should",
        "you",
        "prefer",
        "preferred",
    }
    terms: set[str] = set()
    for token in _WORD_RE.findall(text):
        normalized = token.casefold()
        if normalized in stop:
            continue
        terms.add(normalized)
        if normalized.endswith("ing") and len(normalized) > 5:
            terms.add(normalized[:-3])
            terms.add(normalized[:-3] + "e")
        if normalized.endswith("ence") and len(normalized) > 6:
            terms.add(normalized[:-4])
    return terms


def _timestamp_value(memory: MemoryRecord) -> float:
    value = memory.get("timestamp")
    if not isinstance(value, str):
        return 0.0
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return 0.0


def _is_recent(memory: MemoryRecord) -> bool:
    return _timestamp_value(memory) > datetime(2026, 1, 15, tzinfo=UTC).timestamp()


def _is_current_memory(content: str) -> bool:
    return any(
        marker in content.casefold()
        for marker in ("current", "today", "this week", "new ", "version 2", "latest")
    )


def _object_fragment(content: str) -> str:
    for separator in (" is ", " was ", " are ", " uses "):
        if separator in content:
            return content.rsplit(separator, 1)[-1].strip()
    return content.strip()


def _asks_for_previous(prompt: str) -> bool:
    return any(word in prompt.casefold() for word in ("previous", "old", "prior", "before"))


def _asks_for_timeline(prompt: str) -> bool:
    return any(word in prompt.casefold() for word in ("timeline", "evolve", "history"))


def _is_untrusted(memory: MemoryRecord) -> bool:
    source = str(memory.get("source", "")).casefold()
    return source in {"untrusted", "malicious"} or bool(memory.get("malicious", False))
