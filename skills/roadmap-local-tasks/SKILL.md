---
name: roadmap-local-tasks
description: Gather roadmap thoughts for existing local projects under ~/projects and turn them into TODO.md-ready next tasks. Use when the user wants to think through what to do next across local projects, focus on a certain project, exclude certain projects, compare project priorities, or populate project TODO.md files from planning input.
---

# Roadmap Local Tasks

Guide a short planning conversation for local projects. The goal is to surface
the user's priorities and convert them into clear `TODO.md` entries or
TODO-ready task candidates. This skill plans and records next work; it does not
implement the work unless the user explicitly asks for implementation.

## Contract

Use this skill when the user wants to gather thoughts, choose priorities, or
roadmap next steps for projects that live under `~/projects`.

Successful completion means:

- the target scope is explicit: one project, several projects, all projects, or all except named exclusions
- the user has answered focused questions about goals, constraints, and near-term outcomes
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
3. Ask concise roadmap questions.
   - Ask 3-6 questions at a time, grouped by purpose.
   - Include scope controls when missing: focus project, excluded projects, and time horizon.
   - Prefer questions that produce actionable choices: outcome, user/customer, deadline, risk, blocked decision, and first visible win.
   - For multiple projects, ask for ranking criteria before proposing a plan.
4. Convert answers into next-step options.
   - Summarize the user's direction in one short paragraph.
   - Propose 3-7 candidate TODO entries, each tied to a project and a visible outcome.
   - Mark items as `now`, `next`, or `later` when prioritization is clear.
   - Call out any unresolved decision that would change the plan.
5. Populate `TODO.md` once direction is clear.
   - Treat roadmap decisions, priorities, and "that would be good" confirmations as permission to update the relevant root `TODO.md` files.
   - Preserve existing headings and do not remove tasks; use `refresh-local-tasks` for pruning stale items.
   - If repo evidence is needed to draft concrete TODOs, use `plan-next-todos` rather than inventing implementation tasks from conversation alone.
   - Stop after updating TODOs and reporting the changed files unless the user explicitly asks to implement code.

## Question Patterns

When scope is missing, ask:

- Which project should we focus on first, or should we look across all projects?
- Are there any projects to exclude from this planning pass?
- What time horizon should this roadmap cover: today, this week, this month, or a longer push?

When one project is selected, ask:

- What outcome would make the next work session feel successful?
- Who is the next user, stakeholder, or buyer this project should serve?
- What is the biggest blocker or uncertainty right now?
- What should not be touched in this pass?

When several projects are in play, ask:

- Which criterion should drive priority: revenue, user value, maintenance risk, deadline, or personal momentum?
- Which project has the most urgent external commitment?
- Which project should intentionally receive less attention for now?

## Guardrails

- Do not assume "all projects" when the user has not specified scope; ask for focus or exclusions.
- Do not turn a roadmap conversation into a code audit unless the user asks for evidence-backed TODOs.
- Do not edit task files during the questioning phase, but do update them once the user has provided enough priority direction.
- Do not implement roadmap items from this skill alone. Populate `TODO.md`; implementation belongs to a separate explicit request.
- Do not ask for every possible detail at once; keep questions short enough to answer in chat.
- Do not invent deadlines, stakeholders, or priorities that the user has not provided.

## Output

For the first response, prefer questions over a plan when scope or intent is
unclear. Once the user answers, report:

- `Direction`: one concise summary of the chosen focus
- `TODO updates`: changed `TODO.md` files and items added, when enough direction was provided
- `Next steps`: 3-7 TODO-ready options with project names, when more confirmation is still needed before editing
- `Open decisions`: only the decisions still blocking a sharper roadmap

When files are updated, report the changed files, items added, checks run, and
commit hash when committed.
