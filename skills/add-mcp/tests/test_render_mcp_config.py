#!/usr/bin/env python3

import importlib.util
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "render_mcp_config.py"
SPEC = importlib.util.spec_from_file_location("render_mcp_config", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class RenderMcpConfigTests(unittest.TestCase):
    def test_normalizes_name(self) -> None:
        self.assertEqual(MODULE.normalize_name("Cal.com"), "cal-com")
        self.assertEqual(MODULE.normalize_name(" Cloudflare API "), "cloudflare-api")

    def test_renders_block(self) -> None:
        block = MODULE.render_block("calcom", "https://mcp.cal.com/mcp")
        self.assertEqual(
            block,
            '[mcp_servers.calcom]\nurl = "https://mcp.cal.com/mcp"\nenabled = true\n',
        )

    def test_rejects_invalid_url(self) -> None:
        with self.assertRaises(ValueError):
            MODULE.render_block("calcom", "mcp.cal.com/mcp")


if __name__ == "__main__":
    unittest.main()
