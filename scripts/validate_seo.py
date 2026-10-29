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
from urllib.parse import unquote, urljoin, urlsplit


ARTICLE_PATH = re.compile(r"^/post/\d{4}/\d{2}/\d{2}/[^/]+/?$")
SINGLE_META = ("og:image", "twitter:image", "twitter:card", "og:url")
SITE_HOST = "coding.infoconex.com"
SITE_URL = "https://" + SITE_HOST + "/"
ARTICLE_FILE = re.compile(r"^post/\d{4}/\d{2}/\d{2}/[^/]+(?:/index\.html|\.html)?$")


class SeoParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta: dict[str, list[str]] = defaultdict(list)
        self.canonicals: list[str] = []
        self.json_ld: list[str] = []
        self._json_content: list[str] | None = None
        self.is_redirect = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "meta":
            if (data.get("http-equiv") or "").lower() == "refresh":
                self.is_redirect = True
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


def inspect_html(markup: str, *, require_metadata: bool = False) -> list[str]:
    page = SeoParser()
    page.feed(markup)
    issues: list[str] = []

    # Generated redirect and auxiliary pages without canonical SEO metadata
    # are intentionally excluded from this audit.
    if not page.canonicals and not page.meta.get("og:url"):
        if require_metadata:
            return ["article missing canonical link and og:url metadata"]
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

    if not require_metadata and not ARTICLE_PATH.match(parsed.path):
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
    # Google recommends an author profile URL when one exists, but author.name
    # is the required identity property. Preserve historical guest authors
    # without inventing profiles or attributing their work to Jim Scott.
    named_authors = [
        a for a in authors
        if isinstance(a, dict) and isinstance(a.get("name"), str) and a["name"].strip()
    ]
    if not named_authors:
        issues.append("BlogPosting author is missing a name")
    elif not any(
        a["name"] != "Jim Scott"
        or a.get("url") == "https://coding.infoconex.com/about/"
        for a in named_authors
    ):
        issues.append("BlogPosting author Jim Scott is missing the correct profile URL")

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


def missing_social_images(root: Path, page: SeoParser) -> list[str]:
    """Ensure same-site OG/Twitter images actually exist in the Jekyll output."""
    issues: list[str] = []
    canonical = page.canonicals[0] if page.canonicals else SITE_URL
    for property_name in ("og:image", "twitter:image"):
        for source in page.meta.get(property_name, []):
            if not source:
                issues.append(f"{property_name} has an empty URL")
                continue
            resolved = urlsplit(urljoin(canonical, source))
            if resolved.netloc.lower() != SITE_HOST:
                continue
            if resolved.scheme != "https":
                issues.append(f"{property_name} uses non-HTTPS local URL: {source!r}")
                continue
            destination = (root / unquote(resolved.path).lstrip("/")).resolve()
            if not destination.is_relative_to(root.resolve()) or not destination.is_file():
                issues.append(f"{property_name} references missing local image: {source!r}")
    return issues


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
        relative = path.relative_to(root).as_posix()
        is_article_file = bool(ARTICLE_FILE.match(relative))
        # jekyll-redirect-from emits a canonical link to the destination
        # but intentionally omits social tags. Do not audit redirects as pages.
        if parser.is_redirect:
            continue
        if not parser.canonicals and not parser.meta.get("og:url") and not is_article_file:
            continue
        checked += 1
        if is_article_file or (
            parser.canonicals and ARTICLE_PATH.match(urlsplit(parser.canonicals[0]).path)
        ):
            articles += 1
        page_issues = inspect_html(markup, require_metadata=is_article_file)
        if is_article_file and parser.canonicals:
            # Direct-to-file pages and folder/index pages have the same
            # historical URL except for a possible trailing slash.
            if relative.endswith("/index.html"):
                expected = "/post/" + relative[len("post/") : -len("/index.html")]
            elif relative.endswith(".html"):
                expected = "/post/" + relative[len("post/") : -5]
            else:
                expected = "/" + relative
            canonical_path = urlsplit(parser.canonicals[0]).path.rstrip("/")
            if canonical_path != expected.rstrip("/"):
                page_issues.append(
                    f"article canonical path {canonical_path!r} differs from built article URL {expected!r}"
                )
        page_issues.extend(missing_social_images(root, parser))
        errors.extend(f"{relative}: {issue}" for issue in page_issues)

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
