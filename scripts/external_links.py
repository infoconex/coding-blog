#!/usr/bin/env python3
"""Apply an external-link policy to Jekyll's generated HTML, not Markdown.

The GitHub Pages Jekyll build does not permit arbitrary render hooks. This
post-build step changes only opening anchor tags, leaving everything else,
including SEO/JSON-LD, code samples, and historical articles, byte-for-byte
unchanged in the published output.
"""
from __future__ import annotations

import argparse
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

SITE_HOSTS = {"coding.infoconex.com", "www.coding.infoconex.com"}
REQUIRED_REL = ("noopener", "noreferrer")
REPRESENTATIVE_ARTICLES = (
    "post/2008/08/23/BlueQuartz-installing-Mono",
    "post/2010/10/11/ASPNET-CustomValidator-that-validates-multiple-controls-using-both-Server-Side-and-Client-Side-scripting",
    "post/2026/11/09/editorconfig-dotnet-framework-4-8-verify-code-style",
)


def is_external_http_url(href: str) -> bool:
    """Treat scheme-relative HTTP(S) links as external, but not local links."""
    href = href.strip()
    try:
        parsed = urlsplit(href)
        http_link = parsed.scheme.lower() in {"http", "https"} or (
            href.startswith("//") and not parsed.scheme
        )
        return bool(http_link and parsed.hostname and parsed.hostname.lower() not in SITE_HOSTS)
    except ValueError:  # Bad IPv6 / port / netloc: not a valid link to rewrite.
        return False


def attribute_spans(tag: str) -> dict[str, tuple[int, int]]:
    """Locate original attribute spans without matching inside quoted values."""
    spans: dict[str, tuple[int, int]] = {}
    position = 2  # After '<a'. HTMLParser only calls us for actual <a> tags.
    while position < len(tag):
        while position < len(tag) and tag[position].isspace():
            position += 1
        if position == len(tag) or tag[position] in "/>":
            break
        start = position
        while position < len(tag) and not tag[position].isspace() and tag[position] not in "= />":
            position += 1
        if start == position:
            break
        key = tag[start:position].lower()
        while position < len(tag) and tag[position].isspace():
            position += 1
        if position < len(tag) and tag[position] == "=":
            position += 1
            while position < len(tag) and tag[position].isspace():
                position += 1
            if position < len(tag) and tag[position] in "\"'":
                quote = tag[position]
                position += 1
                while position < len(tag) and tag[position] != quote:
                    position += 1
                if position < len(tag):
                    position += 1
            else:
                while position < len(tag) and not tag[position].isspace() and tag[position] != ">":
                    position += 1
        spans[key] = (start, position)
    return spans


def rewrite_anchor(tag: str, attrs: list[tuple[str, str | None]]) -> str:
    attributes = dict(attrs)
    href = attributes.get("href")
    if not href or not is_external_http_url(href):
        return tag
    # Respect deliberate navigation overrides and download semantics.
    if "download" in attributes:
        return tag
    target = (attributes.get("target") or "").strip().lower()
    if target not in {"", "_blank"}:
        return tag

    rel = (attributes.get("rel") or "").split()
    present = {token.lower() for token in rel}
    added_rel = [token for token in REQUIRED_REL if token not in present]
    if target == "_blank" and not added_rel:
        return tag  # Keeps the current EditorConfig article unchanged.

    spans = attribute_spans(tag)
    edits: list[tuple[int, int, str]] = []
    additions: list[str] = []
    if target != "_blank":
        if "target" in spans:
            start, end = spans["target"]
            edits.append((start, end, 'target="_blank"'))
        else:
            additions.append('target="_blank"')
    if added_rel:
        new_rel = escape(" ".join(rel + added_rel), quote=True)
        if "rel" in spans:
            start, end = spans["rel"]
            edits.append((start, end, f'rel="{new_rel}"'))
        else:
            additions.append(f'rel="{new_rel}"')
    if additions:
        # Insert before the closing bracket, or before '/>' if self-closing.
        end = tag.rfind(">")
        position = end - 1 if tag[end - 1] == "/" else end
        edits.append((position, position, " " + " ".join(additions)))
    for start, end, replacement in sorted(edits, reverse=True):
        tag = tag[:start] + replacement + tag[end:]
    return tag


class ExternalLinkParser(HTMLParser):
    """Record precise substitutions rather than serializing the HTML tree."""

    def __init__(self, markup: str) -> None:
        super().__init__(convert_charrefs=True)
        self.markup = markup
        self.offsets = [0]
        for row in markup.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(row))
        self.edits: list[tuple[int, int, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        original = self.get_starttag_text() or ""
        replacement = rewrite_anchor(original, attrs)
        if replacement != original:
            line, column = self.getpos()
            start = self.offsets[line - 1] + column
            self.edits.append((start, start + len(original), replacement))


def rewrite_html(markup: str) -> tuple[str, int]:
    parser = ExternalLinkParser(markup)
    parser.feed(markup)
    parser.close()
    for start, end, replacement in reversed(parser.edits):
        markup = markup[:start] + replacement + markup[end:]
    return markup, len(parser.edits)


def process_site(site_dir: Path, check: bool = False) -> tuple[int, int, list[str]]:
    if not site_dir.is_dir():
        return 0, 0, [f"Site output not found: {site_dir}"]
    # Historical Jekyll permalinks without a trailing slash can be built as
    # extensionless HTML files. Treat them as pages, not just *.html files.
    pages = sorted(path for path in site_dir.rglob("*") if path.is_file() and (
        path.suffix.lower() == ".html" or (
            not path.suffix and path.relative_to(site_dir).parts[0] == "post"
        )
    ))
    if not pages:
        return 0, 0, [f"No HTML pages found in: {site_dir}"]
    issues: list[str] = []
    modified_pages = 0
    modified_links = 0
    for path in pages:
        original = path.read_text(encoding="utf-8")
        updated, changed = rewrite_html(original)
        if changed:
            modified_pages += 1
            modified_links += changed
            if check:
                issues.append(f"{path.relative_to(site_dir)}: {changed} external links violate the policy")
            else:
                path.write_text(updated, encoding="utf-8")
    if check:
        for article in REPRESENTATIVE_ARTICLES:
            candidates = (site_dir / article, site_dir / article / "index.html",
                          site_dir / (article + ".html"))
            if not any(candidate.is_file() for candidate in candidates):
                issues.append(f"Missing representative article: {article}")
    print(f"Checked {len(pages)} generated HTML pages; {modified_links} links in {modified_pages} pages "
          + ("need changes." if check else "updated."))
    return len(pages), modified_links, issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=Path("_site"))
    parser.add_argument("--check", action="store_true", help="Check the transformed site without writing")
    args = parser.parse_args()
    _, _, errors = process_site(args.site_dir, check=args.check)
    for error in errors:
        print("ERROR: " + error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
