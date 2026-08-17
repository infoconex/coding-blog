#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PRODUCTION_ROOTS = [
    ROOT / "_layouts",
    ROOT / "_includes",
    ROOT / "assets",
    ROOT / "post",
    ROOT / "writing",
    ROOT / "archive",
]
PRODUCTION_FILES = [
    ROOT / "index.html",
    ROOT / "about.md",
    ROOT / "404.html",
    ROOT / "search.json",
    ROOT / "feed.xml",
    ROOT / "robots.txt",
]
TEXT_SUFFIXES = {".html", ".md", ".css", ".js", ".json", ".xml", ".txt"}
TARGET_DOMAIN = "coding.infoconex.com"
TARGET_URL = f"https://{TARGET_DOMAIN}"


def source_files():
    for root in PRODUCTION_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                yield path
    for path in PRODUCTION_FILES:
        if path.is_file():
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Coding blog sources for custom-domain cutover readiness.")
    parser.add_argument("--cutover-ready", action="store_true", help="Also require live custom-domain config and CNAME.")
    args = parser.parse_args()

    errors: list[str] = []
    for path in source_files():
        text = path.read_text(encoding="utf-8")
        if "/coding-blog/" in text or "infoconex.github.io/coding-blog" in text:
            errors.append(f"hard-coded project Pages path in {path.relative_to(ROOT)}")

    config_path = ROOT / "_config.yml"
    config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}

    if args.cutover_ready:
        if config.get("url") != TARGET_URL:
            errors.append(f"_config.yml url must be {TARGET_URL!r} for cutover")
        if config.get("baseurl") not in ("", None):
            errors.append("_config.yml baseurl must be empty for the custom domain")
        cname = ROOT / "CNAME"
        if not cname.is_file():
            errors.append("CNAME file is missing")
        elif cname.read_text(encoding="utf-8").strip() != TARGET_DOMAIN:
            errors.append(f"CNAME must contain only {TARGET_DOMAIN}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print("Custom-domain preflight: FAILED")
        return 1

    print("No hard-coded /coding-blog/ production links found.")
    if args.cutover_ready:
        print(f"Custom-domain config and CNAME are ready for {TARGET_DOMAIN}.")
    else:
        print("Source is migration-safe. Re-run with --cutover-ready during activation.")
    print("Custom-domain preflight: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
