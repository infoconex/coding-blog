"""Sitemap/robots checks run on tiny generated-site fixtures, not production URLs."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from xml.sax.saxutils import escape

from validate_indexability import audit_site, robots_directives

SITE = "https://coding.infoconex.com/"
ARTICLE = SITE + "post/2009/01/14/C-Traceroute-using-net-framework"
ABOUT = SITE + "about/"


class CrawlabilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write_html("index.html", SITE)
        self.write_html("about/index.html", ABOUT)
        self.write_html("post/2009/01/14/C-Traceroute-using-net-framework.html", ARTICLE)
        self.write_html("404.html", SITE + "404.html")
        self.write_html("author/jscott/index.html", ABOUT,
                        extra='<meta name="robots" content="noindex, follow">'
                              '<meta http-equiv="refresh" content="0; url=/about/">')
        self.write_sitemap([SITE, ABOUT, ARTICLE])
        self.write_robots()

    def write_html(self, name: str, canonical: str, extra: str = "") -> None:
        file = self.root / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text('<!doctype html><html><head>'
                        f'<link rel="canonical" href="{canonical}">{extra}'
                        '</head><body></body></html>', encoding="utf-8")

    def write_sitemap(self, urls: list[str]) -> None:
        entries = "".join(f"<url><loc>{escape(url)}</loc></url>" for url in urls)
        (self.root / "sitemap.xml").write_text(
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            + entries + '</urlset>', encoding="utf-8")

    def write_robots(self, content: str = "") -> None:
        (self.root / "robots.txt").write_text(
            content or "User-agent: *\nAllow: /\n\nSitemap: " + SITE + "sitemap.xml\n",
            encoding="utf-8")

    def errors(self) -> list[str]:
        return [f.display() for f in audit_site(self.root)[2] if f.severity == "ERROR"]

    def test_valid_sitemap_matches_all_indexable_canons_and_skips_404_redirect(self):
        self.assertEqual(audit_site(self.root), (3, 3, []))

    def test_missing_article_from_sitemap_blocks(self):
        self.write_sitemap([SITE, ABOUT])
        self.assertTrue(any("CRAWL023" in x and ARTICLE in x for x in self.errors()))

    def test_redirect_in_sitemap_is_not_indexable_page(self):
        self.write_sitemap([SITE, ABOUT, ARTICLE, SITE + "author/jscott/"])
        self.assertTrue(any("CRAWL024" in x for x in self.errors()))

    def test_404_in_sitemap_is_rejected(self):
        self.write_sitemap([SITE, ABOUT, ARTICLE, SITE + "404.html"])
        self.assertTrue(any("CRAWL024" in x for x in self.errors()))

    def test_duplicate_url_is_rejected(self):
        self.write_sitemap([SITE, SITE, ABOUT, ARTICLE])
        self.assertTrue(any("CRAWL003" in x for x in self.errors()))

    def test_wrong_host_and_non_https_is_rejected(self):
        self.write_sitemap([SITE, ABOUT, ARTICLE, "http://example.com/bad"])
        self.assertTrue(any("CRAWL004" in x for x in self.errors()))

    def test_wrong_robots_sitemap_is_rejected(self):
        self.write_robots("User-agent: *\nAllow: /\nSitemap: https://example.com/sitemap.xml\n")
        self.assertTrue(any("CRAWL013" in x for x in self.errors()))

    def test_wildcard_robots_blocks_entire_site(self):
        self.write_robots("User-agent: *\nDisallow: /\nSitemap: " + SITE + "sitemap.xml")
        self.assertTrue(any("CRAWL011" in x for x in self.errors()))

    def test_disallow_for_named_bot_does_not_block_everyone(self):
        self.write_robots("User-agent: ExampleBot\nDisallow: /\n\nUser-agent: *\nAllow: /\n"
                          "Sitemap: " + SITE + "sitemap.xml")
        self.assertEqual(self.errors(), [])

    def test_missing_robots_is_only_advisory(self):
        (self.root / "robots.txt").unlink()
        counts = audit_site(self.root)
        self.assertEqual(counts[:2], (3, 3))
        self.assertFalse(any(f.severity == "ERROR" for f in counts[2]))
        self.assertTrue(any(f.code == "CRAWL010" and f.severity == "WARNING" for f in counts[2]))

    def test_missing_sitemap_blocks(self):
        (self.root / "sitemap.xml").unlink()
        self.assertTrue(any("CRAWL001" in x for x in self.errors()))

    def test_malformed_sitemap_xml_blocks(self):
        (self.root / "sitemap.xml").write_text("<urlset><url>", encoding="utf-8")
        self.assertTrue(any("CRAWL002" in x for x in self.errors()))

    def test_new_indexable_collection_requires_sitemap_entry(self):
        self.write_html("series/new-series/index.html", SITE + "series/new-series/")
        self.assertTrue(any("CRAWL023" in x and "new-series" in x for x in self.errors()))

    def test_missing_canonical_cannot_escape_sitemap_validation(self):
        (self.root / "index.html").write_text("<!doctype html><html></html>", encoding="utf-8")
        self.assertTrue(any("CRAWL021" in x for x in self.errors()))

    def test_robots_parser_accepts_multiple_agent_lines_and_ignores_comments(self):
        directives, blocked = robots_directives(
            "User-agent: Googlebot\nUser-agent: *\nDisallow: / # comment\n"
            "Sitemap: " + SITE + "sitemap.xml")
        self.assertTrue(blocked)
        self.assertEqual(directives, [SITE + "sitemap.xml"])


if __name__ == "__main__":
    unittest.main()
