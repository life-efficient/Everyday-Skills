#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class PatternRule:
    category: str
    pattern: re.Pattern[str]


RULES: tuple[PatternRule, ...] = (
    PatternRule("profanity", re.compile(r"\b(?:fuck(?:ing|ed)?|shit(?:ty)?|bullshit|bitch(?:es)?|asshole|dick|cunt)\b", re.I)),
    PatternRule("insult", re.compile(r"\b(?:idiot|moron|stupid|dumb|worthless|incompetent|pathetic|loser)\b", re.I)),
    PatternRule("sexual", re.compile(r"\b(?:sex|sexual|porn|nude|nudes|naked|hookup|fetish)\b", re.I)),
    PatternRule("sensitive", re.compile(r"\b(?:ssn|social security|passport|bank account|iban|credit card|diagnosis|therapy|medication|pregnan(?:t|cy)|divorce)\b", re.I)),
    PatternRule("personal", re.compile(r"\b(?:family dispute|marital|relationship problem|private life|home address|personal phone)\b", re.I)),
    PatternRule("slander", re.compile(r"\b(?:fraud|criminal|corrupt|harassment|abuse|lawsuit|illegal)\b", re.I)),
)


SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")


def sanitize(text: str) -> tuple[str, dict[str, int]]:
    counts = {rule.category: 0 for rule in RULES}
    safe_chunks: list[str] = []

    for chunk in SENTENCE_SPLIT.split(text):
        stripped = chunk.strip()
        if not stripped:
            continue
        matched_categories = []
        for rule in RULES:
            if rule.pattern.search(stripped):
                matched_categories.append(rule.category)
        if matched_categories:
            for category in set(matched_categories):
                counts[category] += 1
            safe_chunks.append(f"[redacted: {', '.join(sorted(set(matched_categories)))}]")
        else:
            safe_chunks.append(stripped)

    collapsed: list[str] = []
    for chunk in safe_chunks:
        if collapsed and collapsed[-1] == chunk and chunk.startswith("[redacted:"):
            continue
        collapsed.append(chunk)

    return "\n".join(collapsed).strip() + ("\n" if collapsed else ""), counts


def main() -> int:
    parser = argparse.ArgumentParser(description="First-pass sanitizer for Granola transcript sidecars.")
    parser.add_argument("input", nargs="?", help="Transcript file. Reads stdin when omitted.")
    parser.add_argument("--summary", action="store_true", help="Print redaction counts to stderr.")
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as handle:
            text = handle.read()
    else:
        text = sys.stdin.read()

    sanitized, counts = sanitize(text)
    sys.stdout.write(sanitized)
    if args.summary:
        total = sum(counts.values())
        detail = ", ".join(f"{key}={value}" for key, value in sorted(counts.items()) if value)
        sys.stderr.write(f"redactions={total}")
        if detail:
            sys.stderr.write(f" ({detail})")
        sys.stderr.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
