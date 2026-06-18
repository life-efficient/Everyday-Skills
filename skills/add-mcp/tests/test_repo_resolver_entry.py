#!/usr/bin/env python3

import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[3]
RESOLVER = ROOT / "skills" / "RESOLVER.md"


class ResolverEntryTests(unittest.TestCase):
    def test_add_mcp_entry_present(self) -> None:
        text = RESOLVER.read_text(encoding="utf-8")
        lowered = text.lower()
        self.assertIn("hosted mcp server", lowered)
        self.assertIn("skills/add-mcp/SKILL.md", text)


if __name__ == "__main__":
    unittest.main()

