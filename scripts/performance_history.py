#!/usr/bin/env python3
"""Append durable Lighthouse medians to the repository's performance-history issue.

Lighthouse JSON artifacts expire; GitHub issue comments retain the per-device
median measurements for long-term comparisons without changing site content.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import re
import statistics
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ISSUE_NUMBER = 36
MARKER = re.compile(r"<!-- coding-performance-history (\{[^\n]*\}) -->")
FIELDS = ("score", "fcp_ms", "lcp_ms", "speed_index_ms", "tbt_ms", "cls")
ISSUE_API = "https://api.github.com/repos/{repo}/issues/{issue}/comments"
REQUIRED_ENV = ("GITHUB_TOKEN", "GITHUB_REPOSITORY", "GITHUB_RUN_ID", "GITHUB_RUN_NUMBER", "GITHUB_SHA")


def read_medians(artifact_root: Path) -> list[dict]:
    """Read each device's five production Lighthouse samples, not just a score."""
    reports = sorted(artifact_root.glob("production-performance-*/measurements.csv"))
    if not reports:
        raise ValueError(f"No per-device measurements.csv files found under {artifact_root}")
    result = []
    seen = set()
    for report in reports:
        with report.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if len(rows) != 5:
            raise ValueError(f"Expected 5 samples in {report}, found {len(rows)}")
        devices = {row.get("device") for row in rows}
        if len(devices) != 1 or next(iter(devices)) not in ("mobile", "desktop"):
            raise ValueError(f"Invalid device in {report}")
        device = devices.pop()
        if device in seen:
            raise ValueError(f"Multiple measurements files for {device}")
        seen.add(device)
        if {row.get("run") for row in rows} != {"1", "2", "3", "4", "5"}:
            raise ValueError(f"Unexpected run indexes in {report}")
        if any(row.get("variant") != "production" for row in rows):
            raise ValueError(f"Non-production results in {report}")
        medians = {}
        for field in FIELDS:
            try:
                values = [float(row[field]) for row in rows]
            except (ValueError, TypeError, KeyError) as exc:
                raise ValueError(f"Malformed {field} in {report}") from exc
            if not all(math.isfinite(v) and v >= 0 for v in values):
                raise ValueError(f"Invalid value for {field} in {report}")
            medians[field] = round(statistics.median(values), 3)
        if not 0 <= medians["score"] <= 100:
            raise ValueError(f"Invalid score in {report}")
        result.append({"device": device, "count": len(rows), **medians})
    return sorted(result, key=lambda row: row["device"])


def parse_history(comments: list[dict]) -> list[dict]:
    records = []
    for comment in comments:
        for candidate in MARKER.findall(comment.get("body") or ""):
            try:
                record = json.loads(candidate)
                if (record.get("device") in ("mobile", "desktop")
                        and isinstance(record.get("run_id"), int)
                        and all(isinstance(record.get(k), (float, int)) for k in FIELDS)):
                    records.append(record)
            except (ValueError, TypeError):
                continue
    return records


def previous_record(history: list[dict], device: str, run_id: int) -> dict | None:
    entries = [item for item in history if item["device"] == device and item["run_id"] != run_id]
    return entries[-1] if entries else None


def metric_delta(value: float, previous: float | None, units: str) -> str:
    if previous is None:
        return "—"
    diff = value - previous
    if abs(diff) < (0.0005 if units == "" else 0.05):
        return "0"
    return f"{diff:+.1f}{units}" if units else f"{diff:+.3f}"


