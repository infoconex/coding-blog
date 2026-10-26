"""Regression tests for IndexNow experiment URL exclusions."""

from __future__ import annotations

import io
import json
import unittest
from unittest.mock import patch

import indexnow


class Response(io.BytesIO):
    status = 202


class IndexNowExperimentExclusionTests(unittest.TestCase):
    def test_experiment_paths_are_ignored_before_site_wide_detection(self):
        changes = [
            ("A", ["experiments/css-optimization/baseline/index.html"]),
            ("M", ["_layouts/css-experiment.html"]),
            ("M", ["_includes/css-experiment-home.html"]),
        ]
        with patch.object(indexnow, "changed_paths", return_value=changes):
            urls, site_wide = indexnow.collect_changed_urls(
                "https://coding.infoconex.com", "old", "new"
            )
        self.assertFalse(site_wide)
        self.assertEqual(urls, set())

    def test_excluded_url_prefix_is_path_scoped(self):
        self.assertTrue(indexnow.is_excluded_url("https://coding.infoconex.com/experiments"))
        self.assertTrue(indexnow.is_excluded_url("https://coding.infoconex.com/experiments/analytics/ga/"))
        self.assertFalse(indexnow.is_excluded_url("https://coding.infoconex.com/post/experiments-explained/"))
        self.assertFalse(indexnow.is_excluded_url("https://coding.infoconex.com/"))

    def test_full_sitemap_backfill_excludes_experiments(self):
        xml = b"""<?xml version="1.0"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
          <url><loc>https://coding.infoconex.com/</loc></url>
          <url><loc>https://coding.infoconex.com/experiments/css-optimization/baseline/</loc></url>
          <url><loc>https://unrelated.example/post/</loc></url>
        </urlset>"""
        with patch.object(indexnow.urllib.request, "urlopen", return_value=Response(xml)):
            self.assertEqual(indexnow.sitemap_urls("https://coding.infoconex.com"),
                             {"https://coding.infoconex.com/"})

    def test_final_submission_gate_removes_experiments(self):
        submissions = []

        def fake_post(request, timeout=30):
            submissions.append(json.loads(request.data.decode("utf-8")))
            return Response()

        with patch.object(indexnow.urllib.request, "urlopen", side_effect=fake_post):
            indexnow.submit_urls(
                "https://coding.infoconex.com",
                "dummy-key",
                "https://coding.infoconex.com/dummy-key.txt",
                {
                    "https://coding.infoconex.com/experiments/css-optimization/optimized/",
                    "https://coding.infoconex.com/archive/",
                },
            )
        self.assertEqual(len(submissions), 1)
        self.assertEqual(submissions[0]["urlList"], ["https://coding.infoconex.com/archive/"])

    def test_only_experiments_produces_no_post(self):
        with patch.object(indexnow.urllib.request, "urlopen") as urlopen:
            indexnow.submit_urls(
                "https://coding.infoconex.com",
                "dummy-key",
                "https://coding.infoconex.com/dummy-key.txt",
                {"https://coding.infoconex.com/experiments/css-optimization/baseline/"},
            )
        urlopen.assert_not_called()


if __name__ == "__main__":
    unittest.main()
