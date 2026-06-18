#!/usr/bin/env python3
"""Render a Codex MCP config block for ~/.codex/config.toml."""

from __future__ import annotations

import re
import sys


def normalize_name(raw: str) -> str:
    name = raw.strip().lower()
    name = re.sub(r"[^a-z0-9]+", "-", name)
    name = re.sub(r"-{2,}", "-", name).strip("-")
    if not name:
        raise ValueError("MCP server name normalizes to empty")
    return name


def render_block(name: str, url: str) -> str:
    normalized = normalize_name(name)
    cleaned_url = url.strip()
    if not cleaned_url.startswith(("https://", "http://")):
        raise ValueError("MCP URL must start with http:// or https://")

    return (
        f'[mcp_servers.{normalized}]\n'
        f'url = "{cleaned_url}"\n'
        'enabled = true\n'
    )


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: render_mcp_config.py <name> <url>", file=sys.stderr)
        return 1

    try:
        print(render_block(argv[1], argv[2]), end="")
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
