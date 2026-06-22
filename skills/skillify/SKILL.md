---
name: skillify
description: Create or improve Codex skills from repeated workflows. Use when a user wants to turn a task pattern, local procedure, tool setup, repo convention, or operating workflow into a reusable skill with a clear contract, anti-patterns, progressive disclosure, and test plan.
---

# Skillify

Use this skill to design a skill another Codex session can use without hidden
context. The output should be a small, durable skill folder, not a long essay.

## Workflow

1. Capture the repeatable workflow:
   - what a user says when they need it
   - what the agent must do
   - what successful completion looks like
   - what should explicitly not happen
2. Decide whether the workflow deserves a skill:
   - create one when the process is repeated, fragile, domain-specific, or tool-specific
   - do not create one for a one-off preference or ordinary coding pattern
3. Decide where the skill belongs before writing files:
   - create new skills under `${CODEX_HOME:-$HOME/.codex}/skills/<skill-name>` by default so the user can use them immediately
   - do not add a new skill to a shared repo merely because the current working directory is that repo
   - edit a skill inside a shared repo only when the existing installed skill is already sourced from that repo, or when the user explicitly asks to package or publish it there
   - if a skill was mistakenly created in a shared repo, copy or move it to the local skills directory, verify the local copy exists, then remove the shared copy if appropriate
4. Write a tight `SKILL.md`:
   - frontmatter must contain only `name` and `description`
   - description must include when to use the skill
   - body must include contract, workflow, guardrails, and output expectations
5. Add resources only when they reduce repeated work:
   - `scripts/` for deterministic checks or transformations
   - `references/` for details that should load only when needed
   - `assets/` for reusable output material
6. Add or update `agents/openai.yaml` with human-facing display metadata.
7. Add tests using `skill-testing` when the skill is more than a tiny wrapper.
8. Verify the skill is available immediately:
   - confirm `${CODEX_HOME:-$HOME/.codex}/skills/<skill-name>/SKILL.md` exists, or that the installed skill symlink resolves to the intended repo skill
   - inspect the resolved `SKILL.md` path, not just the path that was written
   - report the resolved install path and any validation command results back to the user

## Contract Checklist

- Name is lowercase hyphen-case and under 64 characters.
- The description is specific enough to trigger in the right situations.
- The body starts from action, not background.
- The workflow is ordered and can be executed by a fresh agent.
- Guardrails include common wrong paths and premature success claims.
- Output expectations tell the agent what to report back.
- References are linked from `SKILL.md` and loaded only when relevant.
- Placement is explicit and local by default.
- The installed skill resolves to the intended `SKILL.md` path before success is reported.

## Anti-Patterns

- Vague trigger descriptions such as "use for productivity".
- Duplicating a whole manual in `SKILL.md` instead of using references.
- Creating a skill that only says "be careful".
- Depending on local absolute paths unless the skill is intentionally personal.
- Creating a new skill in a shared repo by default.
- Assuming a written skill is usable without checking the installed or symlink-resolved path.
- Declaring success without a verification step.
- Adding broad routing language that overlaps every other skill.
