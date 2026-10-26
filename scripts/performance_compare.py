#!/usr/bin/env python3
"""Compare two live GitHub Pages experiments using repeated Lighthouse runs."""

from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = "https://coding.infoconex.com/experiments/css-optimization/"
VARIANTS = ("baseline", "optimized")
METRICS = (
    ("Performance score", "score", "points", False),
    ("First Contentful Paint", "fcp_ms", "ms", True),
    ("Largest Contentful Paint", "lcp_ms", "ms", True),
    ("Speed Index", "speed_index_ms", "ms", True),
    ("Total Blocking Time", "tbt_ms", "ms", True),
    ("Cumulative Layout Shift", "cls", "", True),
)
AUDIT_KEYS = {
    "fcp_ms": "first-contentful-paint",
    "lcp_ms": "largest-contentful-paint",
    "speed_index_ms": "speed-index",
    "tbt_ms": "total-blocking-time",
    "cls": "cumulative-layout-shift",
}


def ensure_pages_are_available() -> None:
    for variant in VARIANTS:
        url = f"{BASE_URL}{variant}/"
        request = Request(url, headers={"User-Agent": "coding-blog-performance-comparison/1.0"})
        try:
            with urlopen(request, timeout=30) as response:
                status = response.status
                html = response.read(100_000).decode("utf-8", errors="replace")
                if status != 200 or '<meta name="robots" content="noindex">' not in html:
                    raise RuntimeError(f"Unexpected experimental page response: {url} (HTTP {status})")
        except (HTTPError, URLError) as exc:
            raise RuntimeError(f"Experiment page unavailable: {url}: {exc}") from exc
        print(f"Verified live page: {url}", flush=True)


def extract_metrics(report: Path) -> dict[str, float]:
    data = json.loads(report.read_text(encoding="utf-8"))
    if data.get("runtimeError"):
        raise RuntimeError(f"Lighthouse runtime error in {report}: {data['runtimeError']}")
    category = data.get("categories", {}).get("performance", {})
    if category.get("score") is None:
        raise RuntimeError(f"No performance score in {report}")
    result = {"score": round(category["score"] * 100, 2)}
    for name, audit_key in AUDIT_KEYS.items():
        number = data.get("audits", {}).get(audit_key, {}).get("numericValue")
        if not isinstance(number, (int, float)):
            raise RuntimeError(f"Missing {audit_key} measurement in {report}")
        result[name] = float(number)
    return result


def run_lighthouse(url: str, destination: Path, device: str) -> None:
    args = [
        "lighthouse",
        url,
        "--only-categories=performance",
        "--output=json",
        f"--output-path={destination}",
        "--chrome-flags=--headless --no-sandbox --disable-dev-shm-usage",
        "--quiet",
    ]
    if device == "desktop":
        args.append("--preset=desktop")
    result = subprocess.run(args, text=True, capture_output=True, timeout=240, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            f"Lighthouse failed for {url} (exit {result.returncode}):\n"
            f"{result.stderr[-3000:]}\n{result.stdout[-1000:]}"
        )
    if not destination.is_file():
        raise RuntimeError(f"Lighthouse did not create {destination}")


def render_report(rows: list[dict], device: str) -> str:
    variants = {variant: [row for row in rows if row["variant"] == variant] for variant in VARIANTS}
    lines = [
        f"# Live CSS performance comparison — {device}",
        "",
        "Five alternating Lighthouse runs per URL, on the same GitHub-hosted runner.",
        "The baseline loads five CSS files; optimized loads one combined file.",
        "Both experimental pages omit Google Analytics and Microsoft Clarity and have noindex.",
        "Lower is better for timing and layout-shift metrics; higher is better for Performance score.",
        "",
        "| Metric | Baseline median | Optimized median | Difference (optimized − baseline) |",
        "| --- | ---: | ---: | ---: |",
    ]
    for label, key, unit, _lower_is_better in METRICS:
        before = statistics.median(row[key] for row in variants["baseline"])
        after = statistics.median(row[key] for row in variants["optimized"])
        decimals = 3 if key == "cls" else 1

        def formatted(v: float, signed: bool = False) -> str:
            sign = "+" if signed and v > 0 else ""
            return f"{sign}{v:.{decimals}f}{(' ' + unit) if unit else ''}"

        lines.append(
            f"| {label} | {formatted(before)} | {formatted(after)} | {formatted(after - before, signed=True)} |"
        )
    lines += [
        "",
        "**Interpretation:** Medians reduce single-run noise but do not eliminate it. Confirm any meaningful change with repeated runs and a production validation before deploying.",
        "",
        "### Tested URLs",
        f"- Baseline: {BASE_URL}baseline/",
        f"- Optimized: {BASE_URL}optimized/",
        "",
        "The full JSON runs and CSV measurements are available as a GitHub Actions artifact.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("mobile", "desktop"), default="mobile")
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--output-dir", type=Path, default=Path("performance-reports"))
    args = parser.parse_args()
    if not 1 <= args.runs <= 10:
        parser.error("--runs must be between 1 and 10")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    ensure_pages_are_available()
    rows = []
    for pair in range(1, args.runs + 1):
        # Alternate order to avoid consistently favoring whichever page is tested second.
        order = VARIANTS if pair % 2 == 1 else tuple(reversed(VARIANTS))
        for variant in order:
            url = f"{BASE_URL}{variant}/"
            filename = f"{args.device}-pair-{pair:02d}-{variant}.json"
            print(f"Pair {pair}/{args.runs}: testing {variant} ({args.device})", flush=True)
            run_lighthouse(url, args.output_dir / filename, args.device)
            metrics = extract_metrics(args.output_dir / filename)
            rows.append({"pair": pair, "variant": variant, "device": args.device, **metrics})
            print(f"  Performance {metrics['score']:.0f}; LCP {metrics['lcp_ms']:.0f} ms; Speed Index {metrics['speed_index_ms']:.0f} ms", flush=True)
            time.sleep(2)

    csv_path = args.output_dir / "measurements.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary = render_report(rows, args.device)
    (args.output_dir / "summary.md").write_text(summary, encoding="utf-8")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as handle:
            handle.write(summary + "\n")
    print(summary)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, subprocess.TimeoutExpired, ValueError) as exc:
        print(f"Comparison failed: {exc}", file=sys.stderr)
        sys.exit(1)
