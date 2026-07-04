import unittest

from src.md_to_html import markdown_to_html_node


class TestMDtoHtmlNode(unittest.TestCase):
    # --- Базовые случаи ---

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
# This is a **bolded** heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a <b>bolded</b> heading</h1></div>",
        )

    def test_heading_levels(self):
        md = """
### Level three heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Level three heading</h3></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> with _italic_ text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <i>italic</i> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- This is a list
- with **bold** items
- and _italic_ items
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with <b>bold</b> items</li><li>and <i>italic</i> items</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item with `code`
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <code>code</code></li><li>Third item</li></ol></div>",
        )

    def test_multiple_blocks_mixed(self):
        md = """
# Heading

This is a paragraph with **bold** text

- list item one
- list item two

> a quote block
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><p>This is a paragraph with <b>bold</b> text</p><ul><li>list item one</li><li>list item two</li></ul><blockquote>a quote block</blockquote></div>",
        )

    def test_codeblock_no_inline_parsing(self):
        md = """
```
1. not a list
- not a list either
# not a heading
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>1. not a list\n- not a list either\n# not a heading\n</code></pre></div>",
        )

    # --- Граничные случаи ---

    def test_empty_markdown(self):
        # Пустой markdown — невалидный вход: markdown_to_html_node
        # вернёт ParentNode("div", []) без ошибки, а вот вызов
        # to_html() на нём уже упадёт, так как у div нет детей
        md = ""
        node = markdown_to_html_node(md)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_only_whitespace(self):
        # Markdown из одних пробелов/переносов строк после strip()
        # даёт пустой список блоков — та же ситуация, что и выше
        md = "   \n\n   \n"
        node = markdown_to_html_node(md)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_single_word_paragraph(self):
        md = "word"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>word</p></div>")

    def test_single_item_unordered_list(self):
        md = "- only one item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>only one item</li></ul></div>")

    def test_single_item_ordered_list(self):
        md = "1. only one item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>only one item</li></ol></div>")

    def test_heading_level_six(self):
        md = "###### smallest heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h6>smallest heading</h6></div>")

    def test_seven_hashes_is_paragraph(self):
        # 7 решёток вне диапазона {1,6} — это не заголовок, а обычный параграф
        md = "####### not a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>####### not a heading</p></div>")

    def test_empty_codeblock(self):
        md = """
```
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><pre><code></code></pre></div>")

    def test_multiple_blank_lines_between_blocks(self):
        # Больше одного пустого разделителя между блоками не должно
        # создавать лишние пустые блоки
        md = """
First paragraph


Second paragraph
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>First paragraph</p><p>Second paragraph</p></div>",
        )

    def test_paragraph_with_no_inline_markup(self):
        md = "just plain text with no markup at all"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>just plain text with no markup at all</p></div>",
        )

    def test_quote_single_line(self):
        md = "> single line quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>single line quote</blockquote></div>")

    def test_leading_and_trailing_whitespace_in_block(self):
        # Ведущие/замыкающие переносы строк вокруг блока не должны
        # влиять на результат
        md = "\n\n   paragraph with surrounding whitespace   \n\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>paragraph with surrounding whitespace</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
