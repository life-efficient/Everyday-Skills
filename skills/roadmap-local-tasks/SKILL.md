---
name: roadmap-local-tasks
description: Gather roadmap thoughts for existing local projects under ~/projects and turn them into TODO.md-ready next tasks. Use when the user wants to think through what to do next across local projects, focus on a certain project, exclude certain projects, compare project priorities, draft evidence-backed next TODOs, or populate project TODO.md files from planning input.
---

# Roadmap Local Tasks

Guide a short planning pass for local projects. The goal is to identify active
threads in a project, suggest useful extensions and adjacent work, and convert
repo evidence or the user's priorities into clear `TODO.md` entries or
TODO-ready task candidates. This skill plans and records next work; it does not
implement the work unless the user explicitly asks for implementation.

## Contract

Use this skill when the user wants to gather thoughts, choose priorities, or
roadmap next steps for projects that live under `~/projects`.

Successful completion means:

- the target scope is explicit: one project, several projects, all projects, or all except named exclusions
- the response reflects the project's visible work threads, repo evidence, and plausible next extensions
- the user has answered any focused questions needed to choose among threads
- the response turns their answers into practical TODO-ready next-step options
- if the user gives enough direction to act, the relevant root `TODO.md` files are updated in the existing style
- no product/code implementation is performed unless the user explicitly asks for implementation

## Workflow

1. Identify project scope.
   - Honor explicit focus language such as "for BigBrain", "focus on Taleem", or "only relay".
   - Honor exclusion language such as "excluding ICAIRE", "not diffusing-ai", or "everything except X".
   - If the user gives no project scope, inspect direct child folders under `~/projects` if useful, then ask whether they want to focus on one project, several projects, all projects, or exclude any projects.
   - Ask for scope before deeper repo inspection when the request is broad or ambiguous.
2. Gather context lightly.
   - For scoped projects, read root planning files when present: `TODO.md`, `README.md`, `ROADMAP.md`, `CHANGELOG.md`, and `docs/` indexes.
   - Use current repo state only to frame better questions. Do not perform a full task refresh unless the user asks for it.
   - If the user wants a pure brainstorm, skip repo inspection and ask from their stated goals.
3. Inspect for concrete next-work signals when the user wants TODOs.
   - Search for `TODO`, `FIXME`, `HACK`, failing or skipped tests, empty states, placeholder copy, incomplete docs, and obvious setup gaps.
   - Check package scripts, tests, build config, migrations, API routes, and user-facing flows relevant to the project.
   - Prefer specific evidence over speculative product ideas.
   - Use memory only as background; verify cheap facts in the repo before turning them into TODOs.
4. Map threads before asking broad questions.
   - Identify 3-6 active or implied work threads from planning files, recent context, and the user's prompt.
   - For each thread, name the current direction and suggest 1-3 concrete extensions.
   - Add a short "other suggestions" section for adjacent opportunities that are not already implied by the visible threads.
   - Treat time horizon as priority ordering, not as a required planning question. Use `now`, `next`, and `later` when priority is clear.
5. Ask only targeted roadmap questions.
   - Ask questions only when they would change the task list or file placement.
   - Prefer concrete choice questions about which thread to advance first, which audience or business outcome matters most, what must be kept separate, or which risk blocks execution.
   - Do not ask broad prompts such as "what would make the next work session successful" unless the user explicitly asks for reflective planning.
   - Do not ask "what should not be touched" by default; rely on the user to state exclusions, and ask only if file ownership or safety boundaries are ambiguous.
   - For multiple projects, ask for priority criteria only after naming the visible threads and suggested extensions.
6. Convert evidence and answers into next-step options.
   - Summarize the user's direction in one short paragraph.
   - Propose 3-7 candidate TODO entries, each tied to a project and a visible outcome.
   - Classify candidate TODOs as `add`, `refine`, `defer`, or `ignore` before presenting or writing them.
   - Phrase each TODO as one verifiable outcome with enough implementation context for another agent to start without rediscovery.
   - Avoid bundling unrelated work, duplicating existing `TODO.md` items, or adding process hygiene unless the repo evidence makes it real work.
   - Mark items as `now`, `next`, or `later` when prioritization is clear.
   - Call out any unresolved decision that would change the plan.
7. Populate `TODO.md` once direction is clear.
   - Treat roadmap decisions, priorities, and "that would be good" confirmations as permission to update the relevant root `TODO.md` files.
   - Preserve existing headings and do not remove tasks; use `refresh-local-tasks` for pruning stale items.
   - If repo evidence supports a task but the priority is unclear, report it as `defer` instead of writing it.
   - Stop after updating TODOs and reporting the changed files unless the user explicitly asks to implement code.

## Question Patterns

When scope is missing, ask:

- Which project should we focus on first, or should we look across all projects?
- Are there any projects to exclude from this planning pass?

When one project is selected, ask:

- I see these active threads: `<thread list>`. Which one should be treated as `now`?
- Which audience or business outcome should drive this roadmap: `<specific options from context>`?
- Which boundary matters most here, such as repo placement, data privacy, production safety, or gated versus public content?

When several projects are in play, ask:

- Which criterion should drive priority: revenue, user value, maintenance risk, deadline, or personal momentum?
- Which project has the most urgent external commitment?
- Which project should intentionally receive less attention for now?

## Suggestion Patterns

When a project has enough visible context, lead with suggestions before
questions:

- `Active threads`: name the threads already present in the repo, TODOs, docs,
  recent work, or user prompt.
- `Extensions`: for each thread, suggest practical next work that follows from
  the thread.
- `Other suggestions`: add adjacent options the user may not have named but
  that fit the project's direction.
- `Decisions needed`: list only decisions that block choosing or placing TODO
  entries.

## Guardrails

- Do not assume "all projects" when the user has not specified scope; ask for focus or exclusions.
- Do not turn a roadmap conversation into a code audit unless the user asks for evidence-backed TODOs.
- Do not edit task files during the questioning phase, but do update them once the user has provided enough priority direction.
- Do not implement roadmap items from this skill alone. Populate `TODO.md`; implementation belongs to a separate explicit request.
- Do not duplicate items already present in `TODO.md`.
- Do not invent a roadmap from taste alone; tie TODOs to repo evidence, explicit user direction, or obvious missing product behavior.
- Do not broaden existing tasks while refining them; make the next action narrower and easier to verify.
- Do not ask for generic planning detail when concrete project threads are already visible.
- Do not ask for every possible detail at once; keep questions short enough to answer in chat.
- Do not invent deadlines, stakeholders, or priorities that the user has not provided.

## Output

For the first response, prefer a thread map plus targeted questions when the
project scope is known. Prefer questions first only when scope is missing. Once
the user answers, report:

- `Direction`: one concise summary of the chosen focus
- `Active threads`: visible threads and suggested extensions, when useful
- `Evidence`: brief pointers to files, tests, docs, or gaps when suggestions come from repo inspection
- `Deferred`: useful ideas not justified enough to add yet, when relevant
- `TODO updates`: changed `TODO.md` files and items added, when enough direction was provided
- `Next steps`: 3-7 TODO-ready options with project names, when more confirmation is still needed before editing
- `Open decisions`: only the decisions still blocking a sharper roadmap

When files are updated, report the changed files, items added, checks run, and
commit hash when committed.
