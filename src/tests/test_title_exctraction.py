import unittest

from src.block_type import markdown_to_blocks

# Замените на актуальный путь импорта в вашем проекте
from src.utils import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_title_with_extra_paragraphs(self):
        markdown = """# My Title

Some paragraph text here.

## Subheading
"""
        self.assertEqual(extract_title(markdown), "My Title")

    def test_title_with_trailing_whitespace_in_block(self):
        # Блок целиком стрипается, но внутренние пробелы после "# " остаются
        markdown = "#   Spaced Title   "
        self.assertEqual(extract_title(markdown), "  Spaced Title")

    def test_no_h1_raises_exception(self):
        markdown = """## Not an H1

Just some text.
"""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_h2_only_raises_exception(self):
        # "### ..." матчится под BlockType.HEADING regex-ом,
        # но не проходит проверку startswith("# ")
        markdown = "### Heading level 3"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_h1_not_first_block_raises_exception(self):
        markdown = """Some intro paragraph.

# Title After Paragraph
"""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_paragraph_only_raises_exception(self):
        markdown = "Just a regular paragraph, no heading at all."
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_multiple_h1_returns_first_only(self):
        markdown = """# First Title

Some text.

# Second Title
"""
        self.assertEqual(extract_title(markdown), "First Title")

    def test_h1_with_inline_formatting(self):
        markdown = "# Title with **bold** and _italic_"
        self.assertEqual(extract_title(markdown), "Title with **bold** and _italic_")

    def test_empty_markdown_raises_exception(self):
        # markdown_to_blocks("") -> [] (пустой список после filter)
        # extract_title обращается к [0] -> IndexError (тоже Exception)
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_whitespace_only_markdown_raises_exception(self):
        markdown = "   \n\n   "
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_quote_block_as_first_raises_exception(self):
        markdown = """> This is a quote

# Title
"""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_list_block_as_first_raises_exception(self):
        markdown = """- item one
- item two

# Title
"""
        with self.assertRaises(Exception):
            extract_title(markdown)


class TestMarkdownToBlocksHelper(unittest.TestCase):
    """Доп. тесты на вспомогательную функцию, чтобы зафиксировать её контракт,
    от которого зависит extract_title."""

    def test_strips_each_block(self):
        markdown = "  # Title  \n\n  Some text  "
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["# Title", "Some text"])

    def test_filters_empty_blocks(self):
        markdown = "# Title\n\n\n\nSome text"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["# Title", "Some text"])


if __name__ == "__main__":
    unittest.main()
