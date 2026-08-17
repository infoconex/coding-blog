#!/usr/bin/env python3
from __future__ import annotations

import re
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

import yaml

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "post"
REQUIRED_FIELDS = ("title", "date", "description", "tags", "slug", "author", "originalUrl", "legacyPaths", "permalink")
DATED_POST_RE = re.compile(r"^/post/\d{4}/\d{2}/\d{2}/[^/]+/?$", re.I)
LINK_RE = re.compile(r"!?\[[^\]]*\]\((?P<url>[^)\s]+)")
LINKED_IMAGE_RE = re.compile(r"\[!\[[^\]]*\]\([^)]+\)\]\((?P<url>[^)\s]+)", re.I)
MARKDOWN_IMAGE_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<url>[^)\s]+)")
HTML_URL_RE = re.compile(r"(?:src|href)=[\"'](?P<url>[^\"']+)[\"']", re.I)
HTML_IMG_RE = re.compile(r"<img\b(?P<attrs>[^>]*)>", re.I)
ALT_ATTR_RE = re.compile(r"\balt=[\"'](?P<alt>[^\"']*)[\"']", re.I)
FENCE_RE = re.compile(r"^\s*```", re.M)
LEGACY_HOSTS = {"coding.infoconex.com", "www.coding.infoconex.com"}


