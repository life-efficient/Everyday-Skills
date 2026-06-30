---
name: fanout-local-tasks
description: Fan out individual root-level TODO.md items in local projects under ~/projects into Codex threads with concise handoff prompts. Use when the user wants daily kickoff threads, local project TODO item prompts, one thread per TODO item, prompts for a named local project, prompts for multiple named local projects, or prompts excluding a named local project.
---

# Fanout Local Tasks

Create one Codex thread per fanout-ready local TODO when the Codex app thread
tools are available. The generated worker prompt remains self-contained and
can still be returned as a copyable prompt block when the user explicitly asks
for prompts only, or when live thread creation is unavailable after targeted
tool discovery.

## Workflow

When invoked, find `TODO.md` files that sit at the root of direct child projects under `~/projects`.

Prefer running:

```bash
python3 /Users/hq/.codex/skills/fanout-local-tasks/scripts/generate_project_todo_prompts.py
```

Then create Codex threads with the generated prompts when possible. Discover
`codex_app.create_thread` with `tool_search` before concluding live fanout is
unavailable. Use `codex_app.list_projects` when available to choose a repo
target; otherwise use `target: { "type": "projectless" }` for general local
TODO work.

Respond in chat with launched thread IDs or links and any blocked/non-fanned-out
tasks. Do not write the result to a file, do not return only a file link, and
do not make the user open an artifact to see what was launched.

## Project Selection

Honor project-scoping language in the user's request:

- For “for X project”, include only X: pass `--project X`.
- For “for X & Y project” or “for X and Y projects”, include each named project: pass `--project X --project Y`.
- For “excluding X project” or “except X”, omit X: pass `--exclude-project X`.
- If both inclusion and exclusion are requested, apply both; exclusions win.

Match project names case-insensitively against direct child folder names under `~/projects`.

## Output Requirements

Default output is capped at 10 ready items. Keep each worker prompt short,
self-contained, and suitable as the initial prompt for a fresh Codex thread:

- When live thread creation succeeds, show a `Launched local task threads`
  section first.
- When the user asks for prompts only, or live thread creation is unavailable,
  show a `Ready tasks` section first.
- Each ready task should be one concise copyable prompt block that names the project and describes only the TODO item.
- Infer execution mode conservatively from TODO text:
  - `agent`: Codex can work autonomously from the TODO.
  - `interactive`: Codex can help but should walk the user through judgement,
    review, sending, scheduling, approval, or preference decisions.
  - `user`: the TODO requires a real-world or physical action Codex cannot
    meaningfully perform.
- Generate worker prompts only for inferred `agent` and `interactive` TODOs.
- For inferred `interactive` TODOs, prepend this sentence before the task brief:
  `I need to get this done, and I want you to walk me through it step by step.`
- Do not format ready tasks as a numbered list.
- Do not include boilerplate about reading files, preserving changes, verification, commits, or updating `TODO.md`.
- Do not hard-code a single sentence shape in the skill body; use the generator template so phrasing can evolve.
- When live thread creation succeeds, do not print the full worker prompts by
  default. Instead, show a concise launched-thread list with each project,
  inferred execution mode when useful, and returned thread ID or link.
- Show a `Things Codex can't physically help with` section for inferred `user`
  TODOs. Keep the list succinct; name the project and concrete action.
- Show a `Needs more specification` section after ready tasks when TODOs are too vague to hand off cleanly.
- Keep the needs-specification list succinct; name the project and the unclear TODO.

If no actionable root-level `TODO.md` bullet items are found under `~/projects`, say that directly and do not invent prompts.

If live thread creation is unavailable after targeted `create_thread`
discovery, output exactly:

`Parallel execution unavailable here.`

Then provide the shortest useful set of copyable worker prompts.

Do not include TODO files nested below project roots unless the user explicitly asks for recursive discovery.
