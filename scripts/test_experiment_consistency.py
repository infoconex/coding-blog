"""Ensure analytics experiment pages retain production homepage dependencies.

Runs with Python's standard library as part of GitHub Pages and CI validation.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYTICS_PAGES = (
    "experiments/analytics-impact/none/index.html",
    "experiments/analytics-impact/google/index.html",
    "experiments/analytics-impact/clarity/index.html",
    "experiments/analytics-impact/both/index.html",
    "experiments/google-timing/current/index.html",
    "experiments/google-timing/after-load/index.html",
)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def frontmatter_and_body(text: str) -> tuple[str, str]:
    match = re.match(r"\A---\n(?P<frontmatter>.*?)\n---\n(?P<body>.*)\Z", text, re.DOTALL)
    if match is None:
        raise AssertionError("Missing or malformed Jekyll frontmatter")
    return match.group("frontmatter"), match.group("body")


def field(frontmatter: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}: (.*)$", frontmatter)
    if match is None:
        raise AssertionError(f"Missing frontmatter field: {key}")
    return match.group(1).strip()


def css_dependencies(layout: str) -> tuple[str, ...]:
    """Compare shared stylesheet declarations in the same order."""
    return tuple(re.findall(r"'/assets/css/([a-z-]+\.css)'", layout))


class ExperimentConsistencyTests(unittest.TestCase):
    def test_experiment_home_markup_matches_production(self):
        _, homepage = frontmatter_and_body(read("index.html"))
        self.assertEqual(homepage, read("_includes/css-experiment-home.html"))

    def test_experiment_page_stylesheet_and_metadata_match_home(self):
        production_fm, _ = frontmatter_and_body(read("index.html"))
        stylesheet = field(production_fm, "stylesheet")
        self.assertEqual(stylesheet, "/assets/css/home.css")
        for path in ANALYTICS_PAGES:
            with self.subTest(path=path):
                frontmatter, body = frontmatter_and_body(read(path))
                self.assertEqual(field(frontmatter, "layout"), "analytics-experiment")
                self.assertEqual(field(frontmatter, "stylesheet"), stylesheet)
                self.assertEqual(field(frontmatter, "sitemap"), "false")
                self.assertEqual(body.strip(), "{% include css-experiment-home.html %}")

    def test_analytics_layout_matches_production_css(self):
        production = read("_layouts/default.html")
        experiment = read("_layouts/analytics-experiment.html")
        self.assertEqual(css_dependencies(production), css_dependencies(experiment))
        self.assertIn("{% if page.stylesheet %}", production)
        self.assertIn("{% if page.stylesheet %}", experiment)
        self.assertIn('<meta name="robots" content="noindex">', experiment)
        self.assertIn("{% include analytics.html %}", production)
        self.assertIn("{% include analytics-experiment.html %}", experiment)


if __name__ == "__main__":
    unittest.main()
