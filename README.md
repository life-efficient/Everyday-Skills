# Everyday Skills

Reusable Codex skills for general agent workflows that are not specific to a
single product or knowledge base.

## Included skills

- `add-mcp`: Add a hosted MCP server to Codex using `~/.codex/config.toml`,
  authenticate it when needed, and verify the tools are callable.
- `skillify`: Turn a repeated workflow into a concise, testable Codex skill.
- `skill-testing`: Validate one skill for structure, anti-patterns, metadata
  drift, and realistic task behavior.
- `skillpack-check`: Audit a repo of skills before release.
- `todo-refresh`: Check project task lists against the current repo, remove
  completed or stale items, and rewrite vague tasks into specific remaining work.

## Install locally

Symlink the skills you want into the active skills directory:

```bash
repo_root="$(pwd)"
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -sfn "$repo_root/skills/add-mcp" "${CODEX_HOME:-$HOME/.codex}/skills/add-mcp"
ln -sfn "$repo_root/skills/skillify" "${CODEX_HOME:-$HOME/.codex}/skills/skillify"
ln -sfn "$repo_root/skills/skill-testing" "${CODEX_HOME:-$HOME/.codex}/skills/skill-testing"
ln -sfn "$repo_root/skills/skillpack-check" "${CODEX_HOME:-$HOME/.codex}/skills/skillpack-check"
ln -sfn "$repo_root/skills/todo-refresh" "${CODEX_HOME:-$HOME/.codex}/skills/todo-refresh"
```

## Check before shipping

```bash
python3 tests/check_skillpack.py
python3 -m unittest discover -s skills/add-mcp/tests
```
