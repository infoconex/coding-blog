#!/usr/bin/env python3
"""Generate deterministic Open Graph cards for the Coding blog.

This is intentionally separate from the GitHub Pages deployment. The companion
workflow writes generated PNGs back to assets/og/, while native branch-based
GitHub Pages remains the publisher. A generator failure therefore never blocks
an article from being published.
"""

from __future__ import annotations

import textwrap
from datetime import date, datetime
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "post"
OUTPUT = ROOT / "assets" / "og"
CONFIG = ROOT / "_config.yml"
SIZE = (1200, 630)

PALETTES = {
    "neo-industrial": {
        "bg": "#0d1117",
        "surface": "#111923",
        "text": "#e6edf3",
        "muted": "#8fa3b8",
        "accent": "#38bdf8",
    },
    "midnight-editorial": {
        "bg": "#0b0b0f",
        "surface": "#151219",
        "text": "#f4efe8",
        "muted": "#a79ca9",
        "accent": "#e879f9",
    },
    "warm-analog": {
        "bg": "#201a16",
        "surface": "#2a211b",
        "text": "#f0e5d6",
        "muted": "#b8a58f",
        "accent": "#d68a55",
    },
    "technical-brutalism": {
        "bg": "#f7f5ef",
        "surface": "#ffffff",
        "text": "#111111",
        "muted": "#555555",
        "accent": "#ff5a1f",
    },
}

FONT_REGULAR = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
FONT_BOLD = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
FONT_MONO = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf")


def font(path: Path, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype(str(path), size=size)
    except OSError:
        return ImageFont.load_default()


def read_front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def as_date(value) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.fromisoformat(str(value)).date()


def wrap_title(draw: ImageDraw.ImageDraw, title: str, title_font, max_width: int, max_lines: int = 4) -> list[str]:
    words = title.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        width = draw.textbbox((0, 0), candidate, font=title_font)[2]
        if width <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
            if len(lines) == max_lines - 1:
                break
    if current and len(lines) < max_lines:
        remaining_index = sum(len(line.split()) for line in lines)
        remaining = " ".join(words[remaining_index:])
        candidate = remaining
        while draw.textbbox((0, 0), candidate, font=title_font)[2] > max_width and len(candidate) > 1:
            candidate = candidate[:-2].rstrip() + "…"
        lines.append(candidate)
    return lines[:max_lines]


def render_card(*, title: str, published: date, topic: str, theme: str, output: Path) -> None:
    palette = PALETTES.get(theme, PALETTES["neo-industrial"])
    image = Image.new("RGB", SIZE, palette["bg"])
    draw = ImageDraw.Draw(image)

    # Signature editorial/instrumentation frame.
    draw.rectangle((52, 52, 1148, 578), outline=palette["surface"], width=3)
    draw.rectangle((52, 52, 66, 578), fill=palette["accent"])
    for x in range(92, 1149, 84):
        draw.line((x, 552, x + 34, 552), fill=palette["surface"], width=2)

    brand_font = font(FONT_MONO, 30)
    meta_font = font(FONT_MONO, 23)
    title_font = font(FONT_BOLD, 62 if len(title) < 72 else 54)
    footer_font = font(FONT_REGULAR, 22)

    draw.text((102, 92), "CODING.", fill=palette["accent"], font=brand_font)
    meta = f"{published.strftime('%b %d %Y').upper()}  ·  {topic.upper() if topic else 'ENGINEERING'}"
    draw.text((102, 148), meta, fill=palette["muted"], font=meta_font)

    y = 210
    lines = wrap_title(draw, title, title_font, max_width=930)
    for line in lines:
        draw.text((102, y), line, fill=palette["text"], font=title_font)
        bbox = draw.textbbox((102, y), line, font=title_font)
        y = bbox[3] + 10

    draw.text((102, 514), "Software engineering, architecture & systems", fill=palette["muted"], font=footer_font)
    image.save(output, format="PNG", optimize=True)


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8")) or {}
    default_theme = config.get("default_theme", "neo-industrial")

    # Stable site-wide fallback.
    render_card(
        title=config.get("subtitle", "Software engineering, architecture, systems, and lessons learned the hard way."),
        published=date(2008, 1, 1),
        topic="Engineering notes",
        theme=default_theme,
        output=OUTPUT / "default.png",
    )

    count = 0
    for path in sorted(POSTS.glob("*/*/*/*/index.md")):
        data = read_front_matter(path)
        if not data or data.get("published") is False:
            continue
        title = str(data.get("title", "Untitled"))
        slug = str(data.get("slug") or path.parent.name)
        published = as_date(data.get("date"))
        tags = data.get("tags") or []
        topic = str(tags[0]) if tags else "Engineering"
        theme = str(data.get("socialTheme") or default_theme)
        filename = f"{published.isoformat()}-{slug}.png"
        render_card(title=title, published=published, topic=topic, theme=theme, output=OUTPUT / filename)
        count += 1

    print(f"Generated {count} article social cards plus fallback in {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
