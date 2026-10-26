"""Extract repeatable performance diagnostics from Lighthouse 13 JSON reports.

Browser-observed timing comes from the trace while Lighthouse's numeric LCP
is modeled under its throttling configuration. Do not present them as
measurements taken under the same conditions.
"""

from __future__ import annotations

import statistics
from urllib.parse import urlsplit

# Conservative LAB warning limits, not real-user Core Web Vitals or deployment gates.
LAB_GUARDRAILS = (
    ("Performance score", "score", "min", 90.0, "points"),
    ("Modeled LCP", "lcp_ms", "max", 2500.0, "ms"),
    ("Total Blocking Time", "tbt_ms", "max", 600.0, "ms"),
    ("Layout shift", "cls", "max", 0.1, ""),
)


def numeric(value):
    """Only accept real finite numbers, never booleans or missing values."""
    import math

    if type(value) not in (float, int) or not math.isfinite(value):
        return None
    return float(value)


def observed_lcp(report):
    items = report.get("audits", {}).get("metrics", {}).get("details", {}).get("items", [])
    if not items or not isinstance(items[0], dict):
        return None
    return numeric(items[0].get("observedLargestContentfulPaint"))


def lcp_element(report):
    items = (report.get("audits", {}).get("lcp-breakdown-insight", {})
             .get("details", {}).get("items", []))
    for entry in items:
        if entry.get("type") == "node":
            return entry.get("nodeLabel", "")[:160]
    return ""


def stylesheet_requests(report):
    """Return request timings from the browser network log, not simulated timings."""
    items = (report.get("audits", {}).get("network-requests", {})
             .get("details", {}).get("items", []))
    result = []
    for entry in items:
        if entry.get("resourceType") != "Stylesheet":
            continue
        url = entry.get("url", "")
        if not url:
            continue
        path = urlsplit(url).path
        start = numeric(entry.get("networkRequestTime"))
        end = numeric(entry.get("networkEndTime"))
        duration = round(end - start, 2) if start is not None and end is not None and end >= start else None
        result.append({
            "stylesheet_path": path,
            "request_start_ms": start,
            "request_end_ms": end,
            "request_duration_ms": duration,
            "transfer_bytes": numeric(entry.get("transferSize")),
            "http_status": entry.get("statusCode"),
        })
    return result


def diagnostics(report):
    model_lcp = numeric(report.get("audits", {}).get("largest-contentful-paint", {}).get("numericValue"))
    observed = observed_lcp(report)
    css = stylesheet_requests(report)
    home = next((row for row in css if row["stylesheet_path"] == "/assets/css/home.css"), None)
    timed_css = [row for row in css if row["request_duration_ms"] is not None]
    slowest = max(timed_css, key=lambda row: row["request_duration_ms"], default=None)
    return {
        "observed_lcp_ms": observed,
        "lcp_model_gap_ms": round(model_lcp - observed, 1) if model_lcp is not None and observed is not None else None,
        "stylesheet_count": len(css),
        "home_css_duration_ms": home["request_duration_ms"] if home else None,
        "home_css_finish_ms": home["request_end_ms"] if home else None,
        "slowest_css_duration_ms": slowest["request_duration_ms"] if slowest else None,
        "slowest_css_path": slowest["stylesheet_path"] if slowest else "",
        "lcp_element": lcp_element(report),
    }


def guardrail_checks(rows, experiment):
    """Use median values so an isolated poor Lighthouse run does not trigger."""
    if experiment != "production-baseline":
        return []
    production = [row for row in rows if row["variant"] == "production"]
    if not production:
        return []
    checks = []
    for label, key, mode, limit, units in LAB_GUARDRAILS:
        values = [numeric(row.get(key)) for row in production]
        if any(value is None for value in values):
            continue
        median_value = statistics.median(values)
        over = median_value < limit if mode == "min" else median_value > limit
        affected = sum(value < limit if mode == "min" else value > limit for value in values)
        checks.append({
            "label": label, "median": median_value, "limit": limit,
            "units": units, "status": "WARN" if over else "PASS",
            "affected": affected, "total": len(values),
        })
    return checks


def outlier_rows(rows):
    """Highlight modeled-LCP outliers relative to each variant's own median."""
    result = []
    for variant in dict.fromkeys(row["variant"] for row in rows):
        subset = [row for row in rows if row["variant"] == variant]
        center = statistics.median(row["lcp_ms"] for row in subset)
        for row in subset:
            is_outlier = row["lcp_ms"] > max(center + 500.0, center * 1.75)
            if is_outlier:
                result.append(row)
    return result
