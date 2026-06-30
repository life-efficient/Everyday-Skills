---
name: local-whats-next
description: Summarize actionable root-level TODO.md items from local projects under ~/projects as a concise numbered what's-next snapshot. Use when the user asks what is next locally, wants a local project task snapshot, wants to inspect TODO.md items before optionally fanning out prompts, or wants a named or excluded local project scope.
---

# Local Whats Next

Summarize root-level local project tasks without producing handoff prompts.
This is the snapshot companion to `fanout-local-tasks`.

## Workflow

When invoked, find `TODO.md` files that sit at the root of direct child projects
under `~/projects`.

Prefer running:

```bash
python3 /Users/hq/.codex/skills/local-whats-next/scripts/generate_project_todo_snapshot.py
```

Then respond in chat with the generated snapshot. Do not write the result to a
file, do not return only a file link, and do not make the user open an artifact
to see what is next.

## Project Selection

Honor project-scoping language in the user's request:

- For "for X project", include only X: pass `--project X`.
- For "for X & Y project" or "for X and Y projects", include each named
  project: pass `--project X --project Y`.
- For "excluding X project" or "except X", omit X: pass `--exclude-project X`.
- If both inclusion and exclusion are requested, apply both; exclusions win.

Match project names case-insensitively against direct child folder names under
`~/projects`.

## Output Requirements

Default output is capped at 10 ready items:

- Start with `What's Next`.
- Format ready tasks as a numbered list, not prompt blocks.
- Each item should include the project name and a concise human-readable TODO
  item.
- Do not include boilerplate about reading files, preserving changes,
  verification, commits, or updating `TODO.md`.
- After the ready list, append exactly:
  `I also need your input on a few tasks:`
- Under that line, show a numbered list of TODOs that are too vague to hand off
  cleanly. Include the project name and unclear TODO.
- If no actionable root-level `TODO.md` bullet items are found under
  `~/projects`, say that directly and do not invent tasks.
- End by asking whether the user wants handoff prompts generated for the ready
  tasks.

If the user agrees to receive prompts, immediately use the `fanout-local-tasks`
workflow on the same project scope and filters. Do not ask the user to repeat
the scope.

Do not include TODO files nested below project roots unless the user explicitly
asks for recursive discovery.
