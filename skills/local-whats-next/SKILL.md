---
name: local-whats-next
description: Summarize actionable root-level TODO.md items from local projects under ~/projects as a concise numbered what's-next snapshot split by inferred execution mode. Use when the user asks what is next locally, wants a local project task snapshot, wants to inspect TODO.md items before optionally fanning out Codex threads with prompts, or wants a named or excluded local project scope.
---

# Local Whats Next

Summarize root-level local project tasks without creating handoff threads. This
is the snapshot companion to `fanout-local-tasks`.

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
- Format ready agent-executable and interactive tasks as a numbered list, not
  prompt blocks.
- Each item should include the project name and a concise human-readable TODO
  item.
- Do not include boilerplate about reading files, preserving changes,
  verification, commits, or updating `TODO.md`.
- Infer execution mode conservatively from TODO text:
  - `agent`: Codex can work autonomously from the TODO.
  - `interactive`: Codex can help but should walk the user through judgement,
    review, sending, scheduling, approval, or preference decisions.
  - `user`: the TODO requires a real-world or physical action Codex cannot
    meaningfully perform.
- Only include inferred `agent` and `interactive` tasks in the main numbered
  `What's Next` list.
- Only when there are inferred `user` tasks, append exactly:
  `There are a few things I can't physically help with:`
- Under that line, show a numbered list of user-only tasks with the project
  name and concrete action.
- If there are no inferred user-only tasks, omit this heading entirely.
- Only when TODOs are too vague to hand off cleanly, append exactly:
  `I also need your input on a few tasks:`
- Under that line, show a numbered list of TODOs that are too vague to hand off
  cleanly. Include the project name and unclear TODO.
- If there are no vague/input-needed TODOs, omit this heading entirely and do
  not mention that no such TODOs were found.
- If no actionable root-level `TODO.md` bullet items are found under
  `~/projects`, say that directly and do not invent tasks.
- End by asking whether the user wants Codex threads launched with handoff
  prompts for the ready agent-executable or interactive tasks.

If the user agrees to launch threads or receive prompts, immediately use the
`fanout-local-tasks` workflow on the same project scope and filters. Do not ask
the user to repeat the scope.

Do not include TODO files nested below project roots unless the user explicitly
asks for recursive discovery.
