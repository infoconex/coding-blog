#!/usr/bin/env python3
"""Compare live performance experiments with repeated, alternating Lighthouse runs."""

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

EXPERIMENTS = {
    "css": {
        "base_url": "https://coding.infoconex.com/experiments/css-optimization/",
        "variants": ("baseline", "optimized"),
        "description": "Baseline loads five CSS files; optimized loads one combined stylesheet. Both omit analytics.",
    },
    "analytics": {
        "base_url": "https://coding.infoconex.com/experiments/analytics-impact/",
        "variants": ("none", "google", "clarity", "both"),
        "description": (
            "All pages use the same homepage content and CSS; they differ only in tracking. "
            "Google Analytics and Clarity use the production project IDs; test visits will appear in analytics."
        ),
    },
}
METRICS = (
    ("Performance score", "score", "points"),
    ("First Contentful Paint", "fcp_ms", "ms"),
    ("Largest Contentful Paint", "lcp_ms", "ms"),
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


def ensure_pages_are_available(experiment: str) -> None:
    configuration = EXPERIMENTS[experiment]
    for variant in configuration["variants"]:
        url = f"{configuration['base_url']}{variant}/"
        request = Request(url, headers={"User-Agent": "coding-blog-performance-comparison/1.0"})
        try:
            with urlopen(request, timeout=30) as response:
                status = response.status
                html = response.read(150_000).decode("utf-8", errors="replace")
        except (HTTPError, URLError) as exc:
            raise RuntimeError(f"Experiment page unavailable: {url}: {exc}") from exc

        if status != 200 or '<meta name="robots" content="noindex">' not in html:
            raise RuntimeError(f"Unexpected experimental page response: {url} (HTTP {status})")

        if experiment == "analytics":
            google = "www.googletagmanager.com/gtag/js?id=" in html
            clarity = "https://www.clarity.ms/tag/" in html
            expected_google = variant in ("google", "both")
            expected_clarity = variant in ("clarity", "both")
            if google != expected_google or clarity != expected_clarity:
                raise RuntimeError(
                    f"Tracking scripts do not match variant {variant}: "
                    f"Google={google}, Clarity={clarity} at {url}"
                )

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


def render_report(rows: list[dict], device: str, experiment: str) -> str:
    configuration = EXPERIMENTS[experiment]
    variants = configuration["variants"]
    measurements = {
        variant: [row for row in rows if row["variant"] == variant]
        for variant in variants
    }
    if any(not values for values in measurements.values()):
        raise ValueError("Missing measurements for one or more experiment variants")

    def median(variant: str, metric: str) -> float:
        return statistics.median(row[metric] for row in measurements[variant])

    def formatted(value: float, key: str, unit: str, signed: bool = False) -> str:
        decimals = 3 if key == "cls" else 1
        sign = "+" if signed and value > 0 else ""
        return f"{sign}{value:.{decimals}f}{(' ' + unit) if unit else ''}"

    lines = [
        f"# Live {experiment.upper()} performance comparison — {device}",
        "",
        f"{len(measurements[variants[0]])} runs for each of {len(variants)} variants, "
        "alternating test order on the same GitHub-hosted runner.",
        configuration["description"],
        "All experiment pages are noindex and excluded from IndexNow.",
        "Lower is better for timing and layout shift; higher is better for Performance score.",
        "",
    ]
    headers = ["Metric"] + [variant.capitalize() + " median" for variant in variants]
    if experiment == "css":
        headers += ["Difference (optimized − baseline)"]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] + ["---:"] * (len(headers) - 1)) + " |")

    for label, metric, unit in METRICS:
        cells = [label] + [formatted(median(v, metric), metric, unit) for v in variants]
        if experiment == "css":
            cells += [formatted(median("optimized", metric) - median("baseline", metric),
                                metric, unit, signed=True)]
        lines.append("| " + " | ".join(cells) + " |")

    if experiment == "analytics":
        lines += [
            "",
            "### Change relative to no tracking",
            "",
            "| Metric | Google only − none | Clarity only − none | Both − none |",
            "| --- | ---: | ---: | ---: |",
        ]
        for label, metric, unit in METRICS:
            base = median("none", metric)
            differences = [
                formatted(median(v, metric) - base, metric, unit, signed=True)
                for v in ("google", "clarity", "both")
            ]
            lines.append("| " + " | ".join([label, *differences]) + " |")
        lines += [
            "",
            "The combined effect is not necessarily the sum of separate effects. "
            "Network conditions and Lighthouse run-to-run variation can dominate small differences.",
        ]

    lines += [
        "",
        "**Interpretation:** Compare medians and the individual runs. "
        "Do not change production on small or inconsistent differences alone.",
        "",
        "### Tested URLs",
        *[f"- {variant.capitalize()}: {configuration['base_url']}{variant}/" for variant in variants],
        "",
        "Downloadable artifact: individual Lighthouse JSON results, measurements.csv, and summary.md.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", choices=tuple(EXPERIMENTS), default="css")
    parser.add_argument("--device", choices=("mobile", "desktop"), default="mobile")
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--output-dir", type=Path, default=Path("performance-reports"))
    args = parser.parse_args()
    if not 1 <= args.runs <= 10:
        parser.error("--runs must be between 1 and 10")

    config = EXPERIMENTS[args.experiment]
    variants = config["variants"]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    ensure_pages_are_available(args.experiment)

    rows = []
    for pair in range(1, args.runs + 1):
        # Reverse order every other round to reduce systematic order effects.
        order = variants if pair % 2 else tuple(reversed(variants))
        for variant in order:
            url = f"{config['base_url']}{variant}/"
            filename = f"{args.experiment}-{args.device}-pair-{pair:02d}-{variant}.json"
            print(f"Pair {pair}/{args.runs}: testing {variant} ({args.device})", flush=True)
            run_lighthouse(url, args.output_dir / filename, args.device)
            metrics = extract_metrics(args.output_dir / filename)
            rows.append({
                "pair": pair, "variant": variant, "device": args.device,
                "experiment": args.experiment, **metrics,
            })
            print(
                f"  Performance {metrics['score']:.0f}; LCP {metrics['lcp_ms']:.0f} ms; "
                f"Speed Index {metrics['speed_index_ms']:.0f} ms",
                flush=True,
            )
            time.sleep(2)

    with (args.output_dir / "measurements.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary = render_report(rows, args.device, args.experiment)
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
