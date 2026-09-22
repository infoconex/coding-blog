#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "post"
LEGACY_HOSTS = {"coding.infoconex.com", "www.coding.infoconex.com"}
LINK_RE = re.compile(r"!?\[[^\]]*\]\((?P<url>[^)\s]+)")
LINKED_IMAGE_RE = re.compile(r"\[!\[[^\]]*\]\([^)]+\)\]\((?P<url>[^)\s]+)", re.I)
HTML_URL_RE = re.compile(r"(?:src|href)=[\"'](?P<url>[^\"']+)[\"']", re.I)


def urls(body: str) -> list[str]:
    found = [m.group("url") for m in LINK_RE.finditer(body)]
    found.extend(m.group("url") for m in LINKED_IMAGE_RE.finditer(body))
    found.extend(m.group("url") for m in HTML_URL_RE.finditer(body))
    return found


def main() -> int:
    errors: list[str] = []
    files = sorted(POSTS.glob("*/*/*/*/index.md")) if POSTS.exists() else []

    for index_md in files:
        body = index_md.read_text(encoding="utf-8")
        path_label = index_md.relative_to(ROOT)

        for url in urls(body):
            parsed = urlsplit(url)
            path = parsed.path
            host = (parsed.hostname or "").lower()

            if not parsed.scheme and not parsed.netloc and path.lower().startswith("/blog/"):
                errors.append(f"{path_label}: obsolete /blog/ internal link: {url}")

            if path.lower() == "/file.axd" and (not host or host in LEGACY_HOSTS):
                errors.append(f"{path_label}: obsolete file.axd link: {url}")

    print(f"Posts checked:             {len(files)}")
    print(f"Obsolete link errors:      {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print("Internal link validation:  FAILED")
        return 1

    print("Internal link validation:  PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
