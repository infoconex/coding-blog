#!/usr/bin/env python3
"""Exercise the public GitHub Pages site in a real browser and report CSP blocks.

A healthy HTML response does not prove tracking works. This script records
browser-enforced securitypolicyviolation events, console CSP errors, and whether
the Google Analytics and Clarity scripts were requested and loaded.
No dashboard access, cookies, tokens, or personal data are required.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

BASE = "https://coding.infoconex.com"
PATHS = (
    "/",
    "/writing/",
    "/post/2010/10/11/ASPNET-CustomValidator-that-validates-multiple-controls-using-both-Server-Side-and-Client-Side-scripting",
)
TRACKERS = ("googletagmanager.com", "clarity.ms", "google-analytics.com", "c.bing.com")
CAPTURE_VIOLATIONS = """
(() => {
  window.__cspViolations = [];
  document.addEventListener('securitypolicyviolation', e => {
    window.__cspViolations.push({
      effectiveDirective: e.effectiveDirective,
      blockedURI: e.blockedURI,
      disposition: e.disposition,
      sourceFile: e.sourceFile
    });
  });
})();
"""


def display_url(url: str) -> str:
    """Do not save tracking parameters, identifying IDs, or full beacon URLs."""
    parsed = urlsplit(url)
    return parsed.netloc + parsed.path


def tracker_kind(url: str) -> str | None:
    host = urlsplit(url).hostname or ""
    for domain in TRACKERS:
        if host == domain or host.endswith("." + domain):
            return domain
    return None


def scan_site() -> tuple[list[dict], list[str]]:
    chrome = os.environ.get("CHROME_PATH")
    if not chrome or not Path(chrome).is_file():
        raise RuntimeError("CHROME_PATH must point to the browser-actions/setup-chrome executable")
    results = []
    errors = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=chrome, headless=True, args=["--no-sandbox"])
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        context.add_init_script(script=CAPTURE_VIOLATIONS)
        try:
            for path in PATHS:
                page = context.new_page()
                console_csp = []
                tracker_requests = set()
                tracker_responses = set()
                tracker_failures = []

                def on_console(message):
                    if message.type == "error" and ("content security policy" in message.text.lower()
                                                    or "violates the following" in message.text.lower()
                                                    or "refused to" in message.text.lower()):
                        # Never write visitor identifiers or measurement query strings to logs.
                        sanitized = re.sub(
                            r"https?://[^\\s'\\\"<>]+",
                            lambda match: display_url(match.group(0)),
                            message.text,
                        )
                        console_csp.append(sanitized[:500])

                def on_request(request):
                    if (kind := tracker_kind(request.url)):
                        tracker_requests.add(kind + ": " + display_url(request.url))

                def on_response(response):
                    if (kind := tracker_kind(response.url)):
                        tracker_responses.add(f"{kind}: {display_url(response.url)} [{response.status}]")

                def on_failure(request):
                    if (kind := tracker_kind(request.url)):
                        tracker_failures.append(f"{kind}: {display_url(request.url)} [{request.failure}]")

                page.on("console", on_console)
                page.on("request", on_request)
                page.on("response", on_response)
                page.on("requestfailed", on_failure)

                try:
                    response = page.goto(BASE + path, wait_until="domcontentloaded", timeout=40000)
                    page.wait_for_timeout(6500)
                    status = response.status if response else 0
                    policy = page.locator('meta[http-equiv="Content-Security-Policy"]').get_attribute("content")
                    violations = page.evaluate("window.__cspViolations || []")
                    item = {
                        "path": path,
                        "http_status": status,
                        "csp_present": bool(policy),
                        "violations": [
                            {**v, "blockedURI": display_url(v["blockedURI"]) if v.get("blockedURI", "").startswith("http") else v.get("blockedURI")}
                            for v in violations
                        ],
                        "console_csp_errors": console_csp,
                        "tracker_requests": sorted(tracker_requests),
                        "tracker_responses": sorted(tracker_responses),
                        "tracker_failures": tracker_failures,
                    }
                    results.append(item)
                    print(f"{path}: HTTP {status}; CSP events={len(violations)}; tracker requests={len(tracker_requests)}; tracker responses={len(tracker_responses)}")
                    for event in violations:
                        print("  CSP BLOCK:", event.get("effectiveDirective"), display_url(event.get("blockedURI", "")))
                    for issue in console_csp:
                        print("  CSP CONSOLE:", issue)
                    for failed in tracker_failures:
                        print("  TRACKER NETWORK FAILURE:", failed)
                    if status != 200:
                        errors.append(f"{path}: unexpected HTTP status {status}")
                    if not policy:
                        errors.append(f"{path}: CSP meta tag missing")
                    if violations or console_csp:
                        errors.append(f"{path}: browser reported {len(violations)} CSP events and {len(console_csp)} CSP console errors")
                finally:
                    page.close()
        finally:
            context.close()
            browser.close()
    return results, errors


def main() -> int:
    results, errors = scan_site()
    output_dir = Path("csp-reports")
    output_dir.mkdir(exist_ok=True)
    (output_dir / "live-csp.json").write_text(
        json.dumps({"pages": results, "errors": errors}, indent=2) + "\n", encoding="utf-8"
    )
    for entry in results:
        if entry["path"] == "/":
            if not any("googletagmanager.com/gtag/js" in req for req in entry["tracker_requests"]):
                errors.append("Homepage: Google Analytics script request was not seen")
            if not any("clarity.ms/tag/" in req for req in entry["tracker_requests"]):
                errors.append("Homepage: Clarity script request was not seen")
    if errors:
        print("\nCHECK FAILED:")
        for message in errors:
            print(" -", message)
        return 1
    print("\nNo CSP violations were reported in these browser checks.")
    print("Tracker requests/responses are reported separately: dashboard collection cannot be proven here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
