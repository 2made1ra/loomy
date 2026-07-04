import unittest

from src.textnode import TextNode, TextType
from src.utils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


class TestSplitNode(unittest.TestCase):
    def test_split_asterisk(self):
        nodes = [
            TextNode("This is text with a *bold block* word.", TextType.TEXT),
            TextNode("This is plain text", TextType.TEXT),
        ]

        answers = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word.", TextType.TEXT),
            TextNode("This is plain text", TextType.TEXT),
        ]

        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.BOLD), answers)

    def test_split_under(self):
        nodes = [
            TextNode("This is text with a _italic block_ word.", TextType.TEXT),
            TextNode("This is plain text", TextType.TEXT),
        ]

        answers = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word.", TextType.TEXT),
            TextNode("This is plain text", TextType.TEXT),
        ]

        self.assertEqual(split_nodes_delimiter(nodes, "_", TextType.ITALIC), answers)

    def test_split_backtick(self):
        nodes = [
            TextNode("This is text with a `code block` word.", TextType.TEXT),
            TextNode("This is plain text", TextType.TEXT),
        ]

        answers = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word.", TextType.TEXT),
            TextNode("This is plain text", TextType.TEXT),
        ]

        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), answers)

    def test_split_combo(self):
        nodes = [
            TextNode("This is text with a *bold block* word.", TextType.TEXT),
            TextNode("This is plain text. ", TextType.TEXT),
            TextNode("And this is `code block` word.", TextType.TEXT),
        ]

        answers = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word.", TextType.TEXT),
            TextNode("This is plain text. ", TextType.TEXT),
            TextNode("And this is ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word.", TextType.TEXT),
        ]

        func_test_answers = split_nodes_delimiter(
            split_nodes_delimiter(nodes, "*", TextType.BOLD), "`", TextType.CODE
        )

        self.assertEqual(func_test_answers, answers)


class TestExtractMD(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_both(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [text](https://google.com)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


class TestSplitNodeLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("This is plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_only_image(self):
        node = TextNode("![alone](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("alone", TextType.IMAGE, "https://example.com/img.png")],
            new_nodes,
        )

    def test_split_images_starts_with_image(self):
        node = TextNode(
            "![start](https://example.com/a.png) trailing text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://example.com/a.png"),
                TextNode(" trailing text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_ignores_non_text_nodes(self):
        node = TextNode("already a link", TextType.LINK, "https://example.com")
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_ignores_images(self):
        node = TextNode(
            "Text with ![an image](https://a.com/img.png) and a [real link](https://a.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "Text with ![an image](https://a.com/img.png) and a ",
                    TextType.TEXT,
                ),
                TextNode("real link", TextType.LINK, "https://a.com"),
            ],
            new_nodes,
        )
