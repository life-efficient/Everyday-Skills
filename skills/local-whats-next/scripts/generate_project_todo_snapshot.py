#!/usr/bin/env python3
"""Summarize root-level TODO.md items in ~/projects as a what's-next snapshot."""

from __future__ import annotations

import argparse
import importlib.util
import sys
import textwrap
from pathlib import Path


DEFAULT_LIMIT = 10


def load_fanout_module():
    script_path = (
        Path(__file__).resolve().parents[2]
        / "fanout-local-tasks"
        / "scripts"
        / "generate_project_todo_prompts.py"
    )
    spec = importlib.util.spec_from_file_location("generate_project_todo_prompts", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load fanout-local-tasks parser from {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


fanout = load_fanout_module()


def ready_line(project_path: Path, item_text: str) -> str:
    todo = fanout.concise_todo(item_text)
    return f"{project_path.name}: {textwrap.shorten(todo, width=180, placeholder='...')}"


def needs_input_line(project_path: Path, item_text: str) -> str:
    todo = fanout.concise_todo(item_text)
    return f"{project_path.name}: {textwrap.shorten(todo, width=160, placeholder='...')}"


def execution_mode(section: str, item_text: str) -> str:
    return fanout.execution_mode(section, item_text)


def generate(
    projects_dir: Path,
    include: set[str] | None = None,
    exclude: set[str] | None = None,
    limit: int = DEFAULT_LIMIT,
) -> str:
    include = include or set()
    exclude = exclude or set()
    ready: list[str] = []
    user_only: list[str] = []
    needs_input: list[str] = []

    for project_path in fanout.select_project_dirs(projects_dir, include, exclude):
        todo_path = project_path / "TODO.md"
        if not todo_path.is_file():
            continue
        todo_text = fanout.read_todo(todo_path)
        for section, item_text in fanout.todo_items(todo_text):
            mode = execution_mode(section, item_text)
            if mode == "underspecified":
                needs_input.append(needs_input_line(project_path, item_text))
                continue
            if mode == "user":
                user_only.append(ready_line(project_path, item_text))
                continue
            ready.append(ready_line(project_path, item_text))

    if not ready and not user_only and not needs_input:
        scope_parts: list[str] = []
        if include:
            scope_parts.append("included projects: " + ", ".join(sorted(include)))
        if exclude:
            scope_parts.append("excluded projects: " + ", ".join(sorted(exclude)))
        scope = " (" + "; ".join(scope_parts) + ")" if scope_parts else ""
        return f"No actionable root-level TODO.md bullet items found under {projects_dir}{scope}."

    sections: list[str] = ["What's Next"]
    if ready:
        sections.extend(f"{index}. {item}" for index, item in enumerate(ready[:limit], start=1))
    else:
        sections.append("No ready tasks found.")

    if user_only:
        sections.append("")
        sections.append("There are a few things I can't physically help with:")
        sections.extend(
            f"{index}. {item}" for index, item in enumerate(user_only[:limit], start=1)
        )

    if needs_input:
        sections.append("")
        sections.append("I also need your input on a few tasks:")
        sections.extend(
            f"{index}. {item}" for index, item in enumerate(needs_input[:limit], start=1)
        )

    return "\n".join(sections).rstrip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--projects-dir",
        default=str(Path.home() / "projects"),
        help="Directory containing project folders",
    )
    parser.add_argument("--project", action="append", help="Only include this project name. May be repeated.")
    parser.add_argument("--exclude-project", action="append", help="Exclude this project name. May be repeated.")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="Maximum ready and input-needed tasks to show")
    args = parser.parse_args()

    include = fanout.split_project_names(args.project)
    exclude = fanout.split_project_names(args.exclude_project)
    print(
        generate(
            Path(args.projects_dir).expanduser().resolve(),
            include=include,
            exclude=exclude,
            limit=args.limit,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
