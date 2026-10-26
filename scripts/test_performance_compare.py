"""Unit tests for report summaries and experiment configurations."""

import unittest

import performance_compare


def row(variant, fcp, lcp, score=100, speed=None, tbt=0, cls=0):
    return {
        "pair": 1, "variant": variant, "device": "mobile",
        "fcp_ms": fcp, "lcp_ms": lcp, "speed_index_ms": speed or lcp,
        "tbt_ms": tbt, "cls": cls, "score": score,
    }


class PerformanceExperimentTests(unittest.TestCase):
    def test_css_report_includes_improvement(self):
        rows = [row("baseline", 1000, 1200), row("optimized", 900, 1100)]
        report = performance_compare.render_report(rows, "mobile", "css")
        self.assertIn("Difference (optimized − baseline)", report)
        self.assertIn("-100.0 ms", report)
        self.assertIn("CSS performance comparison", report)

    def test_analytics_has_four_distinct_variants(self):
        variants = performance_compare.EXPERIMENTS["analytics"]["variants"]
        self.assertEqual(variants, ("none", "google", "clarity", "both"))
        self.assertEqual(len(variants), len(set(variants)))

    def test_analytics_report_includes_four_medians_and_differences(self):
        rows = [
            row("none", 800, 900),
            row("google", 950, 1100),
            row("clarity", 870, 1000),
            row("both", 1100, 1400),
        ]
        report = performance_compare.render_report(rows, "mobile", "analytics")
        self.assertIn("Google median", report)
        self.assertIn("Clarity median", report)
        self.assertIn("Both median", report)
        self.assertIn("+200.0 ms", report)
        self.assertIn("+500.0 ms", report)
        self.assertIn("Change relative to no tracking", report)

    def test_missing_variant_is_error(self):
        with self.assertRaises(ValueError):
            performance_compare.render_report([row("none", 800, 900)], "mobile", "analytics")


if __name__ == "__main__":
    unittest.main()
