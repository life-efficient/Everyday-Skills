---
name: skill-testing
description: Test a Codex skill before shipping or after edits. Use when validating a skill folder, checking frontmatter and agents metadata, finding anti-patterns, testing bundled scripts, reviewing resolver coverage, or designing realistic forward tests for a skill contract.
---

# Skill Testing

Use this skill to test whether a skill will help a fresh agent do the right
thing. Prefer concrete checks over abstract review.

## Test Layers

1. Structure:
   - `SKILL.md` exists
   - frontmatter has `name` and `description`
   - no placeholder text remains
   - skill folder name matches the skill name
2. Trigger quality:
   - description says what the skill does
   - description says when to use it
   - trigger scope is neither vague nor overbroad
3. Contract quality:
   - success criteria are explicit
   - verification steps are named
   - guardrails cover likely wrong paths
   - output format is clear enough for handoff
4. Resource quality:
   - scripts run successfully on representative inputs
   - references are linked from `SKILL.md`
   - assets are necessary and not dead weight
5. Integration:
   - resolver points to the skill
   - `agents/openai.yaml` default prompt names `$skill-name`
   - repo-level tests include the skill
6. Forward behavior:
   - run or design one realistic prompt that should trigger the skill
   - run or design one adjacent prompt that should not trigger it

## Anti-Patterns

- Passing validation while leaving a vague contract.
- Testing only frontmatter for a workflow-heavy skill.
- Keeping environment-specific tests in a reusable skill repo.
- Leaking the expected answer into a forward test.
- Treating a missing script test as acceptable when the script performs the fragile part.

## Output

Report:
- checks run
- failures found
- files that need edits
- residual risk if no forward test was run
