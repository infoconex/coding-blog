"""Regression tests for long-term Lighthouse issue history tracking."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).parent))
from performance_history import FIELDS, MARKER, metric_delta, parse_history, previous_record, read_medians, render_comment


class LighthouseHistoryTests(unittest.TestCase):
    def test_read_five_median_samples_per_device(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "reports"
            directory = root / "production-performance-mobile-5"
            directory.mkdir(parents=True)
            with (directory / "measurements.csv").open("w", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["run", "device", "variant", *FIELDS])
                writer.writeheader()
                for run, score in enumerate((94, 98, 97, 96, 99), 1):
                    writer.writerow({
                        "run": run, "device": "mobile", "variant": "production",
                        "score": score, "fcp_ms": 800 + run * 10,
                        "lcp_ms": 1000 + run * 10, "speed_index_ms": 1100 + run * 10,
                        "tbt_ms": 120 + run * 10, "cls": 0,
                    })
            row, = read_medians(root)
            self.assertEqual(row["score"], 97)
            self.assertEqual(row["lcp_ms"], 1030)
            self.assertEqual(row["count"], 5)
            self.assertEqual(row["device"], "mobile")

    def test_reject_partial_run(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp) / "production-performance-mobile-2"
            directory.mkdir()
            (directory / "measurements.csv").write_text("run,device,variant,score\n1,mobile,production,99\n")
            with self.assertRaisesRegex(ValueError, "Expected 5 samples"):
                read_medians(Path(temp))

    def test_extract_and_compare_history(self):
        record = {
            "run_id": 3, "date": "2026-10-27T06:58:05Z", "device": "mobile",
            "score": 98, "fcp_ms": 900, "lcp_ms": 930,
            "speed_index_ms": 940, "tbt_ms": 175, "cls": 0,
        }
        body = f"Historical run\n<!-- coding-performance-history {json.dumps(record)} -->"
        parsed = parse_history([{"body": body}, {"body": "no history"}])
        self.assertEqual(parsed, [record])
        self.assertEqual(previous_record(parsed, "mobile", 4), record)
        self.assertIsNone(previous_record(parsed, "desktop", 4))
        self.assertEqual(metric_delta(900, 930, " ms"), "-30.0 ms")
        output = render_comment([{**record, "run_id": 4, "lcp_ms": 900}], parsed,
                                "https://github.com/infoconex/coding-blog/actions/runs/4", "schedule")
        self.assertIn("mobile", output)
        self.assertIn("-30.0 ms", output)
        self.assertEqual(len(MARKER.findall(output)), 1)


if __name__ == "__main__":
    unittest.main()
