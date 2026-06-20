---
name: refresh-local-tasks
description: Refresh and enrich local project TODO.md files when a user asks to check whether outstanding tasks are stale, already completed, too vague, or need more specific next steps.
---

# Refresh Local Tasks

Refresh a local project task list against the current repository state. The goal is a
cleaner `TODO.md`, not a broad roadmap rewrite.

## Contract

Use this skill when the user asks to maintain, refresh, enrich, prune, or check
staleness in a local project `TODO.md` or similar root task list.

Successful completion means:

- completed tasks are removed only after concrete code, docs, or test evidence
- partially completed tasks are rewritten to name the remaining gap
- vague tasks are made more specific and verifiable
- still-valid tasks are left in place unless clearer wording is useful
- the final report names what changed and what evidence was used

## Workflow

1. Identify the target project and task file.
   - Prefer the current repo if the user is already in one.
   - For named projects, look under `~/projects/<name>` first.
   - If several task files exist, prioritize the root `TODO.md` unless the user named another file.
2. Read the full task file and group tasks by section.
3. Check repository state before editing.
   - Inspect relevant code, docs, tests, package scripts, and recent commits.
   - Use fast targeted search first, then open the files that actually prove or disprove each task.
   - Treat docs-only evidence as enough only for documentation tasks.
4. Classify each task.
   - `complete`: implementation or documentation clearly exists and is verified.
   - `partial`: some requested capability exists, but a concrete gap remains.
   - `stale`: the task no longer matches the project direction or current architecture.
   - `unclear`: the task cannot be acted on without a sharper target.
   - `valid`: still accurate and already specific enough.
5. Edit the task file.
   - Remove `complete` items.
   - Delete or reframe `stale` items with evidence.
   - Rewrite `partial` and `unclear` items into specific remaining work.
   - Merge duplicate items when the same underlying gap appears in multiple sections.
6. Verify the edit.
   - Review the diff.
   - Run formatting or lightweight repository checks when relevant.
   - For task-file-only edits, a whitespace diff check is usually sufficient.
7. Commit if the repo convention or user instruction calls for regular commits.

## Guardrails

- Do not remove a task because it "sounds done"; cite code, docs, tests, or command output.
- Do not turn the task list into a status report. Keep it as future work.
- Do not broaden a task while "enriching" it. Make the remaining work narrower and easier to verify.
- Do not mix unrelated cleanup into the task refresh.
- Do not overwrite user changes in a dirty worktree; inspect and work with them.
- Do not rely only on memory for facts that are cheap to verify in the repo.

## Output

Report briefly:

- task file updated
- completed or stale items removed
- partial or vague items rewritten
- checks run
- commit hash, if committed
- any remaining uncertainty

Prefer concise bullets over a long audit log.
