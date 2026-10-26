"""Regression tests for enhanced Lighthouse diagnostics and production checks."""

import unittest

import performance_diagnostics as diag
import performance_monitor


def lighthouse_fixture():
    return {
        "audits": {
            "largest-contentful-paint": {"numericValue": 2777.0},
            "metrics": {"details": {"items": [
                {"observedLargestContentfulPaint": 298.0}
            ]}},
            "lcp-breakdown-insight": {"details": {"items": [
                {"type": "table", "items": []},
                {"type": "node", "nodeLabel": "Software engineering headline"},
            ]}},
            "network-requests": {"details": {"items": [
                {
                    "url": "https://coding.infoconex.com/assets/css/home.css?v=123",
                    "resourceType": "Stylesheet",
                    "networkRequestTime": 103.0,
                    "networkEndTime": 234.0,
                    "transferSize": 2999,
                    "statusCode": 200,
                },
                {
                    "url": "https://coding.infoconex.com/assets/css/site.css?v=123",
                    "resourceType": "Stylesheet",
                    "networkRequestTime": 102.0,
                    "networkEndTime": 130.0,
                    "transferSize": 2100,
                    "statusCode": 200,
                },
                {
                    "url": "https://www.googletagmanager.com/gtag/js?id=x",
                    "resourceType": "Script",
                    "networkRequestTime": 100.0,
                    "networkEndTime": 800.0,
                },
            ]}},
        },
    }


def row(variant, pair, lcp, score=95, tbt=200, cls=0, observed=300, css=20):
    return {
        "variant": variant, "run": pair, "lcp_ms": lcp,
        "fcp_ms": lcp, "speed_index_ms": lcp, "score": score,
        "tbt_ms": tbt, "cls": cls, "observed_lcp_ms": observed,
        "home_css_duration_ms": css,
        "home_css_finish_ms": css + 100,
        "slowest_css_path": "/assets/css/home.css",
        "slowest_css_duration_ms": css,
    }


class LighthouseDiagnosticsTests(unittest.TestCase):
    def test_extracts_observed_and_modeled_lcp_and_css_network_times(self):
        parsed = diag.diagnostics(lighthouse_fixture())
        self.assertEqual(parsed["observed_lcp_ms"], 298)
        self.assertEqual(parsed["lcp_model_gap_ms"], 2479)
        self.assertEqual(parsed["home_css_duration_ms"], 131)
        self.assertEqual(parsed["home_css_finish_ms"], 234)
        self.assertEqual(parsed["slowest_css_path"], "/assets/css/home.css")
        self.assertEqual(parsed["stylesheet_count"], 2)
        self.assertEqual(parsed["lcp_element"], "Software engineering headline")
        self.assertEqual(len(diag.stylesheet_requests(lighthouse_fixture())), 2)

    def test_missing_browser_trace_data_is_reported_as_missing(self):
        parsed = diag.diagnostics({"audits": {"largest-contentful-paint": {"numericValue": 900}}})
        self.assertIsNone(parsed["observed_lcp_ms"])
        self.assertIsNone(parsed["home_css_duration_ms"])
        self.assertIsNone(parsed["slowest_css_duration_ms"])
        self.assertEqual(parsed["stylesheet_count"], 0)

    def test_single_lcp_outlier_does_not_trigger_median_guardrail(self):
        rows = [row("production", i, lcp) for i, lcp in
                enumerate((2777, 900, 905, 904, 901), 1)]
        checks = diag.guardrail_checks(rows)
        self.assertTrue(all(check["status"] == "PASS" for check in checks))
        self.assertEqual(len(diag.outlier_rows(rows)), 1)
        report = performance_monitor.render_report(rows, "mobile")
        self.assertIn("### Per-run loading diagnostics", report)
        self.assertIn("### Modeled LCP outliers", report)
        self.assertIn("### Production guardrails (warning-only)", report)
        self.assertIn("298", str(diag.diagnostics(lighthouse_fixture())))
        self.assertIn("**PASS**", report)

    def test_sustained_regression_warns_on_median(self):
        rows = [row("production", i, lcp, score=85, tbt=700)
                for i, lcp in enumerate((3100, 2900, 2750, 900, 920), 1)]
        checks = diag.guardrail_checks(rows)
        checks_by_label = {check["label"]: check for check in checks}
        self.assertEqual(checks_by_label["Modeled LCP"]["status"], "WARN")
        self.assertEqual(checks_by_label["Modeled LCP"]["affected"], 3)
        self.assertEqual(checks_by_label["Performance score"]["status"], "WARN")
        self.assertEqual(checks_by_label["Total Blocking Time"]["status"], "WARN")
        self.assertEqual(checks_by_label["Layout shift"]["status"], "PASS")
        self.assertEqual(diag.guardrail_checks([row("experiment", 1, 900)]), [])

    def test_raw_css_missing_end_time_does_not_invent_duration(self):
        sample = lighthouse_fixture()
        sample["audits"]["network-requests"]["details"]["items"][0].pop("networkEndTime")
        row0 = diag.stylesheet_requests(sample)[0]
        self.assertIsNone(row0["request_end_ms"])
        self.assertIsNone(row0["request_duration_ms"])


if __name__ == "__main__":
    unittest.main()
