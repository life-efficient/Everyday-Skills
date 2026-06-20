# Install for Agents

Use these steps from the root of a local checkout of this repo.

## Install

```bash
repo_root="$(pwd)"
skills_dir="${CODEX_HOME:-$HOME/.codex}/skills"

mkdir -p "$skills_dir"
ln -sfn "$repo_root/skills/add-mcp" "$skills_dir/add-mcp"
ln -sfn "$repo_root/skills/fanout-local-tasks" "$skills_dir/fanout-local-tasks"
ln -sfn "$repo_root/skills/plan-next-todos" "$skills_dir/plan-next-todos"
ln -sfn "$repo_root/skills/skillify" "$skills_dir/skillify"
ln -sfn "$repo_root/skills/skill-testing" "$skills_dir/skill-testing"
ln -sfn "$repo_root/skills/skillpack-check" "$skills_dir/skillpack-check"
ln -sfn "$repo_root/skills/refresh-local-tasks" "$skills_dir/refresh-local-tasks"
```

## Verify

```bash
python3 tests/check_skillpack.py
python3 -m unittest discover -s skills/add-mcp/tests
```

Do not replace `$HOME` or `CODEX_HOME` with a machine-specific absolute path in
committed docs or scripts.
