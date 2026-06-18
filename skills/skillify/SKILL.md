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
3. Write a tight `SKILL.md`:
   - frontmatter must contain only `name` and `description`
   - description must include when to use the skill
   - body must include contract, workflow, guardrails, and output expectations
4. Add resources only when they reduce repeated work:
   - `scripts/` for deterministic checks or transformations
   - `references/` for details that should load only when needed
   - `assets/` for reusable output material
5. Add or update `agents/openai.yaml` with human-facing display metadata.
6. Add tests using `skill-testing` when the skill is more than a tiny wrapper.

## Contract Checklist

- Name is lowercase hyphen-case and under 64 characters.
- The description is specific enough to trigger in the right situations.
- The body starts from action, not background.
- The workflow is ordered and can be executed by a fresh agent.
- Guardrails include common wrong paths and premature success claims.
- Output expectations tell the agent what to report back.
- References are linked from `SKILL.md` and loaded only when relevant.

## Anti-Patterns

- Vague trigger descriptions such as "use for productivity".
- Duplicating a whole manual in `SKILL.md` instead of using references.
- Creating a skill that only says "be careful".
- Depending on local absolute paths unless the skill is intentionally personal.
- Declaring success without a verification step.
- Adding broad routing language that overlaps every other skill.
