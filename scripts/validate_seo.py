#!/usr/bin/env python3
"""Validate indexable Jekyll HTML before GitHub Pages deployment.

Only ERROR findings block publication. WARNING findings are advisory.
No HTTP requests, content edits, or indexing submissions are performed.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


SITE_HOST = "coding.infoconex.com"
SITE_URL = "https://" + SITE_HOST + "/"
AUTHOR_URL = SITE_URL + "about/"
PORTRAIT_URL = SITE_URL + "assets/images/about/jim-scott.webp"
ARTICLE_PATH = re.compile(r"^/post/\d{4}/\d{2}/\d{2}/[^/]+/?$")
ARTICLE_FILE = re.compile(r"^post/\d{4}/\d{2}/\d{2}/[^/]+(?:/index\.html|\.html)?$")
SOCIAL_KEYS = ("og:url", "og:title", "og:description", "og:image",
               "twitter:card", "twitter:image")


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    message: str
    file: str = ""
    url: str = ""

    def display(self) -> str:
        location = f"{self.file} [{self.url}]: " if self.file else ""
        return f"{self.severity} {self.code}: {location}{self.message}"


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
            if (data.get("http-equiv") or "").lower() == "refresh" and re.match(
                r"^\s*\d+\s*;\s*url\s*=", data.get("content") or "", re.I
            ):
                self.is_redirect = True
            key = data.get("property") or data.get("name")
            if key:
                self.meta[key.lower()].append(data.get("content") or "")
        elif tag == "link" and "canonical" in (data.get("rel") or "").lower().split():
            self.canonicals.append(data.get("href") or "")
        elif tag == "script" and (data.get("type") or "").lower().split(";")[0].strip() == "application/ld+json":
            self._json_content = []

    def handle_data(self, data: str) -> None:
        if self._json_content is not None:
            self._json_content.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._json_content is not None:
            self.json_ld.append("".join(self._json_content))
            self._json_content = None

    def close(self) -> None:
        super().close()
        if self._json_content is not None:
            self.json_ld.append("".join(self._json_content))
            self._json_content = None

    @property
    def is_generated_redirect(self) -> bool:
        # A normal page containing a stray refresh tag must not bypass SEO.
        robots = " ".join(self.meta.get("robots", [])).lower()
        return self.is_redirect and (
            "noindex" in robots
            or (not self.meta.get("og:url") and not self.json_ld)
        )


def schema_nodes(value: object) -> list[dict]:
    """Accept a JSON-LD object, array, @graph, or a mixture of those forms."""
    if isinstance(value, list):
        return [node for child in value for node in schema_nodes(child)]
    if isinstance(value, dict):
        return [value] + schema_nodes(value["@graph"]) if "@graph" in value else [value]
    return []


def has_type(node: dict, type_name: str) -> bool:
    types = node.get("@type", [])
    return type_name in (types if isinstance(types, list) else [types])


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def valid_date(value: object) -> bool:
    if not nonempty(value):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def valid_absolute_url(value: object) -> bool:
    if not nonempty(value):
        return False
    try:
        parsed = urlsplit(value)
        return parsed.scheme == "https" and bool(parsed.hostname) and not (
            parsed.username or parsed.password or parsed.fragment
        )
    except ValueError:
        return False


def image_urls(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [url for item in value for url in image_urls(item)]
    if isinstance(value, dict):
        url = value.get("url") or value.get("contentUrl")
        return [url] if isinstance(url, str) else []
    return []


def inspect_page(page: SeoParser, *, article: bool, about: bool,
                 expected_url: str | None = None) -> list[Finding]:
    issues: list[Finding] = []

    def add(code: str, severity: str, message: str) -> None:
        issues.append(Finding(code, severity, message))

    if len(page.canonicals) == 0:
        add("SEO001", "ERROR", "missing canonical link on indexable page")
    elif len(page.canonicals) != 1:
        add("SEO002", "ERROR", f"expected one canonical link, found {len(page.canonicals)}")

    canonical = page.canonicals[0] if len(page.canonicals) == 1 else ""
    try:
        parsed = urlsplit(canonical)
    except ValueError:
        add("SEO003", "ERROR", f"malformed canonical URL: {canonical!r}")
        parsed = urlsplit("")
    if canonical:
        if (parsed.scheme != "https" or parsed.netloc != SITE_HOST
                or parsed.query or parsed.fragment or parsed.username or parsed.password
                or ";" in parsed.path):
            add("SEO003", "ERROR", f"unexpected canonical URL: {canonical!r}")
        if expected_url and parsed.path.rstrip("/") != urlsplit(expected_url).path.rstrip("/"):
            kind = "article " if article else ""
            add("SEO004", "ERROR",
                f"{kind}canonical path {parsed.path!r} differs from built page URL {urlsplit(expected_url).path!r}")

    directives = " ".join(page.meta.get("robots", [])).lower()
    if re.search(r"\bnoindex\b", directives):
        add("SEO006", "ERROR", "indexable page unexpectedly contains robots noindex")

    for key in SOCIAL_KEYS:
        values = page.meta.get(key, [])
        if len(values) > 1:
            add("SEO010", "ERROR", f"expected one {key} meta tag, found {len(values)}")
        elif not values or not nonempty(values[0]):
            add("SEO011", "WARNING", f"{key} is missing or empty")
    if canonical and page.meta.get("og:url") and page.meta["og:url"][0] != canonical:
        add("SEO012", "ERROR", "og:url and canonical link disagree")

    found_nodes: list[dict] = []
    for raw in page.json_ld:
        try:
            found_nodes.extend(schema_nodes(json.loads(raw)))
        except (json.JSONDecodeError, TypeError) as exc:
            add("SEO020", "ERROR", f"invalid JSON-LD: {exc}")

    if article:
        articles = [node for node in found_nodes if has_type(node, "BlogPosting")]
        if len(articles) != 1:
            add("SEO021", "ERROR", f"expected one BlogPosting schema, found {len(articles)}")
        else:
            post = articles[0]
            for key in ("headline", "description", "url"):
                if not nonempty(post.get(key)):
                    add("SEO022", "ERROR", f"BlogPosting missing {key}")
            for key in ("datePublished", "dateModified"):
                if not valid_date(post.get(key)):
                    add("SEO023", "ERROR", f"BlogPosting has missing or invalid {key}")
            authors = post.get("author")
            authors = authors if isinstance(authors, list) else [authors]
            named = [
                author for author in authors
                if isinstance(author, dict) and nonempty(author.get("name"))
            ]
            if not named:
                add("SEO024", "ERROR", "BlogPosting author is missing a name")
            elif not any(
                author["name"] != "Jim Scott" or author.get("url") == AUTHOR_URL
                for author in named
            ):
                add("SEO025", "ERROR",
                    "BlogPosting author Jim Scott is missing the correct profile URL")
            if canonical and post.get("url") and post["url"] != canonical:
                add("SEO026", "ERROR", "BlogPosting URL and canonical link disagree")
            if "image" in post and not image_urls(post["image"]):
                add("SEO027", "ERROR", "BlogPosting image has no usable URL")
            for value in image_urls(post.get("image")):
                if not valid_absolute_url(urljoin(canonical or SITE_URL, value)):
                    add("SEO027", "ERROR", f"BlogPosting image has invalid URL: {value!r}")

    if about:
        profiles = [node for node in found_nodes if has_type(node, "ProfilePage")]
        if len(profiles) != 1:
            add("SEO030", "ERROR", f"expected one ProfilePage schema, found {len(profiles)}")
        else:
            profile = profiles[0]
            if profile.get("url") != AUTHOR_URL or canonical != AUTHOR_URL:
                add("SEO031", "ERROR", "ProfilePage URL must match canonical About URL")
            person = profile.get("mainEntity")
            if not isinstance(person, dict) or not has_type(person, "Person"):
                add("SEO032", "ERROR", "ProfilePage mainEntity must be a Person")
            else:
                if person.get("name") != "Jim Scott" or person.get("url") != AUTHOR_URL:
                    add("SEO033", "ERROR", "ProfilePage Person name or profile URL is incorrect")
                if PORTRAIT_URL not in image_urls(person.get("image")):
                    add("SEO034", "ERROR", "ProfilePage portrait image reference is incorrect")
                if not nonempty(person.get("jobTitle")) or not nonempty(person.get("description")):
                    add("SEO035", "ERROR", "ProfilePage professional identity metadata is incomplete")
                same_as = person.get("sameAs")
                if not isinstance(same_as, list) or not same_as or not all(
                    valid_absolute_url(link) for link in same_as
                ):
                    add("SEO036", "ERROR", "ProfilePage sameAs identity links are invalid")

    return issues


def inspect_html(markup: str, *, require_metadata: bool = False) -> list[str]:
    """Compatibility interface for targeted tests; errors only, no local assets."""
    parser = SeoParser()
    parser.feed(markup)
    parser.close()
    if parser.is_generated_redirect:
        return []
    canonical = parser.canonicals[0] if len(parser.canonicals) == 1 else ""
    try:
        path = urlsplit(canonical).path
    except ValueError:
        path = ""
    issues = inspect_page(parser, article=require_metadata or bool(ARTICLE_PATH.match(path)),
                          about=path.rstrip("/") == "/about")
    return [item.message for item in issues if item.severity == "ERROR"]


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


def intended_url(relative: str, article: bool) -> str:
    if relative == "index.html":
        path = "/"
    elif relative.endswith("/index.html"):
        path = "/" + relative[:-len("index.html")]
    elif relative.endswith(".html"):
        path = "/" + relative[:-5] + ("" if article else ".html")
    else:
        path = "/" + relative
    return SITE_URL.rstrip("/") + path


def check_local_image(root: Path, source: str, base_url: str) -> str | None:
    if not nonempty(source):
        return "empty image URL"
    try:
        resolved = urlsplit(urljoin(base_url, source))
        if resolved.hostname != SITE_HOST:
            return None
        if resolved.scheme != "https" or resolved.netloc != SITE_HOST:
            return f"non-HTTPS local URL: {source!r}"
        destination = (root / unquote(resolved.path).lstrip("/")).resolve()
        if not destination.is_relative_to(root.resolve()) or not destination.is_file():
            return f"missing local image: {source!r}"
    except (ValueError, OSError) as exc:
        return f"invalid local image reference {source!r}: {exc}"
    return None


def audit_site_detailed(root: Path) -> tuple[int, int, list[Finding]]:
    if not root.is_dir():
        return 0, 0, [Finding("SEO900", "ERROR", f"site directory not found: {root}")]
    pages = generated_pages(root)
    if not pages:
        return 0, 0, [Finding("SEO900", "ERROR", f"no rendered HTML files found: {root}")]

    checked = 0
    articles = 0
    findings: list[Finding] = []
    canonical_owners: dict[str, str] = {}
    for path in pages:
        relative = path.relative_to(root).as_posix()
        article = bool(ARTICLE_FILE.fullmatch(relative))
        expected = intended_url(relative, article)
        try:
            markup = path.read_text(encoding="utf-8")  # fail closed on corrupt encoding
        except (UnicodeError, OSError) as exc:
            findings.append(Finding("SEO900", "ERROR", f"cannot read generated HTML: {exc}",
                                    relative, expected))
            continue
        if not re.search(r"<(?:!doctype\s+html|html\b)", markup, re.I):
            continue  # assets or fragments are not indexable HTML documents
        parser = SeoParser()
        parser.feed(markup)
        parser.close()
        if parser.is_generated_redirect:
            continue
        checked += 1
        if article:
            articles += 1
        about = relative in {"about/index.html", "about.html"}
        page_findings = inspect_page(parser, article=article, about=about,
                                     expected_url=expected)

        if len(parser.canonicals) == 1:
            canonical = parser.canonicals[0]
            key = canonical.rstrip("/")
            if key in canonical_owners:
                page_findings.append(Finding(
                    "SEO005", "ERROR",
                    f"canonical URL is shared with unrelated page {canonical_owners[key]!r}"))
            else:
                canonical_owners[key] = relative

        base = parser.canonicals[0] if len(parser.canonicals) == 1 else expected
        for key in ("og:image", "twitter:image"):
            for source in parser.meta.get(key, []):
                problem = check_local_image(root, source, base)
                if problem:
                    page_findings.append(Finding("SEO040", "ERROR", f"{key} references {problem}"))

        for raw in parser.json_ld:
            try:
                nodes = schema_nodes(json.loads(raw))
            except (json.JSONDecodeError, TypeError):
                continue  # already reported SEO020
            if article:
                for node in nodes:
                    if has_type(node, "BlogPosting"):
                        for source in image_urls(node.get("image")):
                            problem = check_local_image(root, source, base)
                            if problem:
                                page_findings.append(Finding("SEO041", "ERROR",
                                                             f"BlogPosting image references {problem}"))
            if about:
                problem = check_local_image(root, PORTRAIT_URL, base)
                if problem:
                    page_findings.append(Finding("SEO042", "ERROR",
                                                 f"ProfilePage portrait references {problem}"))

        findings.extend(Finding(item.code, item.severity, item.message, relative, expected)
                        for item in page_findings)

    if checked == 0:
        findings.append(Finding("SEO900", "ERROR", "no indexable rendered HTML pages found"))
    if articles == 0:
        findings.append(Finding("SEO900", "ERROR", "no rendered BlogPosting pages found"))
    return checked, articles, findings


def audit_site(root: Path) -> tuple[int, int, list[str]]:
    """Legacy interface; only critical errors fail the build."""
    pages, articles, findings = audit_site_detailed(root)
    return pages, articles, [f.display() for f in findings if f.severity == "ERROR"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=Path("_site"))
    options = parser.parse_args()
    pages, articles, findings = audit_site_detailed(options.site_dir)
    print(f"SEO audit: {pages} HTML pages, {articles} articles")
    for finding in findings:
        print(finding.display())
    errors = sum(f.severity == "ERROR" for f in findings)
    warnings = sum(f.severity == "WARNING" for f in findings)
    print(f"SEO audit: {errors} critical error(s), {warnings} advisory warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
