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

    def test_wrong_article_canonical_is_reported_even_if_schema_is_missing(self):
        incorrect_url = "https://coding.infoconex.com/"
        bad_markup = article_markup(schema=False).replace(URL, incorrect_url)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "post/2010/01/04/ASPNET-MVC-Tutorials/index.html"
            path.parent.mkdir(parents=True)
            path.write_text(bad_markup, encoding="utf-8")
            _, count, errors = audit_site(root)
            self.assertEqual(count, 1)
            self.assertTrue(any("canonical path" in issue for issue in errors))
            self.assertTrue(any("BlogPosting" in issue for issue in errors))

    def test_valid_html_article_extension_maps_to_historical_canonical(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "post/2010/01/04/ASPNET-MVC-Tutorials.html"
            path.parent.mkdir(parents=True)
            path.write_text(article_markup(), encoding="utf-8")
            (root / "assets/og").mkdir(parents=True)
            (root / "assets/og/card.png").write_bytes(b"test-card")
            self.assertEqual(audit_site(root), (1, 1, []))

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



    def test_guest_author_name_is_valid_without_invented_profile_url(self):
        html = article_markup(author_url=False).replace(
            '"name": "Jim Scott"', '"name": "John Scott"'
        )
        self.assertEqual(inspect_html(html), [])

    def test_guest_author_still_requires_a_name(self):
        html = article_markup(author_url=False).replace(
            '"name": "Jim Scott"', '"name": ""'
        )
        self.assertTrue(any("author" in issue for issue in inspect_html(html)))

    def test_jim_scott_author_url_must_identify_his_profile(self):
        html = article_markup().replace(
            '"url": "https://coding.infoconex.com/about/"',
            '"url": "https://example.com/unrelated/"',
        )
        self.assertTrue(any("profile URL" in issue for issue in inspect_html(html)))

    def test_canonical_redirect_skips_social_tag_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            article = root / "post/2010/01/04/ASPNET-MVC-Tutorials.html"
            article.parent.mkdir(parents=True)
            article.write_text(article_markup(), encoding="utf-8")
            (root / "assets/og").mkdir(parents=True)
            (root / "assets/og/card.png").write_bytes(b"test-card")
            redirect = root / "author/jscott/index.html"
            redirect.parent.mkdir(parents=True)
            redirect.write_text(
                '<!doctype html><html><head>'
                '<title>Page moved</title>'
                '<link rel="canonical" href="https://coding.infoconex.com/about/">'
                '<meta name="robots" content="noindex, follow">'
                '<meta http-equiv="refresh" content="0; url=https://coding.infoconex.com/about/">'
                '</head><body></body></html>',
                encoding="utf-8",
            )
            self.assertEqual(audit_site(root), (1, 1, []))


    def test_homepage_missing_both_canonical_and_og_url_is_critical(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text("<!doctype html><html><head></head></html>")
            _, _, errors = audit_site(root)
            self.assertTrue(any("SEO001" in error and "index.html" in error for error in errors))

    def test_about_missing_canonical_is_critical(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            about = root / "about/index.html"
            about.parent.mkdir()
            about.write_text("<!doctype html><html><head></head></html>")
            _, _, errors = audit_site(root)
            self.assertTrue(any("SEO001" in error and "/about/" in error for error in errors))

    def test_collection_missing_canonical_is_critical(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            collection = root / "writing/index.html"
            collection.parent.mkdir()
            collection.write_text("<!doctype html><html><head></head></html>")
            _, _, errors = audit_site(root)
            self.assertTrue(any("SEO001" in error for error in errors))

    def test_wrong_homepage_canonical_is_critical(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text('<!doctype html><html><head>'
                '<link rel="canonical" href="https://coding.infoconex.com/other/">'
                '</head></html>')
            _, _, errors = audit_site(root)
            self.assertTrue(any("SEO004" in error for error in errors))

    def test_canonical_query_and_http_are_critical(self):
        html = article_markup().replace(URL, "http://coding.infoconex.com/post/2010/01/04/ASPNET-MVC-Tutorials?preview=1")
        issues = inspect_html(html, require_metadata=True)
        self.assertTrue(any("unexpected canonical" in issue for issue in issues))

    def test_duplicate_canonical_across_pages_is_critical(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for path in ("index.html", "writing/index.html"):
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('<!doctype html><html><head>'
                    '<link rel="canonical" href="https://coding.infoconex.com/">'
                    '</head></html>')
            _, _, errors = audit_site(root)
            self.assertTrue(any("SEO005" in issue for issue in errors))

    def test_malformed_json_ld_on_nonarticle_is_critical(self):
        html = '<!doctype html><html><head><link rel="canonical" href="https://coding.infoconex.com/">' \
            '<script type="application/ld+json">{oops</script></head></html>'
        self.assertTrue(any("invalid JSON-LD" in error for error in inspect_html(html)))

    def test_array_graph_and_additional_nodes_are_valid(self):
        data = {"@graph": [
            {"@type": "WebPage", "url": URL},
            {"@type": ["CreativeWork", "BlogPosting"],
             "headline": "Test", "description": "Description", "url": URL,
             "datePublished": "2010-01-04", "dateModified": "2010-01-04",
             "author": {"@type": "Person", "name": "John Scott"}}]}
        html = article_markup(schema=False, author_url=False)
        html = html.replace("</head>", '<script type="application/ld+json">' +
            json.dumps([{"@type":"WebSite"}, data]) + '</script></head>')
        self.assertEqual(inspect_html(html), [])

    def test_malformed_publication_date_is_critical(self):
        html = article_markup().replace("2010-01-04T00:00:00-08:00", "not-a-date")
        self.assertTrue(any("datePublished" in issue for issue in inspect_html(html)))

    def test_about_profile_identity_is_required(self):
        html = '<!doctype html><html><head><link rel="canonical" ' \
               'href="https://coding.infoconex.com/about/"></head></html>'
        self.assertTrue(any("ProfilePage" in issue for issue in inspect_html(html)))

    def test_valid_about_profile_and_wrong_person(self):
        url = "https://coding.infoconex.com/about/"
        profile = {"@type":"ProfilePage", "url":url, "mainEntity":{
            "@type":"Person", "name":"Jim Scott", "url":url,
            "image":"https://coding.infoconex.com/assets/images/about/jim-scott.webp",
            "jobTitle":"Vice President of Software Engineering",
            "description":"Software engineering leader",
            "sameAs":["https://github.com/infoconex"]}}
        html = '<!doctype html><html><head><link rel="canonical" href="' + url + '">' \
               '<script type="application/ld+json">' + json.dumps(profile) + '</script></head></html>'
        self.assertEqual(inspect_html(html), [])
        wrong = html.replace('"name": "Jim Scott"', '"name": "Other"')
        self.assertTrue(any("Person name" in issue for issue in inspect_html(wrong)))

    def test_missing_social_image_tag_is_advisory_not_critical(self):
        from validate_seo import audit_site_detailed
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            article = root / "post/2010/01/04/ASPNET-MVC-Tutorials.html"
            article.parent.mkdir(parents=True, exist_ok=True)
            html = article_markup().replace(
                '<meta property="og:image" content="https://coding.infoconex.com/assets/og/card.png">', '')
            html = html.replace(
                '<meta name="twitter:image" content="https://coding.infoconex.com/assets/og/card.png">', '')
            article.write_text(html)
            _, _, findings = audit_site_detailed(root)
            self.assertTrue(any(f.severity == "WARNING" and f.code == "SEO011" for f in findings))
            self.assertFalse(any(f.severity == "ERROR" for f in findings))

    def test_missing_local_blogposting_image_is_critical(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "post/2010/01/04/ASPNET-MVC-Tutorials.html"
            target.parent.mkdir(parents=True, exist_ok=True)
            html = article_markup()
            html = html.replace('"headline": "ASP.NET MVC Tutorials"',
                '"image": "https://coding.infoconex.com/assets/missing.png", "headline": "ASP.NET MVC Tutorials"')
            target.write_text(html)
            (root / "assets/og").mkdir(parents=True)
            (root / "assets/og/card.png").write_bytes(b"card")
            _, _, errors = audit_site(root)
            self.assertTrue(any("SEO041" in error for error in errors))

    def test_corrupt_html_encoding_is_critical(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_bytes(b"\xff\xfe")
            _, _, errors = audit_site(root)
            self.assertTrue(any("SEO900" in error for error in errors))

    def test_seo_scanner_exception_is_not_swallowed(self):
        from unittest.mock import patch
        from validate_seo import main
        with patch("validate_seo.audit_site_detailed", side_effect=RuntimeError("scanner crash")):
            with patch("sys.argv", ["validate_seo.py", "--site-dir", "_site"]):
                with self.assertRaisesRegex(RuntimeError, "scanner crash"):
                    main()

    def test_normal_page_with_stray_refresh_cannot_bypass_checks(self):
        html = '<!doctype html><html><head>' \
            '<meta http-equiv="refresh" content="0;url=/about/">' \
            '<meta property="og:url" content="https://coding.infoconex.com/">' \
            '</head></html>'
        self.assertTrue(any("missing canonical" in issue for issue in inspect_html(html)))

    def test_trailing_slash_does_not_change_historical_article_path(self):
        from validate_seo import intended_url
        self.assertEqual(intended_url("post/2010/01/04/ASPNET-MVC-Tutorials.html", True), URL)
        self.assertEqual(intended_url("post/2010/01/04/ASPNET-MVC-Tutorials/index.html", True), URL + "/")


if __name__ == "__main__":
    unittest.main()