def render_comment(records: list[dict], history: list[dict], run_url: str, event: str) -> str:
    if not records:
        raise ValueError("Nothing new to archive")
    date = records[0]["date"][:10]
    lines = [
        f"### {date} — {' + '.join(r['device'] for r in records)} — {event} Lighthouse check",
        "",
        "Five production homepage Lighthouse measurements per device; values below are **medians**.",
        "",
        "| Device | Score | Δ score | FCP | LCP (modeled) | Δ LCP | TBT | Δ TBT | CLS |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for record in records:
        older = previous_record(history, record["device"], record["run_id"])
        lines.append(
            f"| {record['device']} | **{record['score']:.0f}** | "
            f"{metric_delta(record['score'], older['score'] if older else None, ' pts')} | "
            f"{record['fcp_ms']:.0f} ms | **{record['lcp_ms']:.0f} ms** | "
            f"{metric_delta(record['lcp_ms'], older['lcp_ms'] if older else None, ' ms')} | "
            f"{record['tbt_ms']:.0f} ms | "
            f"{metric_delta(record['tbt_ms'], older['tbt_ms'] if older else None, ' ms')} | "
            f"{record['cls']:.3f} |"
        )
    lines.extend([
        "",
        f"**Source:** [Lighthouse workflow run]({run_url}) · Synthetic lab data, not real-user Core Web Vitals.",
        "Negative Δ LCP / Δ TBT means faster. Small variations between GitHub-hosted runners are expected.",
        "Raw Lighthouse reports are kept as run artifacts for 30 days; these summaries persist in this issue.",
        "",
    ])
    for record in records:
        older = previous_record(history, record["device"], record["run_id"])
        if older:
            score_drop = older["score"] - record["score"]
            lcp_growth = record["lcp_ms"] - older["lcp_ms"]
            tbt_growth = record["tbt_ms"] - older["tbt_ms"]
            if score_drop >= 5 or lcp_growth >= 500 or tbt_growth >= 200:
                lines.append(
                    f"> **Investigate {record['device']} regression:** compared with "
                    f"[run {older['run_id']}](https://github.com/"
                    f"{os.environ.get('GITHUB_REPOSITORY', 'infoconex/coding-blog')}/actions/runs/{older['run_id']}), "
                    f"score changed {score_drop:+.0f} points lower, "
                    f"LCP {lcp_growth:+.0f} ms, TBT {tbt_growth:+.0f} ms."
                )
        lines.append(f"<!-- coding-performance-history {json.dumps(record, separators=(',', ':'))} -->")
    return "\n".join(lines) + "\n"


def github_api(method: str, url: str, token: str, payload: dict | None = None):
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8") if payload is not None else None,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "coding-blog-lighthouse-history/1.0",
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urlopen(request, timeout=35) as response:
            return json.load(response)
    except (HTTPError, URLError) as exc:
        raise RuntimeError(f"GitHub issue history API request failed ({method}): {exc}") from exc


def fetch_issue_comments(repo: str, token: str) -> list[dict]:
    comments = []
    for page in range(1, 51):
        batch = github_api("GET", ISSUE_API.format(repo=repo, issue=ISSUE_NUMBER)
                           + f"?per_page=100&page={page}", token)
        if not isinstance(batch, list):
            raise RuntimeError("Unexpected GitHub issue comments API response")
        comments.extend(batch)
        if len(batch) < 100:
            return comments
    raise RuntimeError("History exceeds 5,000 comments; pagination limit reached")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-root", type=Path, default=Path("performance-history-input"))
    args = parser.parse_args()
    missing = [name for name in REQUIRED_ENV if not os.environ.get(name)]
    if missing:
        parser.error("Missing required Actions environment: " + ", ".join(missing))
    repo = os.environ["GITHUB_REPOSITORY"]
    if repo != "infoconex/coding-blog":
        raise RuntimeError("Refusing to write history to the wrong repository")
    token = os.environ["GITHUB_TOKEN"]
    run_id = int(os.environ["GITHUB_RUN_ID"])
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    samples = read_medians(args.artifact_root)
    records = [{
        "run_id": run_id,
        "device": sample["device"],
        "date": now,
        **{key: value for key, value in sample.items() if key != "device"},
        "head_sha": os.environ["GITHUB_SHA"],
    } for sample in samples]

    history = parse_history(fetch_issue_comments(repo, token))
    existing = {(entry["run_id"], entry["device"]) for entry in history}
    new_records = [record for record in records if (record["run_id"], record["device"]) not in existing]
    if not new_records:
        print("This workflow run has already been archived. Nothing to do.")
        return 0

    url = f"https://github.com/{repo}/actions/runs/{run_id}"
    body = render_comment(new_records, history, url, os.environ.get("GITHUB_EVENT_NAME", "manual"))
    comment = github_api("POST", ISSUE_API.format(repo=repo, issue=ISSUE_NUMBER), token, {"body": body})
    issue_url = f"https://github.com/{repo}/issues/{ISSUE_NUMBER}"
    print(f"Archived {len(new_records)} device(s) in {issue_url} (comment {comment.get('id')}).")
    print(body)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as handle:
            handle.write(body + f"\n[Long-term history]({issue_url})\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError) as exc:
        print(f"Failed to update Lighthouse history: {exc}")
        raise SystemExit(1)
