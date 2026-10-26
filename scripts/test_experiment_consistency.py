"""Guard against accidentally re-publishing retired performance experiments.

Kept at this path because the existing Pages build already runs it.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RETIRED_SOURCES = (
    "_layouts/css-experiment.html",
    "_layouts/analytics-experiment.html",
    "_includes/css-experiment-home.html",
    "_includes/analytics-experiment.html",
)


class RetiredExperimentTests(unittest.TestCase):
    def test_no_live_experiment_pages_or_assets(self):
        experiments = ROOT / "experiments"
        self.assertFalse(experiments.exists(), "Retired experiments must not be published")

    def test_retired_layouts_and_includes_are_absent(self):
        for relative in RETIRED_SOURCES:
            with self.subTest(file=relative):
                self.assertFalse((ROOT / relative).exists())

    def test_production_homepage_still_loads_normal_assets(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        layout = (ROOT / "_layouts/default.html").read_text(encoding="utf-8")
        self.assertRegex(index, r"(?m)^stylesheet: /assets/css/home\.css$")
        self.assertIn("{% include analytics.html %}", layout)
        for stylesheet in ("site.css", "themes.css", "search.css", "mobile-header.css"):
            self.assertIn("/assets/css/" + stylesheet, layout)

    def test_historical_experiment_urls_remain_excluded_from_indexnow(self):
        import indexnow

        self.assertTrue(indexnow.is_excluded_url(
            "https://coding.infoconex.com/experiments/google-timing/current/"))
        self.assertTrue(indexnow.is_ignored_path(
            "experiments/analytics-impact/both/index.html"))
        for relative in RETIRED_SOURCES:
            self.assertTrue(indexnow.is_ignored_path(relative))


if __name__ == "__main__":
    unittest.main()
