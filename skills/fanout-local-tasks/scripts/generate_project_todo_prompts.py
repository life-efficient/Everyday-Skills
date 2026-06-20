#!/usr/bin/env python3
"""Fan out concise prompts from root-level TODO.md items in ~/projects."""

from __future__ import annotations

import argparse
import re
import textwrap
from pathlib import Path


MAX_ITEM_CHARS = 3000
DEFAULT_LIMIT = 10
DEFAULT_PROMPT_TEMPLATE = "In {project} project, {todo}"
NEEDS_SPEC_MARKERS = (
    "decide ",
    "whether ",
    "exact ",
    "frontmatter",
    "keep ",
)
READY_VERBS = {
    "add",
    "build",
    "continue",
    "define",
    "document",
    "improve",
    "prefer",
    "remove",
    "replace",
    "revoke",
    "rotate",
    "score",
    "separate",
    "start",
    "store",
    "update",
    "use",
    "verify",
}


def normalize_project_name(name: str) -> str:
    return " ".join(name.strip().lower().split())


def split_project_names(values: list[str] | None) -> set[str]:
    if not values:
        return set()

    names: set[str] = set()
    for value in values:
        normalized_separators = re.sub(r"\s+(?:and|&)\s+", ",", value, flags=re.IGNORECASE)
        for part in normalized_separators.split(","):
            name = normalize_project_name(part)
            for suffix in (" projects", " project"):
                if name.endswith(suffix):
                    name = name[: -len(suffix)].strip()
                    break
            if name:
                names.add(name)
    return names


def project_dirs(projects_dir: Path) -> list[Path]:
    if not projects_dir.exists():
        return []
    return sorted([path for path in projects_dir.iterdir() if path.is_dir()], key=lambda p: p.name.lower())


def select_project_dirs(projects_dir: Path, include: set[str], exclude: set[str]) -> list[Path]:
    dirs = project_dirs(projects_dir)
    selected: list[Path] = []
    for project_path in dirs:
        project_name = normalize_project_name(project_path.name)
        if include and project_name not in include:
            continue
        if project_name in exclude:
            continue
        selected.append(project_path)
    return selected


def read_todo(todo_path: Path) -> str:
    text = todo_path.read_text(encoding="utf-8", errors="replace").strip()
    return text


def truncate_item(item_text: str) -> str:
    if len(item_text) <= MAX_ITEM_CHARS:
        return item_text
    return item_text[:MAX_ITEM_CHARS].rstrip() + "\n\n[TODO item excerpt truncated for length. Read the full file before editing.]"


def bullet_indent(line: str) -> int | None:
    stripped = line.lstrip(" ")
    if stripped.startswith(("- ", "* ", "+ ")):
        return len(line) - len(stripped)
    return None


def todo_items(todo_text: str) -> list[tuple[str, str]]:
    lines = todo_text.splitlines()
    bullet_indents = [indent for line in lines if (indent := bullet_indent(line)) is not None]
    if not bullet_indents:
        return []

    item_indent = min(bullet_indents)
    items: list[tuple[str, str]] = []
    current_heading = "TODO"
    current_lines: list[str] = []

    def flush() -> None:
        if current_lines:
            items.append((current_heading, truncate_item("\n".join(current_lines).strip())))

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            flush()
            current_lines = []
            current_heading = stripped.lstrip("#").strip() or "TODO"
            continue

        indent = bullet_indent(line)
        if indent == item_indent:
            flush()
            current_lines = [line]
            continue

        if current_lines:
            current_lines.append(line)

    flush()
    return items


def strip_bullet_marker(line: str) -> str:
    stripped = line.strip()
    for marker in ("- ", "* ", "+ "):
        if stripped.startswith(marker):
            return stripped[len(marker) :].strip()
    return stripped


def concise_todo(item_text: str) -> str:
    lines = item_text.splitlines()
    if not lines:
        return ""

    first_line = strip_bullet_marker(lines[0]).rstrip(".")
    detail_lines = []
    for line in lines[1:]:
        if bullet_indent(line) is None:
            continuation = line.strip()
            if continuation:
                first_line = f"{first_line} {continuation.rstrip('.')}"
            continue

        stripped = strip_bullet_marker(line)
        if stripped:
            detail_lines.append(stripped.rstrip("."))

    if not detail_lines:
        return first_line

    details = "; ".join(detail_lines)
    return f"{first_line}: {details}"


