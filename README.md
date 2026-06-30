# Everyday Skills

Copy this into a new agent thread before asking it to install or use this repo:

```text
Install the Everyday Skills by following https://github.com/life-efficient/Everyday-Skills/blob/main/INSTALL_FOR_AGENTS.md.
```

Reusable Codex skills for general agent workflows that are not specific to a
single product or knowledge base.

## Included skills

- `add-mcp`: Add a hosted MCP server to Codex using `~/.codex/config.toml`,
  authenticate it when needed, and verify the tools are callable.
- `fanout-local-tasks`: Fan out root-level local project TODO items into Codex
  threads with concise handoff prompts.
- `in-parallel`: Split separable work across parallel Codex threads or subagents,
  then integrate and verify the results.
- `local-whats-next`: Summarize root-level local project TODO items as a
  concise numbered what's-next snapshot split by inferred execution mode before
  optional fanout.
- `roadmap-local-tasks`: Ask focused roadmap questions to choose local project
  priorities, evidence-backed next TODOs, and next-step options.
- `skillify`: Turn a repeated workflow into a concise, testable Codex skill.
- `skill-testing`: Validate one skill for structure, anti-patterns, metadata
  drift, and realistic task behavior.
- `skillpack-check`: Audit a repo of skills before release.
- `refresh-local-tasks`: Check local project task lists against the current repo, remove
  completed or stale items, and rewrite vague tasks into specific remaining work.

## Install locally

Symlink the skills you want into the active skills directory. Agent-facing
install steps are also available in `INSTALL_FOR_AGENTS.md`.

```bash
repo_root="$(pwd)"
skills_dir="${CODEX_HOME:-$HOME/.codex}/skills"

mkdir -p "$skills_dir"
ln -sfn "$repo_root/skills/add-mcp" "$skills_dir/add-mcp"
ln -sfn "$repo_root/skills/fanout-local-tasks" "$skills_dir/fanout-local-tasks"
ln -sfn "$repo_root/skills/in-parallel" "$skills_dir/in-parallel"
ln -sfn "$repo_root/skills/local-whats-next" "$skills_dir/local-whats-next"
ln -sfn "$repo_root/skills/roadmap-local-tasks" "$skills_dir/roadmap-local-tasks"
ln -sfn "$repo_root/skills/skillify" "$skills_dir/skillify"
ln -sfn "$repo_root/skills/skill-testing" "$skills_dir/skill-testing"
ln -sfn "$repo_root/skills/skillpack-check" "$skills_dir/skillpack-check"
ln -sfn "$repo_root/skills/refresh-local-tasks" "$skills_dir/refresh-local-tasks"
```

## Check before shipping

```bash
python3 tests/check_skillpack.py
python3 -m unittest discover -s skills/add-mcp/tests
```
