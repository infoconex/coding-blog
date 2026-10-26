#!/usr/bin/env python3
"""Validate rendered image accessibility and local image destinations.

Run AFTER the Jekyll build against _site. The page's canonical URL is used
for resolving relative links, matching what visitors see at that URL.
No network requests, publication, or indexing submissions occur here.
"""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

SITE = "https://coding.infoconex.com/"
EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg", ".bmp", ".ico")
GENERIC_ALT = frozenset({"image", "img", "picture", "photo", "screenshot", "thumbnail", "graphic"})


class ImageTagParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.images: list[tuple[int, dict[str, str | None]]] = []
        self.links: list[tuple[int, dict[str, str | None]]] = []
        self.canonical: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "img":
            self.images.append((self.getpos()[0], values))
        elif tag == "a":
            self.links.append((self.getpos()[0], values))
        elif tag == "link" and "canonical" in (values.get("rel") or "").lower().split():
            self.canonical = values.get("href")


def page_url(site_root: Path, html_file: Path, canonical: str | None) -> str:
    if canonical:
        url = urlsplit(canonical)
        if url.scheme in {"https", "http"} and url.netloc == urlsplit(SITE).netloc:
            return canonical
    relative = html_file.relative_to(site_root).as_posix()
    if relative == "index.html":
        return SITE
    if relative.endswith("/index.html"):
        return urljoin(SITE, relative[:-10] + "/")
    if relative.endswith(".html"):
        return urljoin(SITE, relative[:-5])
    return urljoin(SITE, relative)


def is_image_url(url: str) -> bool:
    return urlsplit(url).path.lower().endswith(EXTENSIONS)


def missing_local_image(site_root: Path, source_url: str, url: str) -> str | None:
    # Third-party and data images are out of scope for asset existence checks,
    # but <img> alt text is still validated below.
    resolved = urlsplit(urljoin(source_url, url))
    host = urlsplit(SITE).netloc
    if resolved.netloc != host or resolved.scheme not in {"http", "https"}:
        return None
    path = unquote(resolved.path).lstrip("/")
    root = site_root.resolve()
    target = (root / path).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        return resolved.geturl()
    return None


def audit_site(site_root: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    count = 0
    pages = sorted(site_root.rglob("*.html"))
    if not pages:
        return 0, [f"Site has no generated HTML: {site_root}"]

    for html_file in pages:
        document = ImageTagParser()
        document.feed(html_file.read_text(encoding="utf-8", errors="replace"))
        url = page_url(site_root, html_file, document.canonical)
        page = html_file.relative_to(site_root).as_posix()

        for line, attrs in document.images:
            count += 1
            alt = attrs.get("alt")
            decorative = attrs.get("role") in {"presentation", "none"} or attrs.get("aria-hidden") == "true"
            if alt is None:
                errors.append(f"{page}:{line}: <img> is missing an alt attribute")
            elif not alt.strip() and not decorative:
                errors.append(f"{page}:{line}: informative image has empty alt text")
            elif alt.strip().casefold() in GENERIC_ALT:
                errors.append(f"{page}:{line}: non-descriptive image alt text: {alt!r}")

            src = attrs.get("src")
            if not src:
                errors.append(f"{page}:{line}: <img> is missing its src")
            else:
                missing = missing_local_image(site_root, url, src)
                if missing:
                    errors.append(f"{page}:{line}: broken image src {src!r} -> {missing}")

            # Also catch srcset local image files; entries are URL plus size hints.
            for candidate in (attrs.get("srcset") or "").split(","):
                entry = candidate.strip().split()
                if not entry:
                    continue
                missing = missing_local_image(site_root, url, entry[0])
                if missing:
                    errors.append(f"{page}:{line}: broken image srcset {entry[0]!r} -> {missing}")

        for line, attrs in document.links:
            href = attrs.get("href")
            if href and is_image_url(href):
                missing = missing_local_image(site_root, url, href)
                if missing:
                    errors.append(f"{page}:{line}: broken clickable image href {href!r} -> {missing}")

    return count, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=Path("_site"))
    options = parser.parse_args()
    images, errors = audit_site(options.site_dir)
    print(f"Image audit: examined {images} rendered images")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Image audit: {len(errors)} issue(s) found")
        return 1
    print("Image audit: no missing/local broken image links or missing/generic alt text")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
