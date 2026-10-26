#!/usr/bin/env python3
"""Compare live performance experiments with repeated, alternating Lighthouse runs."""

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
    "production-baseline": {
        "variants": ("production", "baseline"),
        "urls": {
            "production": "https://coding.infoconex.com/",
            "baseline": "https://coding.infoconex.com/experiments/analytics-impact/both/",
        },
        "description": (
            "Compares the live production homepage with an isolated, nonindexed copy. "
            "Both run Google Analytics, Clarity, and the same five homepage stylesheets. "
            "Tests isolate remaining differences between production and the experiment."
        ),
    },
    "google-timing": {
        "base_url": "https://coding.infoconex.com/experiments/google-timing/",
        "variants": ("current", "after-load"),
        "description": (
            "Both versions run Google Analytics and Clarity. Current loads gtag.js as an async "
            "head script, while after-load requests gtag.js after the window load event. "
            "Both queue the same GA configuration. Short visits ending before load may not "
            "be counted by the delayed version."
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


def variant_url(experiment: str, variant: str) -> str:
    config = EXPERIMENTS[experiment]
    if variant not in config["variants"]:
        raise ValueError(f"Unknown {experiment} variant: {variant}")
    return config["urls"][variant] if "urls" in config else f"{config['base_url']}{variant}/"


def stylesheet_paths(html: str) -> tuple[str, ...]:
    """Match actual stylesheet URLs independent of cache-busting query strings."""
    hrefs = re.findall(r'<link rel="stylesheet" href="([^"]+)"', html)
    return tuple(urlsplit(href).path for href in hrefs)


def ensure_pages_are_available(experiment: str) -> None:
    configuration = EXPERIMENTS[experiment]
    html_by_variant = {}
    for variant in configuration["variants"]:
        url = variant_url(experiment, variant)
        request = Request(url, headers={"User-Agent": "coding-blog-performance-comparison/1.0"})
        try:
            with urlopen(request, timeout=30) as response:
                status = response.status
                html = response.read(150_000).decode("utf-8", errors="replace")
        except (HTTPError, URLError) as exc:
            raise RuntimeError(f"Experiment page unavailable: {url}: {exc}") from exc

        is_production = experiment == "production-baseline" and variant == "production"
        noindex = '<meta name="robots" content="noindex">' in html
        if status != 200 or noindex == is_production:
            raise RuntimeError(
                f"Unexpected page status or indexing directive: {url} (HTTP {status}, noindex={noindex})"
            )
        html_by_variant[variant] = html

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

        if experiment == "google-timing":
            marker = f'<meta name="experiment-google-timing" content="{variant}">'
            static_tag = '<script async src="https://www.googletagmanager.com/gtag/js?id='
            is_static = static_tag in html
            is_delayed = "window.addEventListener('load', loadGoogleTag" in html
            has_clarity = "https://www.clarity.ms/tag/" in html
            has_config = "gtag('config'," in html
            if (marker not in html or is_static != (variant == "current")
                    or is_delayed != (variant == "after-load")
                    or not has_clarity or not has_config):
                raise RuntimeError(f"Unexpected Google timing configuration at {url}")

        print(f"Verified live page: {url}", flush=True)

    if experiment == "production-baseline":
        reference = stylesheet_paths(html_by_variant["production"])
        comparison = stylesheet_paths(html_by_variant["baseline"])
        expected_stylesheets = (
            "/assets/css/site.css", "/assets/css/themes.css", "/assets/css/search.css",
            "/assets/css/mobile-header.css", "/assets/css/home.css",
        )
        if reference != expected_stylesheets or comparison != expected_stylesheets:
            raise RuntimeError(
                "Production and baseline do not load identical expected CSS files. "
                f"Production: {reference}; baseline: {comparison}"
            )
        for variant, html in html_by_variant.items():
            has_google = '<script async src="https://www.googletagmanager.com/gtag/js?id=' in html
            has_clarity = 'https://www.clarity.ms/tag/' in html
            if not has_google or not has_clarity:
                raise RuntimeError(f"Both production and baseline must load analytics: {variant}")


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
        ("Production is indexable; the baseline is noindex and excluded from IndexNow."
         if experiment == "production-baseline" else
         "All experiment pages are noindex and excluded from IndexNow."),
        "Lower is better for timing and layout shift; higher is better for Performance score.",
        "",
    ]
    headers = ["Metric"] + [variant.capitalize() + " median" for variant in variants]
    pair = {
        "css": ("baseline", "optimized"),
        "google-timing": ("current", "after-load"),
        "production-baseline": ("production", "baseline"),
    }.get(experiment)
    if pair:
        headers += [f"Difference ({pair[1]} − {pair[0]})"]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] + ["---:"] * (len(headers) - 1)) + " |")

    for label, metric, unit in METRICS:
        cells = [label] + [formatted(median(v, metric), metric, unit) for v in variants]
        if pair:
            cells += [formatted(median(pair[1], metric) - median(pair[0], metric),
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

    if experiment == "google-timing":
        lines += [
            "",
            "**Tracking caveat:** This measures loading performance, not GA reporting completeness. "
            "A visit ending before the load event may never request gtag.js in the after-load version. "
            "Validate that real pageviews are received and weigh this tradeoff before making a production change.",
        ]

    if all("observed_lcp_ms" in row for row in rows):
        lines += [
            "",
            "### Per-run loading diagnostics",
            "",
            "The scored LCP is Lighthouse's **modeled** mobile timing; observed LCP and "
            "CSS request timings come from its unthrottled browser trace. "
            "Do not compare them as if both used the same network conditions.",
            "",
            "| Variant | Run | Modeled LCP | Observed LCP | Home CSS duration | Home CSS finished | Slowest CSS request |",
            "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]

        def fmt(value):
            return f"{value:.0f} ms" if isinstance(value, (float, int)) else "n/a"

        for row in sorted(rows, key=lambda entry: (entry["pair"], entry["variant"])):
            slowest_path = row.get("slowest_css_path", "")
            slowest_label = slowest_path.split("/")[-1] if slowest_path else "n/a"
            slowest_duration = fmt(row.get("slowest_css_duration_ms"))
            lines.append(
                f"| {row['variant']} | {row['pair']} | {fmt(row['lcp_ms'])} | "
                f"{fmt(row.get('observed_lcp_ms'))} | {fmt(row.get('home_css_duration_ms'))} | "
                f"{fmt(row.get('home_css_finish_ms'))} | "
                f"{slowest_label} ({slowest_duration}) |"
            )

        unusual = outlier_rows(rows)
        if unusual:
            lines += ["", "### Modeled LCP outliers", ""]
            for row in unusual:
                ratio = row["lcp_ms"] / row["observed_lcp_ms"] if row.get("observed_lcp_ms") else None
                comparison = f" ({ratio:.1f}× observed)" if ratio is not None else ""
                lines.append(
                    f"- **{row['variant']} / run {row['pair']}**: modeled LCP "
                    f"{fmt(row['lcp_ms'])}; observed LCP "
                    f"{fmt(row.get('observed_lcp_ms'))}{comparison}; "
                    f"home.css took {fmt(row.get('home_css_duration_ms'))}. "
                    "This is a diagnostic clue, not proof of causation."
                )

    checks = guardrail_checks(rows, experiment)
    if checks:
        lines += [
            "",
            "### Production regression guardrails (manual, warning-only)",
            "",
            "The checks apply to the **median of production runs**, not a single outlier. "
            "These are conservative synthetic-lab heuristics, not field Core Web Vitals. "
            "They do not fail the workflow or trigger deployments.",
            "",
            "| Check | Median | Warning threshold | Status | Runs outside limit |",
            "| --- | ---: | ---: | --- | ---: |",
        ]
        for check in checks:
            suffix = f" {check['units']}" if check["units"] else ""
            comparison = "below" if check["label"] == "Performance score" else "above"
            lines.append(
                f"| {check['label']} | {check['median']:.1f}{suffix} | "
                f"{comparison} {check['limit']:g}{suffix} | **{check['status']}** | "
                f"{check['affected']}/{check['total']} |"
            )

    lines += [
        "",
        "**Interpretation:** Compare medians and the individual runs. "
        "Do not change production on small or inconsistent differences alone.",
        "",
        "### Tested URLs",
        *[f"- {variant.capitalize()}: {variant_url(experiment, variant)}" for variant in variants],
        "",
        "Downloadable artifact: Lighthouse JSON, measurements.csv, stylesheet-requests.csv, and summary.md.",
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
    css_rows = []
    for pair in range(1, args.runs + 1):
        # Reverse order every other round to reduce systematic order effects.
        order = variants if pair % 2 else tuple(reversed(variants))
        for variant in order:
            url = variant_url(args.experiment, variant)
            filename = f"{args.experiment}-{args.device}-pair-{pair:02d}-{variant}.json"
            print(f"Pair {pair}/{args.runs}: testing {variant} ({args.device})", flush=True)
            run_lighthouse(url, args.output_dir / filename, args.device)
            report = args.output_dir / filename
            metrics = extract_metrics(report)
            report_data = json.loads(report.read_text(encoding="utf-8"))
            measured = diagnostics(report_data)
            rows.append({
                "pair": pair, "variant": variant, "device": args.device,
                "experiment": args.experiment, **metrics, **measured,
            })
            css_rows.extend({
                "pair": pair, "variant": variant, "device": args.device,
                "experiment": args.experiment, **css
            } for css in stylesheet_requests(report_data))
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

    # Detailed network timings remain available as CSV even when the summary
    # highlights only home.css and the slowest stylesheet.
    if css_rows:
        with (args.output_dir / "stylesheet-requests.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=list(css_rows[0]))
            writer.writeheader()
            writer.writerows(css_rows)

    summary = render_report(rows, args.device, args.experiment)
    for check in guardrail_checks(rows, args.experiment):
        if check["status"] == "WARN":
            print(
                f"::warning title=Production lab performance guardrail::"
                f"{check['label']} median {check['median']:.1f} "
                f"outside warning threshold {check['limit']:g} "
                f"({check['affected']}/{check['total']} individual runs)",
                flush=True,
            )
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