def read_post(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError("missing YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise ValueError("invalid YAML frontmatter")
    data = yaml.safe_load(parts[1]) or {}
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return data, parts[2].lstrip("\r\n")


def urls(body: str) -> list[str]:
    found = [m.group("url") for m in LINK_RE.finditer(body)]
    found.extend(m.group("url") for m in LINKED_IMAGE_RE.finditer(body))
    found.extend(m.group("url") for m in HTML_URL_RE.finditer(body))
    return found


def route_key(path: str) -> str:
    clean = path.split("#", 1)[0].split("?", 1)[0].rstrip("/")
    clean = re.sub(r"\.aspx$", "", clean, flags=re.I)
    return clean.lower()


def expected_source_parts(permalink: str) -> tuple[str, str, str, str] | None:
    clean = re.sub(r"\.aspx$", "", permalink.rstrip("/"), flags=re.I)
    parts = clean.strip("/").split("/")
    if len(parts) != 5 or parts[0].lower() != "post":
        return None
    return parts[1], parts[2], parts[3], parts[4]


def normalized_tag(tag: str) -> str:
    return re.sub(r"\s+", " ", tag.strip()).casefold()


def main() -> int:
    files = sorted(POSTS.glob("*/*/*/*/index.md")) if POSTS.exists() else []
    errors: list[str] = []
    warnings: list[str] = []
    slugs: list[str] = []
    titles: list[tuple[str, str]] = []
    routes: dict[str, str] = {}
    bodies: dict[str, str] = {}

    if not files:
        errors.append("no post/YYYY/MM/DD/<historical-slug>/index.md files found")

    for required_path in (ROOT / "404.html", ROOT / "feed.xml", ROOT / "robots.txt", ROOT / "search.json"):
        if not required_path.is_file():
            errors.append(f"missing production artifact source: {required_path.relative_to(ROOT)}")

    for index_md in files:
        try:
            data, body = read_post(index_md)
        except Exception as exc:
            errors.append(f"{index_md}: {exc}")
            continue

        path_label = str(index_md.relative_to(ROOT))
        bodies[str(index_md)] = body
        missing = [field for field in REQUIRED_FIELDS if field not in data]
        if missing:
            errors.append(f"{path_label}: missing fields: {', '.join(missing)}")

        title = str(data.get("title") or "").strip()
        if title:
            titles.append((title.casefold(), path_label))
        else:
            errors.append(f"{path_label}: empty title")

        description = str(data.get("description") or "").strip()
        if description and not 40 <= len(description) <= 200:
            warnings.append(f"{path_label}: description length is {len(description)} characters; target 40-200")

        slug = str(data.get("slug") or "")
        if slug:
            slugs.append(slug)
        else:
            errors.append(f"{path_label}: empty slug")

        raw_date = str(data.get("date") or "")
        parsed_date: date | None = None
        try:
            parsed_date = date.fromisoformat(raw_date)
        except ValueError:
            errors.append(f"{path_label}: invalid ISO date {raw_date!r}")
        if parsed_date and parsed_date > date.today():
            errors.append(f"{path_label}: publication date is in the future: {raw_date}")

        tags = data.get("tags")
        if not isinstance(tags, list):
            errors.append(f"{path_label}: tags must be a list")
        else:
            seen_tags: set[str] = set()
            for tag in tags:
                if not isinstance(tag, str) or not tag.strip():
                    warnings.append(f"{path_label}: tag should be a non-empty string: {tag!r}")
                    continue
                normalized = normalized_tag(tag)
                if tag != tag.strip() or re.search(r"\s{2,}", tag):
                    warnings.append(f"{path_label}: normalize tag whitespace: {tag!r}")
                if normalized in seen_tags:
                    warnings.append(f"{path_label}: duplicate tag after normalization: {tag!r}")
                seen_tags.add(normalized)

        original = str(data.get("originalUrl") or "")
        parsed = urlsplit(original)
        if (parsed.hostname or "").lower() not in LEGACY_HOSTS:
            errors.append(f"{path_label}: unexpected originalUrl host: {original}")

        permalink = str(data.get("permalink") or "")
        if not DATED_POST_RE.match(permalink):
            errors.append(f"{path_label}: invalid historical permalink: {permalink}")
        elif permalink != parsed.path:
            errors.append(f"{path_label}: permalink must exactly match originalUrl path: {permalink} != {parsed.path}")
        else:
            key = route_key(permalink)
            if key in routes:
                errors.append(f"duplicate historical permalink: {permalink}")
            routes[key] = path_label

            expected = expected_source_parts(permalink)
            actual = index_md.relative_to(POSTS).parts[:4]
            if expected and tuple(actual) != expected:
                errors.append(
                    f"{path_label}: source path must mirror permalink date/slug; expected "
                    f"post/{'/'.join(expected)}/index.md"
                )

        legacy_paths = data.get("legacyPaths")
        if not isinstance(legacy_paths, list) or not legacy_paths:
            errors.append(f"{path_label}: legacyPaths must be a non-empty list")

        if len(FENCE_RE.findall(body)) % 2:
            errors.append(f"{path_label}: malformed Markdown code fences (odd number of ``` fences)")

        for match in MARKDOWN_IMAGE_RE.finditer(body):
            if not match.group("alt").strip():
                warnings.append(f"{path_label}: image missing alt text: {match.group('url')}")
        for match in HTML_IMG_RE.finditer(body):
            alt = ALT_ATTR_RE.search(match.group("attrs"))
            if not alt or not alt.group("alt").strip():
                warnings.append(f"{path_label}: HTML image missing alt text")

        for url in urls(body):
            clean = url.split("#", 1)[0].split("?", 1)[0]
            if not clean:
                continue
            if re.match(r"^[A-Za-z]:\\", clean):
                errors.append(f"{path_label}: absolute Windows path: {url}")
            if clean.startswith("images/"):
                target = index_md.parent / clean
                if not target.is_file():
                    errors.append(f"{path_label}: missing local image: {clean}")
            if clean.startswith("/images/posts/"):
                errors.append(f"{path_label}: old generated image URL remains: {url}")
            parsed_link = urlsplit(url)
            if (parsed_link.hostname or "").lower() in LEGACY_HOSTS and parsed_link.path.lower().startswith("/post/"):
                errors.append(f"{path_label}: historical post link should be root-relative: {url}")

        image_dir = index_md.parent / "images"
        if image_dir.exists():
            referenced = {
                (index_md.parent / u.split("#", 1)[0].split("?", 1)[0]).resolve()
                for u in urls(body)
                if u.startswith("images/")
            }
            for image in image_dir.rglob("*"):
                if image.is_file() and image.resolve() not in referenced:
                    warnings.append(f"{path_label}: orphaned image: {image.relative_to(index_md.parent)}")

    for slug, count in Counter(slugs).items():
        if slug and count > 1:
            errors.append(f"duplicate slug: {slug}")

    title_counts = Counter(title for title, _ in titles)
    for normalized_title, count in title_counts.items():
        if count > 1:
            paths = [path for title, path in titles if title == normalized_title]
            warnings.append(f"duplicate title across {count} posts: {', '.join(paths)}")

    for path, body in bodies.items():
        for url in urls(body):
            clean = url.split("#", 1)[0].split("?", 1)[0]
            if DATED_POST_RE.match(clean) and route_key(clean) not in routes:
                errors.append(f"{Path(path).relative_to(ROOT)}: broken historical internal link: {url}")
            elif re.match(r"^/post/[^/]+/?$", clean, re.I):
                errors.append(f"{Path(path).relative_to(ROOT)}: non-historical canonical post link remains: {url}")

    print(f"Posts checked:             {len(files)}")
    print(f"Unique slugs:              {len(set(slugs))}")
    print(f"Historical permalinks:     {len(routes)}")
    print(f"Errors:                    {len(errors)}")
    print(f"Warnings:                  {len(warnings)}")
    for message in warnings:
        print(f"WARNING: {message}")
    for message in errors:
        print(f"ERROR: {message}")

    if errors:
        print("Validation:                FAILED")
        return 1
    print("Validation:                PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
