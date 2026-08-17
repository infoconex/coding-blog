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
LINKED_IMAGE_RE = re.compile(
    r"\[!\[[^\]]*\]\([^)]+\)\]\((?P<url>[^)\s]+)",
    re.I,
)
HTML_URL_RE = re.compile(r"(?:src|href)=[\"'](?P<url>[^\"']+)[\"']", re.I)
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
    # LINK_RE sees the embedded thumbnail in [![...](thumb)](full), but not
    # the outer full-size image target. Capture that target explicitly.
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


def main() -> int:
    files = sorted(POSTS.glob("*/*/*/*/index.md")) if POSTS.exists() else []
    errors: list[str] = []
    warnings: list[str] = []
    slugs: list[str] = []
    routes: dict[str, str] = {}
    bodies: dict[str, str] = {}

    if not files:
        errors.append("no post/YYYY/MM/DD/<historical-slug>/index.md files found")

    for index_md in files:
        try:
            data, body = read_post(index_md)
        except Exception as exc:
            errors.append(f"{index_md}: {exc}")
            continue

        bodies[str(index_md)] = body
        missing = [field for field in REQUIRED_FIELDS if field not in data]
        if missing:
            errors.append(f"{index_md}: missing fields: {', '.join(missing)}")

        slug = str(data.get("slug") or "")
        if slug:
            slugs.append(slug)
        else:
            errors.append(f"{index_md}: empty slug")

        raw_date = str(data.get("date") or "")
        try:
            date.fromisoformat(raw_date)
        except ValueError:
            errors.append(f"{index_md}: invalid ISO date {raw_date!r}")

        if not isinstance(data.get("tags"), list):
            errors.append(f"{index_md}: tags must be a list")

        original = str(data.get("originalUrl") or "")
        parsed = urlsplit(original)
        if (parsed.hostname or "").lower() not in LEGACY_HOSTS:
            errors.append(f"{index_md}: unexpected originalUrl host: {original}")

        permalink = str(data.get("permalink") or "")
        if not DATED_POST_RE.match(permalink):
            errors.append(f"{index_md}: invalid historical permalink: {permalink}")
        elif permalink != parsed.path:
            errors.append(f"{index_md}: permalink must exactly match originalUrl path: {permalink} != {parsed.path}")
        else:
            key = route_key(permalink)
            if key in routes:
                errors.append(f"duplicate historical permalink: {permalink}")
            routes[key] = str(index_md)

            expected = expected_source_parts(permalink)
            actual = index_md.relative_to(POSTS).parts[:4]
            if expected and tuple(actual) != expected:
                errors.append(
                    f"{index_md}: source path must mirror permalink date/slug; expected "
                    f"post/{'/'.join(expected)}/index.md"
                )

        legacy_paths = data.get("legacyPaths")
        if not isinstance(legacy_paths, list) or not legacy_paths:
            errors.append(f"{index_md}: legacyPaths must be a non-empty list")

        for url in urls(body):
            clean = url.split("#", 1)[0].split("?", 1)[0]
            if not clean:
                continue
            if re.match(r"^[A-Za-z]:\\", clean):
                errors.append(f"{index_md}: absolute Windows path: {url}")
            if clean.startswith("images/"):
                target = index_md.parent / clean
                if not target.is_file():
                    errors.append(f"{index_md}: missing local image: {clean}")
            if clean.startswith("/images/posts/"):
                errors.append(f"{index_md}: old generated image URL remains: {url}")
            parsed_link = urlsplit(url)
            if (
                (parsed_link.hostname or "").lower() in LEGACY_HOSTS
                and parsed_link.path.lower().startswith("/post/")
            ):
                errors.append(f"{index_md}: historical post link should be root-relative: {url}")

        image_dir = index_md.parent / "images"
        if image_dir.exists():
            referenced = {
                (index_md.parent / u.split("#", 1)[0].split("?", 1)[0]).resolve()
                for u in urls(body)
                if u.startswith("images/")
            }
            for image in image_dir.rglob("*"):
                if image.is_file() and image.resolve() not in referenced:
                    warnings.append(f"{index_md}: orphaned image: {image.relative_to(index_md.parent)}")

    for slug, count in Counter(slugs).items():
        if slug and count > 1:
            errors.append(f"duplicate slug: {slug}")

    for path, body in bodies.items():
        for url in urls(body):
            clean = url.split("#", 1)[0].split("?", 1)[0]
            if DATED_POST_RE.match(clean) and route_key(clean) not in routes:
                errors.append(f"{path}: broken historical internal link: {url}")
            elif re.match(r"^/post/[^/]+/?$", clean, re.I):
                errors.append(f"{path}: non-historical canonical post link remains: {url}")

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
