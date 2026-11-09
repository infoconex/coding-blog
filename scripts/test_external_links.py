"""Regression tests for Jekyll build-time external link handling."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from external_links import is_external_http_url, process_site, rewrite_html


class ExternalLinksTests(unittest.TestCase):
    def assert_rewrite(self, original: str, expected: str) -> None:
        rendered, _ = rewrite_html(original)
        self.assertEqual(rendered, expected)
        self.assertEqual(rewrite_html(rendered), (rendered, 0), "Rewriting must be idempotent")

    def test_normal_external_links_and_mixed_quotes(self):
        self.assert_rewrite(
            '<p><a class="reference" href="https://learn.microsoft.com/">Docs</a>'
            " <a href='http://github.com/infoconex'>Source</a></p>",
            '<p><a class="reference" href="https://learn.microsoft.com/" target="_blank" rel="noopener noreferrer">Docs</a>'
            ' <a href=\'http://github.com/infoconex\' target="_blank" rel="noopener noreferrer">Source</a></p>',
        )

    def test_internal_navigation_and_non_http_links_are_untouched(self):
        for href in (
            "/", "/archive/", "../index.html", "#section", "?topic=net", "mailto:someone@example.com",
            "javascript:void(0)", "https://coding.infoconex.com/post/2008/",
            "http://www.coding.infoconex.com/about/", "//coding.infoconex.com/search",
            "HTTPS://CODING.INFOCONEX.COM/post/", "https://coding.infoconex.com:443/about/",
        ):
            with self.subTest(href=href):
                anchor = f'<a href="{href}">Link</a>'
                self.assert_rewrite(anchor, anchor)

    def test_scheme_relative_external_is_transformed(self):
        self.assert_rewrite('<a href="//external.example.org/path">Outside</a>',
                            '<a href="//external.example.org/path" target="_blank" rel="noopener noreferrer">Outside</a>')

    def test_existing_rel_tokens_are_preserved(self):
        self.assert_rewrite('<a href="https://example.com" rel="nofollow sponsored">Visit</a>',
                            '<a href="https://example.com" rel="nofollow sponsored noopener noreferrer" target="_blank">Visit</a>')
        self.assert_rewrite('<a rel=\'ugc noopener\' href="https://example.com" target="_blank">Visit</a>',
                            '<a rel="ugc noopener noreferrer" href="https://example.com" target="_blank">Visit</a>')

    def test_editorconfig_already_secure_links_are_identical(self):
        anchor = '<a href="https://github.com/infoconex/RecordSift" target="_blank" rel="noopener noreferrer">RecordSift</a>'
        self.assert_rewrite(anchor, anchor)

    def test_deliberate_targets_and_downloads_are_not_overridden(self):
        for anchor in (
            '<a href="https://example.com" target="_self">Same tab</a>',
            '<a href="https://example.com" target="reference-panel">Named tab</a>',
            '<a href="https://example.com/file.pdf" download>Download</a>',
            '<a href="https://example.com/file.pdf" download="file.pdf">Download</a>',
        ):
            self.assert_rewrite(anchor, anchor)

    def test_external_image_links_are_covered_and_internal_images_are_not(self):
        self.assert_rewrite('<a href="https://images.example.com/full.png"><img src="/images/thumb.png" alt="Diagram"></a>',
                            '<a href="https://images.example.com/full.png" target="_blank" rel="noopener noreferrer"><img src="/images/thumb.png" alt="Diagram"></a>')
        self.assert_rewrite('<a href="/images/full.png"><img src="/images/thumb.png" alt="Diagram"></a>',
                            '<a href="/images/full.png"><img src="/images/thumb.png" alt="Diagram"></a>')

    def test_multiline_tags_quoted_greater_than_and_protected_content(self):
        doc = '''<!doctype html>
<html><head><script type="application/ld+json">{"text":"<a href=\\"https://ignored.example\\">"}</script></head>
<body><!-- <a href="https://comment.example"> -->
<pre>&lt;a href="https://code.example"&gt;</pre>
<a data-note="rel='bogus' > text" 
 href="https://example.org?first=1&amp;second=2" rel="nofollow">External</a>
</body></html>'''
        result, count = rewrite_html(doc)
        self.assertEqual(count, 1)
        self.assertIn('data-note="rel=\'bogus\' > text"', result)
        self.assertIn('rel="nofollow noopener noreferrer"', result)
        self.assertIn('target="_blank"', result)
        self.assertIn('<!-- <a href="https://comment.example"> -->', result)
        self.assertIn('"<a href=\\"https://ignored.example\\">"', result)
        self.assertEqual(rewrite_html(result), (result, 0))

    def test_not_rewrite_malformed_or_non_http_url(self):
        for href in ("https://", "ftp://example.com", "tel:+123", "data:text/plain,abc"):
            self.assertFalse(is_external_http_url(href))

    def test_archive_and_latest_artifact_policy_check(self):
        # Synthetic Jekyll output named after three real, established articles.
        samples = {
            "post/2008/08/23/BlueQuartz-installing-Mono": '<a href="https://www.mono-project.com/docs/web/mod_mono/">Mono</a>',
            "post/2010/10/11/ASPNET-CustomValidator-that-validates-multiple-controls-using-both-Server-Side-and-Client-Side-scripting/index.html": '<a href="https://learn.microsoft.com/">Docs</a>',
            "post/2026/11/09/editorconfig-dotnet-framework-4-8-verify-code-style/index.html": '<a href="https://github.com/infoconex/RecordSift" target="_blank" rel="noopener noreferrer">RecordSift</a>',
        }
        with TemporaryDirectory() as temp:
            root = Path(temp)
            for relative, html in samples.items():
                page = root / relative
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text(html, encoding="utf-8")
            _, changed, issues = process_site(root, check=True)
            self.assertEqual(changed, 2)
            self.assertEqual(len(issues), 2)
            _, changed, issues = process_site(root)
            self.assertEqual((changed, issues), (2, []))
            _, changed, issues = process_site(root, check=True)
            self.assertEqual((changed, issues), (0, []))
            self.assertEqual((root / list(samples)[2]).read_text(encoding="utf-8"), samples[list(samples)[2]])


if __name__ == "__main__":
    unittest.main()
