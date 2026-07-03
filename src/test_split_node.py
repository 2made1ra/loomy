import unittest

from src.split_node import split_nodes_delimiter
from src.textnode import TextNode, TextType


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
