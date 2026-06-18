#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def frontmatter(text: str, skill: pathlib.Path) -> str:
    if not text.startswith("---\n"):
        fail(f"{skill}: missing YAML frontmatter")
    try:
        return text.split("---\n", 2)[1]
    except IndexError:
        fail(f"{skill}: malformed YAML frontmatter")


def field_value(meta: str, field: str) -> str:
    match = re.search(rf"^{field}:\s*(.+)$", meta, re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip('"')


def main() -> int:
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    if not skill_files:
        fail("no skills found")

    resolver = (SKILLS / "RESOLVER.md").read_text(encoding="utf-8")
    failures: list[str] = []

    for skill_file in skill_files:
        skill_dir = skill_file.parent
        text = skill_file.read_text(encoding="utf-8")
        meta = frontmatter(text, skill_file)
        name = field_value(meta, "name")
        description = field_value(meta, "description")

        if not name:
            failures.append(f"{skill_dir.name}: missing name")
        if not description or "TODO" in description:
            failures.append(f"{skill_dir.name}: missing useful description")
        if "TODO" in text:
            failures.append(f"{skill_dir.name}: contains TODO placeholder")
        if f"skills/{skill_dir.name}/SKILL.md" not in resolver:
            failures.append(f"{skill_dir.name}: missing resolver entry")

        openai_yaml = skill_dir / "agents" / "openai.yaml"
        if openai_yaml.exists():
            agent_text = openai_yaml.read_text(encoding="utf-8")
            if "default_prompt" in agent_text and f"${skill_dir.name}" not in agent_text:
                failures.append(f"{skill_dir.name}: default_prompt does not mention ${skill_dir.name}")

    if failures:
        for item in failures:
            print(f"FAIL: {item}", file=sys.stderr)
        return 1

    print(f"checked {len(skill_files)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

