#!/usr/bin/env python3
"""Compare Jekyll's generated sitemap and robots.txt with rendered page canonicals.

Runs entirely against _site. No live requests, submissions, or date changes.
"""
from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

from validate_seo import Finding, SITE_HOST, SITE_URL, SeoParser, generated_pages


SITEMAP_URL = SITE_URL + "sitemap.xml"
EXCLUDED_HTML = {"404.html"}  # A custom error document is not a search landing page.


def robots_directives(value: str) -> tuple[list[str], bool]:
    """Read sitemap directives and detect a blanket wildcard Disallow: /."""
    sitemap_urls: list[str] = []
    agents: set[str] = set()
    has_rule = False
    global_block = False
    for raw in value.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            if has_rule:
                agents.clear()
                has_rule = False
            continue
        if ":" not in line:
            continue
        key, option = (part.strip() for part in line.split(":", 1))
        key = key.casefold()
        if key == "user-agent":
            if has_rule:
                agents.clear()
                has_rule = False
            agents.add(option.casefold())
        elif key == "sitemap":
            sitemap_urls.append(option)
        elif key in {"allow", "disallow"}:
            has_rule = True
            if key == "disallow" and option == "/" and "*" in agents:
                global_block = True
    return sitemap_urls, global_block


def audit_site(root: Path) -> tuple[int, int, list[Finding]]:
    """Return (sitemap URLs, generated indexable URLs, findings)."""
    issues: list[Finding] = []

    def add(code: str, severity: str, message: str, path: str = "", url: str = "") -> None:
        issues.append(Finding(code, severity, message, path, url))

    if not root.is_dir():
        add("CRAWL001", "ERROR", f"generated site directory is missing: {root}")
        return 0, 0, issues

    sitemap = root / "sitemap.xml"
    declared: list[str] = []
    if not sitemap.is_file():
        add("CRAWL001", "ERROR", "generated sitemap.xml is missing", "sitemap.xml", SITEMAP_URL)
    else:
        try:
            document = ET.parse(sitemap).getroot()
            if document.tag.rsplit("}", 1)[-1] != "urlset":
                add("CRAWL002", "ERROR", "expected XML sitemap urlset", "sitemap.xml", SITEMAP_URL)
            else:
                declared = [
                    (node.text or "").strip()
                    for node in document.findall("./{*}url/{*}loc")
                ]
                if not declared:
                    add("CRAWL002", "ERROR", "sitemap has no URLs", "sitemap.xml", SITEMAP_URL)
        except (ET.ParseError, UnicodeError, OSError) as exc:
            add("CRAWL002", "ERROR", f"cannot parse sitemap XML: {exc}", "sitemap.xml", SITEMAP_URL)

    for url, count in Counter(declared).items():
        if count > 1:
            add("CRAWL003", "ERROR", f"duplicate sitemap URL ({count} entries)", "sitemap.xml", url)
        try:
            parts = urlsplit(url)
            if (parts.scheme != "https" or parts.netloc != SITE_HOST
                    or parts.query or parts.fragment or parts.username or parts.password):
                add("CRAWL004", "ERROR", f"invalid sitemap URL: {url!r}", "sitemap.xml", url)
        except ValueError:
            add("CRAWL004", "ERROR", f"malformed sitemap URL: {url!r}", "sitemap.xml", url)

    robots = root / "robots.txt"
    if not robots.is_file():
        add("CRAWL010", "WARNING", "robots.txt is absent; crawlers can still discover the sitemap",
            "robots.txt", SITE_URL + "robots.txt")
    else:
        try:
            entries, blocked = robots_directives(robots.read_text(encoding="utf-8"))
            if blocked:
                add("CRAWL011", "ERROR", "wildcard robots group blocks the entire site with Disallow: /",
                    "robots.txt", SITE_URL + "robots.txt")
            if not entries:
                add("CRAWL012", "WARNING", "robots.txt does not advertise sitemap.xml",
                    "robots.txt", SITE_URL + "robots.txt")
            for entry in entries:
                if entry != SITEMAP_URL:
                    add("CRAWL013", "ERROR", f"robots.txt advertises an unexpected sitemap: {entry!r}",
                        "robots.txt", SITE_URL + "robots.txt")
        except (UnicodeError, OSError) as exc:
            add("CRAWL014", "ERROR", f"cannot read robots.txt: {exc}", "robots.txt",
                SITE_URL + "robots.txt")

    expected: dict[str, str] = {}
    for html in generated_pages(root):
        path = html.relative_to(root).as_posix()
        if path in EXCLUDED_HTML:
            continue
        try:
            markup = html.read_text(encoding="utf-8")
        except (UnicodeError, OSError) as exc:
            add("CRAWL020", "ERROR", f"cannot read rendered document: {exc}", path)
            continue
        if not re.search(r"<(?:!doctype\s+html|html\b)", markup, flags=re.I):
            continue
        page = SeoParser()
        page.feed(markup)
        page.close()
        if page.is_generated_redirect:
            continue
        if len(page.canonicals) != 1 or not page.canonicals[0]:
            add("CRAWL021", "ERROR", "indexable rendered page lacks exactly one canonical URL", path)
            continue
        url = page.canonicals[0]
        if url in expected:
            add("CRAWL022", "ERROR", f"multiple rendered pages share canonical {url!r} ({expected[url]})",
                path, url)
        expected[url] = path

    listed = set(declared)
    for url, path in expected.items():
        if url not in listed:
            add("CRAWL023", "ERROR", "indexable generated page is missing from the sitemap", path, url)
    for url in sorted(listed - set(expected)):
        add("CRAWL024", "ERROR", "sitemap URL has no corresponding indexable generated page",
            "sitemap.xml", url)

    if not expected:
        add("CRAWL025", "ERROR", "no indexable generated HTML pages were identified")
    return len(declared), len(expected), issues


def main() -> int:
    options = argparse.ArgumentParser(description=__doc__)
    options.add_argument("--site-dir", type=Path, default=Path("_site"))
    args = options.parse_args()
    in_sitemap, indexable, findings = audit_site(args.site_dir)
    errors = sum(item.severity == "ERROR" for item in findings)
    warnings = sum(item.severity == "WARNING" for item in findings)
    print(f"Crawlability audit: {in_sitemap} sitemap URLs, {indexable} indexable generated pages")
    for finding in findings:
        print(finding.display())
    print(f"Crawlability audit: {errors} critical error(s), {warnings} advisory warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
