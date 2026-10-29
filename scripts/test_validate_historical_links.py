"""Validate Markdown link extraction with balanced parentheses in URL segments."""

from pathlib import Path
import unittest

import validate


class HistoricalMarkdownLinksTests(unittest.TestCase):
    def test_regular_markdown_image_with_title(self):
        body = '![Backup screenshot](images/backup.png "Backup")'
        self.assertIn("images/backup.png", validate.urls(body))
        self.assertEqual(validate.MARKDOWN_IMAGE_RE.search(body).group("url"), "images/backup.png")

    def test_markdown_image_with_parentheses_in_historical_slug(self):
        path = "/post/2010/01/16/(MVP)-Model-View-Presenter-Passive-View/images/diagram.jpg"
        body = f"![MVP diagram]({path})"
        self.assertEqual(validate.MARKDOWN_IMAGE_RE.search(body).group("url"), path)
        self.assertIn(path, validate.urls(body))

    def test_linked_thumbnail_with_parentheses_in_image_and_link(self):
        prefix = "/post/2010/01/16/(MVP)-Model-View-Presenter-Passive-View/images/"
        body = f"[![View hierarchy]({prefix}thumb.jpg)]({prefix}full.jpg)"
        all_urls = validate.urls(body)
        self.assertIn(prefix + "thumb.jpg", all_urls)
        self.assertIn(prefix + "full.jpg", all_urls)

    def test_plain_historical_post_link_with_parentheses(self):
        slug = "/post/2010/01/16/(MVP)-Model-View-Presenter-Passive-View"
        self.assertIn(slug, validate.urls(f"[Read post]({slug})"))

    def test_known_root_relative_image_points_to_actual_source_file(self):
        root = Path("post/2010/01/16/(MVP)-Model-View-Presenter-Passive-View/index.md")
        link = "/post/2010/01/16/(MVP)-Model-View-Presenter-Passive-View/images/mvp-pattern-diagram-1.jpg"
        self.assertEqual(
            validate.local_path_for_url(root, link),
            (validate.ROOT / link.lstrip("/")).resolve()
        )


    def test_body_h1_is_detected_without_flagging_second_level_headings(self):
        self.assertEqual(validate.content_h1_count("# Duplicate title\n## Section\n"), 1)

    def test_h1_in_fenced_code_does_not_count(self):
        body = "```markdown\n# Example heading in code\n```\n## Actual section\n"
        self.assertEqual(validate.content_h1_count(body), 0)

    def test_html_h1_in_article_body_is_detected(self):
        self.assertEqual(validate.content_h1_count("<h1>Extra heading</h1>"), 1)



if __name__ == "__main__":
    unittest.main()
