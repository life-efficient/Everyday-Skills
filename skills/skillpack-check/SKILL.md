---
name: skillpack-check
description: Audit a repository or folder of Codex skills before publishing. Use when checking a skills pack for missing resolver entries, invalid skill frontmatter, stale agents metadata, placeholder text, non-portable tests, dead resource directories, and release readiness.
---

# Skillpack Check

Use this skill for the whole pack, not for rewriting one skill. It should leave
the repo closer to being installable by another agent.

## Workflow

1. Inventory skills:
   - list every `skills/*/SKILL.md`
   - confirm each skill has an `agents/openai.yaml` unless intentionally omitted
   - confirm `skills/RESOLVER.md` mentions every skill
2. Run deterministic checks:
   - `python3 tests/check_skillpack.py` when present
   - run each skill's local unit tests when present
   - run script-specific tests for bundled scripts
3. Inspect portability:
   - no absolute user paths in reusable tests
   - no secrets or tokens
   - no machine-specific MCP registrations as required test fixtures
   - no generated caches committed
4. Inspect quality:
   - no placeholders
   - no broad "use for anything" descriptions
   - guardrails name real anti-patterns
   - verification steps match what the skill can actually check
5. Report release status:
   - ready
   - ready with caveats
   - blocked, with exact files and fixes

## Guardrails

- Do not expand a reusable skills repo with product-specific skills.
- Do not treat local installation success as proof the pack is portable.
- Do not keep failing environment-dependent tests in the default test suite.
- Do not publish until generated caches and secrets are absent.

## Output

Report:
- skill count
- checks run
- failures fixed
- remaining blockers
- suggested next release step
