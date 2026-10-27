#!/usr/bin/env python3
"""Fail a Pages build if the rendered HTML loses its browser security guardrails.

GitHub Pages cannot set site-specific HSTS/X-Frame-Options/nosniff HTTP headers.
This check deliberately verifies only protections possible in site HTML.
"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path

NON_EXECUTABLE_SCRIPT_TYPES = {"application/ld+json", "application/json", "importmap"}


class BrowserSecurityParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.csp: str | None = None
        self.referrer: str | None = None
        self.errors: list[str] = []
        self.seen_script = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "meta":
            if (attributes.get("http-equiv") or "").lower() == "content-security-policy":
                if self.csp is not None:
                    self.errors.append("multiple CSP meta tags")
                if self.seen_script:
                    self.errors.append("CSP declared after a script")
                self.csp = attributes.get("content") or ""
            if (attributes.get("name") or "").lower() == "referrer":
                self.referrer = attributes.get("content")
        if tag == "script":
            self.seen_script = True
            script_type = (attributes.get("type") or "").lower().strip()
            if not attributes.get("src") and script_type not in NON_EXECUTABLE_SCRIPT_TYPES:
                self.errors.append("executable inline script")
            if (attributes.get("src") or "").lower().startswith("http://"):
                self.errors.append("script loaded over HTTP")
        for key, value in attrs:
            if key.lower().startswith("on") and value is not None:
                self.errors.append("inline event handler: " + key)

    def validate(self) -> list[str]:
        errors = list(self.errors)
        if not self.csp:
            errors.append("missing CSP meta tag")
        else:
            directives = {}
            for item in self.csp.split(";"):
                tokens = item.strip().split()
                if tokens:
                    directives[tokens[0]] = tokens[1:]
            if "'unsafe-inline'" in directives.get("script-src", []):
                errors.append("unsafe-inline permitted in script-src")
            if "'unsafe-eval'" in directives.get("script-src", []):
                errors.append("unsafe-eval permitted in script-src")
            if not {"default-src", "script-src", "connect-src", "base-uri", "object-src", "form-action"}.issubset(directives):
                errors.append("missing required CSP directives")
            if directives.get("object-src") != ["'none'"]:
                errors.append("object-src must be 'none'")
            if "https://stats.g.doubleclick.net" not in directives.get("connect-src", []):
                errors.append("Google measurement endpoint missing from connect-src")
            if "frame-ancestors" in directives or "report-uri" in directives:
                errors.append("header-only directives in meta CSP")
        if self.referrer != "strict-origin-when-cross-origin":
            errors.append("missing expected referrer policy")
        return errors


def check_site(site_dir: Path) -> list[str]:
    if not site_dir.is_dir():
        return ["Site build folder does not exist: " + str(site_dir)]
    pages = sorted(site_dir.rglob("*.html"))
    if not pages:
        return ["No HTML pages found in " + str(site_dir)]
    errors: list[str] = []
    for path in pages:
        parser = BrowserSecurityParser()
        parser.feed(path.read_text(encoding="utf-8"))
        errors.extend(str(path.relative_to(site_dir)) + ": " + detail for detail in parser.validate())
    print(f"Checked browser security policy for {len(pages)} rendered HTML pages.")
    return errors


def main() -> int:
    command = argparse.ArgumentParser()
    command.add_argument("--site-dir", type=Path, default=Path("_site"))
    args = command.parse_args()
    errors = check_site(args.site_dir)
    if errors:
        for error in errors:
            print("ERROR: " + error)
        return 1
    print("CSP and Referrer-Policy checks passed; executable inline scripts are disabled.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
