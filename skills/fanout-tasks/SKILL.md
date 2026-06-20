---
name: fanout-tasks
description: Fan out concise chat prompts from individual root-level TODO.md items in projects under ~/projects. Use when the user wants daily kickoff prompts, project TODO item prompts, one prompt per TODO item, prompts for a named project, prompts for multiple named projects, or prompts excluding a named project.
---

# Fanout Tasks

## Workflow

When invoked, find `TODO.md` files that sit at the root of direct child projects under `~/projects`.

Prefer running:

```bash
python3 /Users/hq/.codex/skills/fanout-tasks/scripts/generate_project_todo_prompts.py
```

Then respond in chat with the generated prompts. Do not write the result to a file, do not return only a file link, and do not make the user open an artifact to see the prompts.

## Project Selection

Honor project-scoping language in the user's request:

- For “for X project”, include only X: pass `--project X`.
- For “for X & Y project” or “for X and Y projects”, include each named project: pass `--project X --project Y`.
- For “excluding X project” or “except X”, omit X: pass `--exclude-project X`.
- If both inclusion and exclusion are requested, apply both; exclusions win.

Match project names case-insensitively against direct child folder names under `~/projects`.

## Output Requirements

Default output is capped at 10 ready items. Keep each ready item short and copyable:

- Show a `Ready tasks` section first.
- Each ready task should be one concise copyable prompt block that names the project and describes only the TODO item.
- Do not format ready tasks as a numbered list.
- Do not include boilerplate about reading files, preserving changes, verification, commits, or updating `TODO.md`.
- Do not hard-code a single sentence shape in the skill body; use the generator template so phrasing can evolve.
- Show a `Needs more specification` section after ready tasks when TODOs are too vague to hand off cleanly.
- Keep the needs-specification list succinct; name the project and the unclear TODO.

If no actionable root-level `TODO.md` bullet items are found under `~/projects`, say that directly and do not invent prompts.

Do not include TODO files nested below project roots unless the user explicitly asks for recursive discovery.