def needs_more_specification(section: str, item_text: str) -> bool:
    todo = concise_todo(item_text).lower()
    words = todo.split()
    if not words:
        return True
    if section.strip().lower() == "open design decisions":
        return True
    if words[0].rstrip(":") in READY_VERBS:
        return False
    if todo.endswith(":") or len(words) <= 3:
        return True
    return todo.startswith(NEEDS_SPEC_MARKERS)


def item_title(item_text: str) -> str:
    lines = item_text.splitlines()
    first_line = lines[0].strip()
    for marker in ("- ", "* ", "+ "):
        if first_line.startswith(marker):
            first_line = first_line[len(marker) :]
            break

    continuation_parts: list[str] = []
    for line in lines[1:]:
        stripped = line.strip()
        if not stripped or bullet_indent(line) is not None:
            break
        continuation_parts.append(stripped)

    title = " ".join([first_line, *continuation_parts]).rstrip(".")
    return textwrap.shorten(title, width=100, placeholder="...")


def prompt_for_item(project_path: Path, item_text: str, template: str) -> str:
    project_name = project_path.name
    return template.format(project=project_name, todo=concise_todo(item_text)).strip()


def spec_line(project_path: Path, item_text: str) -> str:
    return f"- {project_path.name}: {textwrap.shorten(concise_todo(item_text), width=140, placeholder='...')}"


def format_output(ready: list[str], needs_spec: list[str], limit: int) -> str:
    if not ready and not needs_spec:
        return ""

    sections: list[str] = []
    if ready:
        sections.append("Ready tasks")
        for prompt in ready[:limit]:
            sections.append(f"```text\n{prompt}\n```")
    else:
        sections.append("Ready tasks\nNo ready tasks found.")

    if needs_spec:
        sections.append("\nNeeds more specification")
        sections.extend(needs_spec[:limit])

    return "\n".join(sections).rstrip() + "\n"


def generate(
    projects_dir: Path,
    include: set[str] | None = None,
    exclude: set[str] | None = None,
    limit: int = DEFAULT_LIMIT,
    template: str = DEFAULT_PROMPT_TEMPLATE,
) -> str:
    include = include or set()
    exclude = exclude or set()
    ready: list[str] = []
    needs_spec: list[str] = []
    for project_path in select_project_dirs(projects_dir, include, exclude):
        todo_path = project_path / "TODO.md"
        if not todo_path.is_file():
            continue
        todo_text = read_todo(todo_path)
        for section, item_text in todo_items(todo_text):
            if needs_more_specification(section, item_text):
                needs_spec.append(spec_line(project_path, item_text))
                continue
            ready.append(prompt_for_item(project_path, item_text, template))

    output = format_output(ready, needs_spec, limit)
    if not output:
        scope_parts: list[str] = []
        if include:
            scope_parts.append("included projects: " + ", ".join(sorted(include)))
        if exclude:
            scope_parts.append("excluded projects: " + ", ".join(sorted(exclude)))
        scope = " (" + "; ".join(scope_parts) + ")" if scope_parts else ""
        return f"No actionable root-level TODO.md bullet items found under {projects_dir}{scope}."

    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--projects-dir", default=str(Path.home() / "projects"), help="Directory containing project folders")
    parser.add_argument("--project", action="append", help="Only include this project name. May be repeated.")
    parser.add_argument("--exclude-project", action="append", help="Exclude this project name. May be repeated.")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="Maximum ready tasks and spec-needed tasks to show")
    parser.add_argument("--template", default=DEFAULT_PROMPT_TEMPLATE, help="Prompt template using {project} and {todo}")
    args = parser.parse_args()

    include = split_project_names(args.project)
    exclude = split_project_names(args.exclude_project)
    print(
        generate(
            Path(args.projects_dir).expanduser().resolve(),
            include=include,
            exclude=exclude,
            limit=args.limit,
            template=args.template,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
