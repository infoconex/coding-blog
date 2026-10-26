#!/usr/bin/env python3
"""Run repeated Lighthouse measurements against the production homepage only.

Manual GitHub Actions workflow. Warnings are lab heuristics and never block deployment.
No experiments, public reports, or site content are generated.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import statistics
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from performance_diagnostics import diagnostics, guardrail_checks, outlier_rows, stylesheet_requests

PRODUCTION_URL = "https://coding.infoconex.com/"
EXPECTED_CSS = (
    "/assets/css/site.css",
    "/assets/css/themes.css",
    "/assets/css/search.css",
    "/assets/css/mobile-header.css",
    "/assets/css/home.css",
)
METRICS = (
    ("Performance score", "score", "points"),
    ("First Contentful Paint", "fcp_ms", "ms"),
    ("Largest Contentful Paint (modeled)", "lcp_ms", "ms"),
    ("Speed Index", "speed_index_ms", "ms"),
    ("Total Blocking Time", "tbt_ms", "ms"),
    ("Cumulative Layout Shift", "cls", ""),
)
AUDIT_KEYS = {
    "fcp_ms": "first-contentful-paint",
    "lcp_ms": "largest-contentful-paint",
    "speed_index_ms": "speed-index",
    "tbt_ms": "total-blocking-time",
    "cls": "cumulative-layout-shift",
}


def validate_live_homepage():
    request = Request(PRODUCTION_URL, headers={"User-Agent": "coding-blog-production-monitor/1.0"})
    try:
        with urlopen(request, timeout=30) as response:
            status = response.status
            html = response.read(200_000).decode("utf-8", errors="replace")
    except (HTTPError, URLError) as exc:
        raise RuntimeError(f"Production homepage unavailable: {exc}") from exc

    if status != 200 or '<meta name="robots" content="noindex">' in html:
        raise RuntimeError(f"Unexpected production homepage status/indexing directive: {status}")
    hrefs = re.findall(r'<link rel="stylesheet" href="([^"]+)"', html)
    loaded_css = tuple(urlsplit(href).path for href in hrefs)
    if loaded_css != EXPECTED_CSS:
        raise RuntimeError(f"Production stylesheet set changed: {loaded_css}")
    if ('https://www.googletagmanager.com/gtag/js?id=' not in html
            or 'https://www.clarity.ms/tag/' not in html):
        raise RuntimeError("Unexpected production analytics configuration")
    print(f"Verified production homepage and dependencies: {PRODUCTION_URL}", flush=True)


def extract_metrics(data):
    if data.get("runtimeError"):
        raise RuntimeError(f"Lighthouse runtime error: {data['runtimeError']}")
    score = data.get("categories", {}).get("performance", {}).get("score")
    if not isinstance(score, (int, float)):
        raise RuntimeError("Missing Lighthouse performance score")
    metrics = {"score": round(score * 100, 2)}
    for name, audit_key in AUDIT_KEYS.items():
        value = data.get("audits", {}).get(audit_key, {}).get("numericValue")
        if not isinstance(value, (int, float)):
            raise RuntimeError(f"Missing {audit_key} in Lighthouse report")
        metrics[name] = float(value)
    return metrics


def run_lighthouse(url, destination, device):
    args = [
        "lighthouse", url, "--only-categories=performance", "--output=json",
        f"--output-path={destination}",
        "--chrome-flags=--headless --no-sandbox --disable-dev-shm-usage", "--quiet",
    ]
    if device == "desktop":
        args.append("--preset=desktop")
    result = subprocess.run(args, text=True, capture_output=True, timeout=240, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            f"Lighthouse failed (exit {result.returncode}): "
            f"{result.stderr[-3000:]} {result.stdout[-1000:]}"
        )
    if not destination.is_file():
        raise RuntimeError(f"Missing Lighthouse output: {destination}")


def fmt(value, unit="ms"):
    if not isinstance(value, (int, float)):
        return "n/a"
    return f"{value:.1f}{(' ' + unit) if unit else ''}"


def render_report(rows, device):
    if not rows:
        raise ValueError("Cannot report an empty measurement set")
    lines = [
        f"# Production performance monitor — {device}",
        "",
        f"{len(rows)} Lighthouse runs of the production homepage on one GitHub-hosted runner.",
        "This is a **synthetic lab test**, not real-user Core Web Vitals.",
        "The homepage is the only URL tested. No experimental pages or public reports are created.",
        "",
        "### Median measurements",
        "",
        "| Metric | Median | Minimum | Maximum |",
        "| --- | ---: | ---: | ---: |",
    ]
    for label, key, unit in METRICS:
        values = [row[key] for row in rows]
        lines.append(
            f"| {label} | {fmt(statistics.median(values), unit)} | "
            f"{fmt(min(values), unit)} | {fmt(max(values), unit)} |"
        )

    lines += [
        "",
        "### Per-run loading diagnostics",
        "",
        "Scored LCP uses Lighthouse's **modeled** throttling; observed LCP and CSS "
        "request durations come from the unthrottled browser trace. "
        "They are not measurements under equivalent network conditions.",
        "",
        "| Run | Score | Modeled LCP | Observed LCP | home.css duration | home.css finished | Slowest CSS request |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in sorted(rows, key=lambda item: item["run"]):
        path = row.get("slowest_css_path") or ""
        slowest = path.rsplit("/", 1)[-1] if path else "n/a"
        lines.append(
            f"| {row['run']} | {row['score']:.0f} | {fmt(row['lcp_ms'])} | "
            f"{fmt(row.get('observed_lcp_ms'))} | {fmt(row.get('home_css_duration_ms'))} | "
            f"{fmt(row.get('home_css_finish_ms'))} | "
            f"{slowest} ({fmt(row.get('slowest_css_duration_ms'))}) |"
        )
    unusual = outlier_rows(rows)
    if unusual:
        lines += ["", "### Modeled LCP outliers", ""]
        for row in unusual:
            lines.append(
                f"- Run {row['run']}: modeled LCP {fmt(row['lcp_ms'])}; "
                f"observed {fmt(row.get('observed_lcp_ms'))}; "
                f"home.css {fmt(row.get('home_css_duration_ms'))}. "
                "This does not establish the cause."
            )

    lines += [
        "",
        "### Production guardrails (warning-only)",
        "",
        "These checks use **medians**, not individual outliers. They are conservative "
        "synthetic lab warning thresholds, not field Core Web Vitals or "
        "comparisons with a saved historical baseline. They never block deployment.",
        "",
        "| Check | Median | Warning threshold | Status | Individual runs outside threshold |",
        "| --- | ---: | ---: | --- | ---: |",
    ]
    for check in guardrail_checks(rows):
        unit = f" {check['units']}" if check["units"] else ""
        direction = "below" if check["label"] == "Performance score" else "above"
        lines.append(
            f"| {check['label']} | {check['median']:.1f}{unit} | "
            f"{direction} {check['limit']:g}{unit} | **{check['status']}** | "
            f"{check['affected']}/{check['total']} |"
        )
    lines += [
        "",
        f"Tested URL: {PRODUCTION_URL}",
        "",
        "Job artifact: Lighthouse JSON reports, measurements.csv, stylesheet-requests.csv, and summary.md.",
        "Artifacts expire after 30 days. This summary is available only in GitHub Actions, not on the site.",
        "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("mobile", "desktop"), default="mobile")
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--output-dir", type=Path, default=Path("performance-reports"))
    args = parser.parse_args()
    if not 3 <= args.runs <= 10:
        parser.error("--runs must be between 3 and 10 for median-based checks")

    validate_live_homepage()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    css_rows = []
    for number in range(1, args.runs + 1):
        filename = args.output_dir / f"production-{args.device}-run-{number:02d}.json"
        print(f"Run {number}/{args.runs}: {PRODUCTION_URL} ({args.device})", flush=True)
        run_lighthouse(PRODUCTION_URL, filename, args.device)
        payload = json.loads(filename.read_text(encoding="utf-8"))
        metrics = extract_metrics(payload)
        rows.append({
            "run": number, "variant": "production", "device": args.device,
            **metrics, **diagnostics(payload),
        })
        css_rows.extend({
            "run": number, "device": args.device, **request,
        } for request in stylesheet_requests(payload))
        print(
            f"  Score {metrics['score']:.0f}; LCP {metrics['lcp_ms']:.0f} ms; "
            f"TBT {metrics['tbt_ms']:.0f} ms",
            flush=True,
        )
        if number < args.runs:
            time.sleep(2)

    with (args.output_dir / "measurements.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    if css_rows:
        with (args.output_dir / "stylesheet-requests.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=list(css_rows[0]))
            writer.writeheader()
            writer.writerows(css_rows)

    summary = render_report(rows, args.device)
    (args.output_dir / "summary.md").write_text(summary, encoding="utf-8")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as handle:
            handle.write(summary + "\n")
    for check in guardrail_checks(rows):
        if check["status"] == "WARN":
            print(
                f"::warning title=Production performance lab guardrail::"
                f"{check['label']} median {check['median']:.1f} crossed {check['limit']:g} "
                f"({check['affected']}/{check['total']} runs)",
                flush=True,
            )
    print(summary)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, subprocess.TimeoutExpired, ValueError) as exc:
        print(f"Monitoring failed: {exc}", file=sys.stderr)
        sys.exit(1)
