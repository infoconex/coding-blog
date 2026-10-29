"""Regression tests for image alt text and deployed image link validation."""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from validate_images import audit_site, main, page_url


class ImageValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def page(self, relative, body, canonical):
        file = self.root / relative
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(
            '<!doctype html><html><head>'
            f'<link rel="canonical" href="{canonical}">'
            '</head><body>' + body + '</body></html>',
            encoding="utf-8",
        )
        return file

    def image(self, relative):
        file = self.root / relative
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(b"test-image")

    def test_root_relative_image_and_full_size_link_pass(self):
        prefix = "post/2013/10/05/Strategy-and-Factory"
        canonical = "https://coding.infoconex.com/" + prefix
        self.image(prefix + "/images/thumb.jpg")
        self.image(prefix + "/images/full.jpg")
        self.page(
            prefix + ".html",
            f'<a href="/{prefix}/images/full.jpg">'
            f'<img src="/{prefix}/images/thumb.jpg" alt="Strategy pattern diagram"></a>',
            canonical,
        )
        count, errors = audit_site(self.root)
        self.assertEqual(count, 1)
        self.assertEqual(errors, [])

    def test_extensionless_article_resolves_relative_images_in_parent_directory(self):
        prefix = "post/2009/11/26/My-Post"
        self.image(prefix + "/images/diagram.png")
        self.page(
            prefix + ".html",
            '<a href="images/full.jpg"><img src="images/diagram.png" '
            'alt="Diagram of attachment process"></a>',
            "https://coding.infoconex.com/" + prefix,
        )
        count, errors = audit_site(self.root)
        self.assertEqual(count, 1)
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("broken image src" in issue and "/post/2009/11/26/images/" in issue for issue in errors))
        self.assertTrue(any("broken clickable image href" in issue for issue in errors))

    def test_rejects_missing_blank_and_generic_alt(self):
        self.image("assets/a.png")
        self.page(
            "index.html",
            '<img src="/assets/a.png">'
            '<img src="/assets/a.png" alt="">'
            '<img src="/assets/a.png" alt="image">',
            "https://coding.infoconex.com/",
        )
        count, errors = audit_site(self.root)
        self.assertEqual(count, 3)
        self.assertEqual(len(errors), 3)
        self.assertIn("missing an alt", errors[0])
        self.assertIn("empty alt", errors[1])
        self.assertIn("non-descriptive", errors[2])

    def test_explicitly_decorative_image_may_have_empty_alt(self):
        self.image("assets/decorative.svg")
        self.page(
            "index.html",
            '<img src="/assets/decorative.svg" alt="" role="presentation">',
            "https://coding.infoconex.com/",
        )
        self.assertEqual(audit_site(self.root), (1, []))

    def test_validates_srcset_and_ignores_external_asset_files(self):
        self.image("assets/a.png")
        self.page(
            "index.html",
            '<img alt="Website screenshot" src="https://external.example/screenshot.png" '
            'srcset="/assets/a.png 1x, /assets/missing.png 2x">',
            "https://coding.infoconex.com/",
        )
        count, errors = audit_site(self.root)
        self.assertEqual(count, 1)
        self.assertEqual(len(errors), 1)
        self.assertIn("broken image srcset", errors[0])

    def test_no_html_files_is_error(self):
        self.assertEqual(audit_site(self.root)[0], 0)
        self.assertEqual(len(audit_site(self.root)[1]), 1)


if __name__ == "__main__":
    unittest.main()
