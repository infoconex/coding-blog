#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "post"
TAG_LINE = re.compile(r'^(?P<indent>\s*)tags:\s*(?P<value>\[.*\])\s*$', re.M)

# Canonical spellings/casing for technology names and recurring blog topics.
SPECIAL = {
    "ai": "AI",
    "ai flywheel": "AI Flywheel",
    "agentic ai": "Agentic AI",
    "api": "API",
    "asp.net": "ASP.NET",
    "aspnet": "ASP.NET",
    "asp.net mvc": "ASP.NET MVC",
    "aspnet mvc": "ASP.NET MVC",
    "azure": "Azure",
    "windows azure": "Windows Azure",
    "blueonyx": "BlueOnyx",
    "bluequartz": "BlueQuartz",
    "c#": "C#",
    "chatgpt": "ChatGPT",
    "cli": "CLI",
    "covid": "COVID",
    "dns": "DNS",
    "dotnet": ".NET",
    ".net": ".NET",
    ".net core": ".NET Core",
    ".net framework": ".NET Framework",
    "ebay": "eBay",
    "github": "GitHub",
    "github pages": "GitHub Pages",
    "html": "HTML",
    "http": "HTTP",
    "https": "HTTPS",
    "hyper-v": "Hyper-V",
    "imap": "IMAP",
    "javascript": "JavaScript",
    "jquery": "jQuery",
    "linq": "LINQ",
    "linqpad": "LINQPad",
    "linux": "Linux",
    "lvm": "LVM",
    "mvc": "MVC",
    "mvvm": "MVVM",
    "openai": "OpenAI",
    "openwebmail": "OpenWebmail",
    "playon": "PlayOn",
    "pop3": "POP3",
    "powershell": "PowerShell",
    "python": "Python",
    "roundcube": "Roundcube",
    "sharepoint": "SharePoint",
    "silverlight": "Silverlight",
    "smtp": "SMTP",
    "sql": "SQL",
    "sql server": "SQL Server",
    "ssl": "SSL",
    "tls": "TLS",
    "vb.net": "VB.NET",
    "vbnet": "VB.NET",
    "visual studio": "Visual Studio",
    "visual studio code": "Visual Studio Code",
    "wcf": "WCF",
    "windows": "Windows",
    "windows phone": "Windows Phone",
    "wpf": "WPF",
    "xbox": "Xbox",
    "zune": "Zune",
    "solid": "SOLID",
    "solid principles": "SOLID Principles",
    "open closed principle": "Open-Closed Principle",
    "open-closed principle": "Open-Closed Principle",
    "single responsibility principle": "Single Responsibility Principle",
    "liskov substitution principle": "Liskov Substitution Principle",
    "interface segregation principle": "Interface Segregation Principle",
    "dependency inversion principle": "Dependency Inversion Principle",
    "design patterns": "Design Patterns",
    "software development": "Software Development",
    "software engineering": "Software Engineering",
    "human oversight": "Human Oversight",
}

TOKEN_SPECIAL = {
    "ai": "AI", "api": "API", "asp.net": "ASP.NET", "aspnet": "ASP.NET",
    "c#": "C#", "cli": "CLI", "dns": "DNS", "github": "GitHub",
    "html": "HTML", "http": "HTTP", "https": "HTTPS", "imap": "IMAP",
    "javascript": "JavaScript", "jquery": "jQuery", "linq": "LINQ",
    "linqpad": "LINQPad", "linux": "Linux", "lvm": "LVM", "mvc": "MVC",
    "mvvm": "MVVM", "openai": "OpenAI", "pop3": "POP3", "powershell": "PowerShell",
    "python": "Python", "smtp": "SMTP", "sql": "SQL", "ssl": "SSL", "tls": "TLS",
    "vb.net": "VB.NET", "vbnet": "VB.NET", "wcf": "WCF", "wpf": "WPF",
    "ebay": "eBay", "blueonyx": "BlueOnyx", "bluequartz": "BlueQuartz",
    "playon": "PlayOn", "sharepoint": "SharePoint", "silverlight": "Silverlight",
    "chatgpt": "ChatGPT", "openwebmail": "OpenWebmail", "hyper-v": "Hyper-V",
    "xbox": "Xbox", "zune": "Zune", "solid": "SOLID", ".net": ".NET",
}

SMALL_WORDS = {"a", "an", "and", "as", "at", "by", "for", "from", "in", "of", "on", "or", "the", "to", "with"}


def smart_title(tag: str) -> str:
    words = tag.split(" ")
    out: list[str] = []
    for i, word in enumerate(words):
        key = word.casefold()
        if key in TOKEN_SPECIAL:
            out.append(TOKEN_SPECIAL[key])
        elif i > 0 and key in SMALL_WORDS:
            out.append(key)
        elif word.isupper() and len(word) <= 6:
            out.append(word)
        else:
            out.append(word[:1].upper() + word[1:].lower())
    return " ".join(out)


def canonical_tag(tag: str) -> str:
    clean = re.sub(r"\s+", " ", tag.strip())
    key = clean.casefold()
    return SPECIAL.get(key, smart_title(clean))


def normalize_file(path: Path) -> tuple[bool, list[tuple[str, str]]]:
    text = path.read_text(encoding="utf-8")
    match = TAG_LINE.search(text)
    if not match:
        return False, []
    try:
        tags = ast.literal_eval(match.group("value"))
    except Exception:
        return False, []
    if not isinstance(tags, list):
        return False, []

    normalized: list[str] = []
    seen: set[str] = set()
    changes: list[tuple[str, str]] = []
    for tag in tags:
        if not isinstance(tag, str):
            continue
        canonical = canonical_tag(tag)
        if canonical != tag:
            changes.append((tag, canonical))
        key = canonical.casefold()
        if key not in seen:
            seen.add(key)
            normalized.append(canonical)

    if normalized == tags:
        return False, []

    replacement = f'{match.group("indent")}tags: {json.dumps(normalized, ensure_ascii=False)}'
    updated = text[:match.start()] + replacement + text[match.end():]
    path.write_text(updated, encoding="utf-8")
    return True, changes


def main() -> int:
    changed_files = 0
    changed_tags = 0
    for path in sorted(POSTS.glob("*/*/*/*/index.md")):
        changed, changes = normalize_file(path)
        if not changed:
            continue
        changed_files += 1
        changed_tags += len(changes)
        rel = path.relative_to(ROOT)
        summary = ", ".join(f"{old!r} -> {new!r}" for old, new in changes)
        print(f"{rel}: {summary or 'deduplicated tags'}")

    print(f"Normalized {changed_tags} tag values across {changed_files} articles.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
