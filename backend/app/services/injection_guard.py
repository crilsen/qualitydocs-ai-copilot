"""Prompt injection guard: document content is DATA, never instructions.

Detects suspicious instruction-like text inside documents, flags it, and
wraps document context with delimiters so the LLM treats it as data.
Full content is never logged.
"""
import re

_PATTERNS = [
    r"ignore (all )?previous instructions",
    r"ignore the system prompt",
    r"disregard (all )?(prior|previous|above)",
    r"you are now ",
    r"new instructions?:",
    r"override the system",
    r"jailbreak",
    r"do not cite",
    r"hide .* finding",
    r"approve everything",
]


def scan(text: str) -> list[str]:
    hits = []
    low = text.lower()
    for p in _PATTERNS:
        m = re.search(p, low)
        if m:
            hits.append(m.group(0)[:80])
    return hits


def wrap_as_data(name: str, section: str, text: str, limit: int = 6000) -> str:
    clipped = text[:limit]
    return f"<<<DOCUMENT_DATA name={name!r} section={section!r}>\n{clipped}\n<<<END_DOCUMENT_DATA>>>"
