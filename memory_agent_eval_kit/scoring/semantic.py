"""Deterministic semantic-ish scoring without external model dependencies."""

from __future__ import annotations

import re
from difflib import SequenceMatcher

_TOKEN_RE = re.compile(r"[a-zA-Z0-9_./-]+")


def normalized_text(text: str) -> str:
    """Lowercase text and collapse punctuation/whitespace for stable matching."""

    return " ".join(token.casefold() for token in _TOKEN_RE.findall(text))


def exact_score(expected: str, actual: str) -> float:
    """Return 1 when normalized expected text is contained in actual text."""

    expected_norm = normalized_text(expected)
    actual_norm = normalized_text(actual)
    return 1.0 if expected_norm and expected_norm in actual_norm else 0.0


def token_overlap(expected: str, actual: str) -> float:
    """Return expected-token recall against actual tokens."""

    expected_tokens = set(normalized_text(expected).split())
    actual_tokens = set(normalized_text(actual).split())
    if not expected_tokens:
        return 0.0
    return len(expected_tokens & actual_tokens) / len(expected_tokens)


def partial_score(expected: str, actual: str) -> float:
    """Blend token overlap and normalized sequence similarity."""

    expected_norm = normalized_text(expected)
    actual_norm = normalized_text(actual)
    if not expected_norm or not actual_norm:
        return 0.0
    if expected_norm in actual_norm:
        return 1.0
    similarity = SequenceMatcher(None, expected_norm, actual_norm).ratio()
    return max(token_overlap(expected, actual), similarity)
