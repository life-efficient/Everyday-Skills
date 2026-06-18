#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_mcp_config.py"


class CodexMcpCliIntegrationTests(unittest.TestCase):
    def test_render_script_outputs_valid_toml_block_shape(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "Cal.com", "https://mcp.cal.com/mcp"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.stdout,
            '[mcp_servers.cal-com]\nurl = "https://mcp.cal.com/mcp"\nenabled = true\n',
        )

    def test_skill_contract_names_required_verification_steps(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("~/.codex/config.toml", skill)
        self.assertIn("codex mcp list", skill)
        self.assertIn("codex mcp login <name>", skill)
        self.assertIn("tools are callable", skill)


if __name__ == "__main__":
    unittest.main()
