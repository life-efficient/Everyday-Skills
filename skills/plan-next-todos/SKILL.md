---
name: plan-next-todos
description: Plan the next actionable TODO.md items for a software project. Use when the user asks what TODOs should be added next, wants to plan or draft the next project tasks, wants a roadmap-to-TODO pass, or asks to update a root TODO.md with newly discovered next work.
---

# Plan Next TODOs

Plan future work for a project from current repo evidence. The goal is a short
set of actionable TODO items, not a broad strategy memo.

## Workflow

1. Identify the target project.
   - Prefer the current repo if the user is already inside one.
   - For named projects, look under `~/projects/<name>` first.
   - If the user gives no project and the current directory is not a repo, ask for the project name.
2. Read existing planning context.
   - Read the root `TODO.md` when present.
   - Also scan root docs such as `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `docs/`, and recent commits when useful.
   - Use memory only as background; verify cheap facts in the repo before turning them into TODOs.
3. Inspect the repo for concrete next-work signals.
   - Search for `TODO`, `FIXME`, `HACK`, failing or skipped tests, empty states, placeholder copy, incomplete docs, and obvious setup gaps.
   - Check package scripts, tests, build config, migrations, API routes, and user-facing flows relevant to the project.
   - Prefer specific evidence over speculative product ideas.
4. Classify candidate TODOs.
   - `add`: genuinely missing next work that is not already listed.
   - `refine`: an existing TODO that is too vague and should be rewritten.
   - `defer`: useful idea, but not justified by current repo evidence or user direction.
   - `ignore`: duplicate, already done, or not actionable.
5. Produce concise TODO items.
   - Each TODO should name one verifiable outcome.
   - Include enough implementation context for another agent to start without rediscovery.
   - Avoid bundling unrelated work into one item.
   - Avoid tasks about process hygiene unless the repo evidence makes them real work.
6. Edit `TODO.md` only when the user explicitly asks to add or update TODOs.
   - Preserve the existing style, headings, and ordering.
   - Add new items to the most relevant section; create a small section only when needed.
   - Do not remove old items unless the user also asks for a refresh or prune pass.
   - Review the diff and commit according to the repo convention.

## Output

When only planning, report:

- `Suggested TODOs`: 3-7 bullet items, each phrased as it should appear in `TODO.md`
- `Evidence`: brief pointers to the files, tests, docs, or gaps that justify the items
- `Deferred`: optional short list of ideas not worth adding yet

When editing `TODO.md`, report:

- task file updated
- items added or rewritten
- checks run
- commit hash, if committed
- any uncertainty that still needs user direction

## Guardrails

- Do not invent a roadmap from taste alone; tie TODOs to repo evidence, explicit user direction, or obvious missing product behavior.
- Do not duplicate items already present in `TODO.md`.
- Do not convert `TODO.md` into a status report or research memo.
- Do not broaden existing tasks while refining them; make the next action narrower and easier to verify.
- Do not overwrite user changes in a dirty worktree; inspect and work with them.
