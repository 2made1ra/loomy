import unittest

from src.textnode import TextNode, TextType
from src.utils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
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
