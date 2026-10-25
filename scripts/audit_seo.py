#!/usr/bin/env python3
"""Audit generated Jekyll HTML for SEO titles, descriptions, and canonicals.

Run after: bundle exec jekyll build
Usage: python scripts/audit_seo.py --site _site --report seo-audit.csv
Exit status: 1 for missing/duplicate title or description, or missing canonical;
length recommendations are reported but do not fail the build.
"""
from __future__ import annotations

import argparse
import csv
import html
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path


class HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.in_title = False
        self.titles: list[str] = []
        self.descriptions: list[str] = []
        self.canonicals: list[str] = []
        self._title_parts: list[str] = []
        self.robots: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "head":
            self.in_head = True
        if not self.in_head:
            return
        if tag == "title":
            self.in_title = True
            self._title_parts = []
        elif tag == "meta":
            name = (attrs_dict.get("name") or "").casefold()
            if name == "description":
                self.descriptions.append(attrs_dict.get("content") or "")
            elif name == "robots":
                self.robots.append(attrs_dict.get("content") or "")
        elif tag == "link" and (attrs_dict.get("rel") or "").casefold() == "canonical":
            self.canonicals.append(attrs_dict.get("href") or "")

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self._title_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self.in_title:
            self.titles.append("".join(self._title_parts).strip())
            self.in_title = False
        if tag == "head":
            self.in_head = False


def main() -> int:
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument("--site", type=Path, default=Path("_site"))
    argp.add_argument("--report", type=Path, default=Path("seo-audit.csv"))
    args = argp.parse_args()
    if not args.site.is_dir():
        argp.error(f"Generated site not found: {args.site}. Build Jekyll first.")
    rows = []
    for path in sorted(args.site.rglob("*.html")):
        page = HeadParser()
        page.feed(path.read_text(encoding="utf-8", errors="replace"))
        if any("noindex" in value.casefold() for value in page.robots):
            continue
        title = html.unescape(page.titles[0]) if page.titles else ""
        desc = html.unescape(page.descriptions[0]) if page.descriptions else ""
        canonical = page.canonicals[0] if page.canonicals else ""
        issues = []
        if len(page.titles) != 1 or not title:
            issues.append("title_missing_or_multiple")
        if len(page.descriptions) != 1 or not desc:
            issues.append("description_missing_or_multiple")
        if len(page.canonicals) != 1 or not canonical:
            issues.append("canonical_missing_or_multiple")
        if title and len(title) < 30:
            issues.append("title_short")
        if len(title) > 70:
            issues.append("title_long")
        if desc and len(desc) < 110:
            issues.append("description_short")
        if len(desc) > 170:
            issues.append("description_long")
        rows.append({"path": path.relative_to(args.site).as_posix(), "title": title,
                     "title_length": len(title), "description": desc,
                     "description_length": len(desc), "canonical": canonical,
                     "issues": issues})

    for field, code in (("title", "duplicate_title"), ("description", "duplicate_description"),
                        ("canonical", "duplicate_canonical")):
        groups = defaultdict(list)
        for row in rows:
            if row[field]:
                groups[row[field].casefold().strip()].append(row)
        for group in groups.values():
            if len(group) > 1:
                for row in group:
                    row["issues"].append(code)

    args.report.parent.mkdir(parents=True, exist_ok=True)
    with args.report.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=("path", "title", "title_length", "description",
                          "description_length", "canonical", "issues"))
        writer.writeheader()
        for row in rows:
            writer.writerow({**row, "issues": ";".join(row["issues"])})
    counts = defaultdict(int)
    for row in rows:
        for issue in row["issues"]:
            counts[issue] += 1
    print(f"Pages audited: {len(rows)} | Report: {args.report}")
    for issue, count in sorted(counts.items()):
        print(f"{issue}: {count}")
    fatal = {"title_missing_or_multiple", "description_missing_or_multiple",
             "canonical_missing_or_multiple", "duplicate_title",
             "duplicate_description", "duplicate_canonical"}
    return int(any(fatal.intersection(row["issues"]) for row in rows))


if __name__ == "__main__":
    raise SystemExit(main())
