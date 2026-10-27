"""Tests for the production-only, manually triggered Lighthouse workflow."""

import io
import unittest
from unittest.mock import patch

import performance_monitor as monitor


class HomepageResponse(io.BytesIO):
    status = 200


def homepage_html():
    stylesheets = "".join(
        f'<link rel="stylesheet" href="{path}?v=123">'
        for path in monitor.EXPECTED_CSS
    )
    return (
        "<html><head>" + stylesheets +
        '<script async src="https://www.googletagmanager.com/gtag/js?id=G-test"></script>'
        '<script src="/assets/js/analytics-init.js?v=123" data-measurement-id="G-test"></script>'
        '<script src="/assets/js/clarity-init.js?v=123" data-clarity-id="test"></script></head></html>'
    )


def metric_report():
    audits = {
        key: {"numericValue": index * 100.0}
        for index, key in enumerate(monitor.AUDIT_KEYS.values(), start=1)
    }
    return {"categories": {"performance": {"score": 0.96}}, "audits": audits}


def metric_row(run, lcp=1000.0, score=96.0, css=20.0):
    return {
        "variant": "production", "run": run, "score": score,
        "fcp_ms": 900.0, "lcp_ms": lcp, "speed_index_ms": 950.0,
        "tbt_ms": 250.0, "cls": 0.0, "observed_lcp_ms": 250.0,
        "home_css_duration_ms": css, "home_css_finish_ms": 300.0,
        "slowest_css_duration_ms": css, "slowest_css_path": "/assets/css/home.css",
    }


class ProductionMonitorTests(unittest.TestCase):
    def test_preflight_accepts_live_homepage_dependencies(self):
        response = HomepageResponse(homepage_html().encode())
        with patch.object(monitor, "urlopen", return_value=response) as opened:
            monitor.validate_live_homepage()
        opened.assert_called_once()

    def test_preflight_rejects_missing_home_css(self):
        html = homepage_html().replace('href="/assets/css/home.css?v=123"', 'href="/assets/css/wrong.css?v=123"')
        with patch.object(monitor, "urlopen", return_value=HomepageResponse(html.encode())):
            with self.assertRaisesRegex(RuntimeError, "stylesheet"):
                monitor.validate_live_homepage()

    def test_preflight_rejects_noindex_homepage(self):
        html = homepage_html().replace("<head>", '<head><meta name="robots" content="noindex">')
        with patch.object(monitor, "urlopen", return_value=HomepageResponse(html.encode())):
            with self.assertRaisesRegex(RuntimeError, "indexing"):
                monitor.validate_live_homepage()

    def test_extract_metrics_uses_lighthouse_scores_and_audits(self):
        metrics = monitor.extract_metrics(metric_report())
        self.assertEqual(metrics["score"], 96.0)
        self.assertEqual(metrics["fcp_ms"], 100.0)
        self.assertEqual(metrics["cls"], 500.0)
        with self.assertRaisesRegex(RuntimeError, "Missing largest-contentful-paint"):
            report = metric_report()
            del report["audits"]["largest-contentful-paint"]
            monitor.extract_metrics(report)

    def test_report_has_no_experiment_pages_and_retains_outlier_diagnostics(self):
        rows = [metric_row(i, lcp) for i, lcp in
                enumerate((1000, 980, 3600, 950, 990), 1)]
        summary = monitor.render_report(rows, "mobile")
        self.assertIn("Production performance monitor", summary)
        self.assertIn("### Modeled LCP outliers", summary)
        self.assertIn("### Production guardrails (warning-only)", summary)
        self.assertIn("| Performance score | 96.0 points", summary)
        self.assertNotIn("experiments/analytics-impact", summary)
        self.assertNotIn("Baseline median", summary)

    def test_render_report_rejects_no_measurements(self):
        with self.assertRaisesRegex(ValueError, "empty"):
            monitor.render_report([], "mobile")


if __name__ == "__main__":
    unittest.main()
