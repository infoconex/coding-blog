#!/usr/bin/env python3
"""Validate canonical URLs, social metadata and BlogPosting JSON-LD in built HTML.

Run after Jekyll builds _site; no HTTP requests or indexing submissions.
This checks generated markup, not how search engines choose to display it.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ARTICLE_PATH = re.compile(r"^/post/\d{4}/\d{2}/\d{2}/[^/]+/?$")
SINGLE_META = ("og:image", "twitter:image", "twitter:card", "og:url")
SITE_HOST = "coding.infoconex.com"


class SeoParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta: dict[str, list[str]] = defaultdict(list)
        self.canonicals: list[str] = []
        self.json_ld: list[str] = []
        self._json_content: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "meta":
            key = data.get("property") or data.get("name")
            if key:
                self.meta[key.lower()].append(data.get("content") or "")
        elif tag == "link" and "canonical" in (data.get("rel") or "").lower().split():
            self.canonicals.append(data.get("href") or "")
        elif tag == "script" and (data.get("type") or "").lower() == "application/ld+json":
            self._json_content = []

    def handle_data(self, data: str) -> None:
        if self._json_content is not None:
            self._json_content.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._json_content is not None:
            self.json_ld.append("".join(self._json_content))
            self._json_content = None


def schema_nodes(value: object) -> list[dict]:
    if isinstance(value, list):
        return [node for child in value for node in schema_nodes(child)]
    if isinstance(value, dict):
        nodes = [value]
        if "@graph" in value:
            nodes.extend(schema_nodes(value["@graph"]))
        return nodes
    return []


def inspect_html(markup: str) -> list[str]:
    page = SeoParser()
    page.feed(markup)
    issues: list[str] = []

    # Generated redirect and auxiliary pages without canonical SEO metadata
    # are intentionally excluded from this audit.
    if not page.canonicals and not page.meta.get("og:url"):
        return issues

    if len(page.canonicals) != 1:
        issues.append(f"expected one canonical link, found {len(page.canonicals)}")
        return issues

    canonical = page.canonicals[0]
    parsed = urlsplit(canonical)
    if parsed.scheme != "https" or parsed.netloc != SITE_HOST:
        issues.append(f"unexpected canonical URL: {canonical!r}")

    for key in SINGLE_META:
        count = len(page.meta.get(key, []))
        if count != 1:
            issues.append(f"expected one {key} meta tag, found {count}")

    if page.meta.get("og:url") and page.meta["og:url"][0] != canonical:
        issues.append("og:url and canonical link disagree")

    if not ARTICLE_PATH.match(parsed.path):
        return issues

    found_nodes: list[dict] = []
    for raw in page.json_ld:
        try:
            found_nodes.extend(schema_nodes(json.loads(raw)))
        except json.JSONDecodeError as exc:
            issues.append(f"invalid JSON-LD: {exc.msg}")

    articles = [
        obj for obj in found_nodes
        if "BlogPosting" in (
            obj.get("@type", []) if isinstance(obj.get("@type"), list)
            else [obj.get("@type")]
        )
    ]
    if len(articles) != 1:
        issues.append(f"expected one BlogPosting schema, found {len(articles)}")
        return issues

    article = articles[0]
    for key in ("headline", "description", "datePublished", "dateModified", "url"):
        if not article.get(key):
            issues.append(f"BlogPosting missing {key}")

    author = article.get("author")
    authors = author if isinstance(author, list) else [author]
    if not any(
        isinstance(a, dict) and a.get("name") and a.get("url")
        for a in authors
    ):
        issues.append("BlogPosting author is missing name or profile URL")

    if article.get("url") and article["url"] != canonical:
        issues.append("BlogPosting URL and canonical link disagree")

    return issues


def generated_pages(root: Path) -> list[Path]:
    pages: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if path.suffix.lower() == ".html" or (
            path.suffix == "" and relative.parts and relative.parts[0] == "post"
        ):
            pages.append(path)
    return sorted(pages)


def audit_site(root: Path) -> tuple[int, int, list[str]]:
    if not root.is_dir():
        return 0, 0, [f"site directory not found: {root}"]
    pages = generated_pages(root)
    if not pages:
        return 0, 0, [f"no rendered HTML files found: {root}"]

    checked = 0
    articles = 0
    errors: list[str] = []
    for path in pages:
        markup = path.read_text(encoding="utf-8", errors="replace")
        if not re.search(r"<(?:!doctype\s+html|html\b)", markup, re.I):
            continue
        parser = SeoParser()
        parser.feed(markup)
        if not parser.canonicals and not parser.meta.get("og:url"):
            continue
        checked += 1
        if parser.canonicals and ARTICLE_PATH.match(urlsplit(parser.canonicals[0]).path):
            articles += 1
        errors.extend(
            f"{path.relative_to(root)}: {issue}"
            for issue in inspect_html(markup)
        )

    if not checked:
        errors.append("no rendered pages with canonical metadata found")
    if not articles:
        errors.append("no rendered BlogPosting pages found")
    return checked, articles, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=Path("_site"))
    args = parser.parse_args()
    checked, articles, errors = audit_site(args.site_dir)
    print(f"SEO audit: {checked} HTML pages, {articles} articles")
    for error in errors:
        print("ERROR: " + error)
    if errors:
        return 1
    print("Canonical, social-image and BlogPosting checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
