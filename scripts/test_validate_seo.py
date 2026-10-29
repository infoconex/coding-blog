"""Regression tests for generated HTML SEO and BlogPosting checks."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from validate_seo import audit_site, inspect_html


URL = "https://coding.infoconex.com/post/2010/01/04/ASPNET-MVC-Tutorials"


def article_markup(*, author_url: bool = True, extra: str = "", schema: bool = True) -> str:
    post = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": "ASP.NET MVC Tutorials",
        "description": "Notes about historical ASP.NET MVC 2.",
        "datePublished": "2010-01-04T00:00:00-08:00",
        "dateModified": "2010-01-04T00:00:00-08:00",
        "url": URL,
        "author": {
            "@type": "Person",
            "name": "Jim Scott",
        },
    }
    if author_url:
        post["author"]["url"] = "https://coding.infoconex.com/about/"
    structured_data = (
        '<script type="application/ld+json">' + json.dumps(post) + "</script>"
        if schema else ""
    )
    return (
        "<!doctype html><html><head>"
        f'<link rel="canonical" href="{URL}">'
        f'<meta property="og:url" content="{URL}">'
        '<meta property="og:image" content="https://coding.infoconex.com/assets/og/card.png">'
        '<meta name="twitter:image" content="https://coding.infoconex.com/assets/og/card.png">'
        '<meta name="twitter:card" content="summary_large_image">'
        + extra + structured_data + "</head><body></body></html>"
    )


class RenderedSeoTests(unittest.TestCase):
    def test_valid_article_has_unique_social_tags_and_schema(self):
        self.assertEqual(inspect_html(article_markup()), [])

    def test_duplicate_social_image_and_card_tags_fail(self):
        html = article_markup(extra=(
            '<meta property="og:image" content="https://example.com/another.png">'
            '<meta name="twitter:card" content="summary">'
        ))
        errors = inspect_html(html)
        self.assertTrue(any("og:image" in error for error in errors))
        self.assertTrue(any("twitter:card" in error for error in errors))

    def test_missing_author_profile_url_fails(self):
        issues = inspect_html(article_markup(author_url=False))
        self.assertTrue(any("author" in issue for issue in issues))

    def test_missing_blogposting_fails_for_article(self):
        issues = inspect_html(article_markup(schema=False))
        self.assertTrue(any("BlogPosting" in issue for issue in issues))

    def test_redirect_without_canonical_is_excluded(self):
        self.assertEqual(inspect_html('<html><head><meta http-equiv="refresh" '
                                      'content="0; url=/about/"></head></html>'), [])

    def test_extensionless_article_in_built_site_is_scanned(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "post/2010/01/04/ASPNET-MVC-Tutorials"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(article_markup(), encoding="utf-8")
            (root / "assets/og").mkdir(parents=True, exist_ok=True)
            (root / "assets/og/card.png").write_bytes(b"test-card")
            result = audit_site(root)
            self.assertEqual(result, (1, 1, []))


    def test_article_missing_both_canonical_and_og_url_is_not_skipped(self):
        missing_canonical = article_markup().replace(
            f'<link rel="canonical" href="{URL}">', ""
        ).replace(f'<meta property="og:url" content="{URL}">', "")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "post/2010/01/04/ASPNET-MVC-Tutorials/index.html"
            path.parent.mkdir(parents=True)
            path.write_text(missing_canonical, encoding="utf-8")
            checked, articles, errors = audit_site(root)
            self.assertEqual((checked, articles), (1, 1))
            self.assertTrue(any("missing canonical link" in error for error in errors))

    def test_missing_local_social_card_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "post/2010/01/04/ASPNET-MVC-Tutorials/index.html"
            path.parent.mkdir(parents=True)
            path.write_text(article_markup(), encoding="utf-8")
            checked, articles, errors = audit_site(root)
            self.assertEqual((checked, articles), (1, 1))
            self.assertTrue(any("og:image references missing local image" in error for error in errors))
            self.assertTrue(any("twitter:image references missing local image" in error for error in errors))

    def test_redirect_page_under_post_path_is_not_treated_as_article(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            article = root / "post/2010/01/04/ASPNET-MVC-Tutorials/index.html"
            article.parent.mkdir(parents=True)
            article.write_text(article_markup(), encoding="utf-8")
            (root / "assets/og").mkdir(parents=True)
            (root / "assets/og/card.png").write_bytes(b"test-card")
            redirected = root / "post/2010/01/05/legacy-redirect/index.html"
            redirected.parent.mkdir(parents=True)
            redirected.write_text(
                '<!doctype html><meta http-equiv="refresh" content="0; url=/about/">',
                encoding="utf-8",
            )
            self.assertEqual(audit_site(root), (1, 1, []))



if __name__ == "__main__":
    unittest.main()
