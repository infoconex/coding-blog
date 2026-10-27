"""Regression tests for the generated HTML browser-security validator."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate_browser_security import BrowserSecurityParser


def check(html: str) -> list[str]:
    parser = BrowserSecurityParser()
    parser.feed(html)
    return parser.validate()


POLICY = "default-src 'none'; script-src 'self'; connect-src 'self' https://stats.g.doubleclick.net; base-uri 'self'; object-src 'none'; form-action 'self'"
META = '<meta http-equiv="Content-Security-Policy" content="' + POLICY + '"><meta name="referrer" content="strict-origin-when-cross-origin">'


class BrowserSecurityTests(unittest.TestCase):
    def test_external_script_and_structured_data_allowed(self):
        self.assertEqual(check('<head>' + META + '<script src="/assets/js/site.js"></script><script type="application/ld+json">{}</script></head>'), [])

    def test_missing_csp_rejected(self):
        self.assertTrue(any("missing CSP" in msg for msg in check('<html><head></head></html>')))

    def test_executable_inline_script_rejected(self):
        self.assertIn("executable inline script", check('<head>' + META + '<script>alert(1)</script></head>'))

    def test_unsafe_inline_rejected(self):
        self.assertIn("unsafe-inline permitted in script-src", check('<head>' + META.replace("script-src 'self'", "script-src 'self' 'unsafe-inline'") + '</head>'))

    def test_csp_must_precede_scripts(self):
        self.assertIn("CSP declared after a script", check('<head><script src="/site.js"></script>' + META + '</head>'))

    def test_inline_event_handlers_rejected(self):
        self.assertIn("inline event handler: onclick", check('<head>' + META + '</head><button onclick="go()">x</button>'))


if __name__ == "__main__":
    unittest.main()
