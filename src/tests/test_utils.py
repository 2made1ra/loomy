import unittest
from statistics import correlation

from src.textnode import TextNode, TextType
from src.utils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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


class TestTextToNode(unittest.TestCase):
    def test_split_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        correct_answer = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        testing_answer = text_to_textnodes(text)
        self.assertEqual(testing_answer, correct_answer)

    def test_plain_text(self):
        text = "just plain text, nothing special"
        correct_answer = [TextNode("just plain text, nothing special", TextType.TEXT)]
        testing_answer = text_to_textnodes(text)
        self.assertEqual(testing_answer, correct_answer)

    def test_empty_string(self):
        text = ""
        correct_answer = []
        testing_answer = text_to_textnodes(text)
        self.assertEqual(testing_answer, correct_answer)

    def test_only_bold(self):
        text = "**bold only**"
        correct_answer = [TextNode("bold only", TextType.BOLD)]
        testing_answer = text_to_textnodes(text)
        self.assertEqual(testing_answer, correct_answer)

    def test_only_italic(self):
        text = "_italic only_"
        correct_answer = [TextNode("italic only", TextType.ITALIC)]
        testing_answer = text_to_textnodes(text)
        self.assertEqual(testing_answer, correct_answer)

    def test_only_code(self):
        text = "`code only`"
        correct_answer = [TextNode("code only", TextType.CODE)]
        testing_answer = text_to_textnodes(text)
        self.assertEqual(testing_answer, correct_answer)

    def test_only_image(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        correct_answer = [
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            )
        ]
        testing_answer = text_to_textnodes(text)
        self.assertEqual(testing_answer, correct_answer)

    def test_only_link(self):
        text = "[link](https://boot.dev)"
        correct_answer = [TextNode("link", TextType.LINK, "https://boot.dev")]
        testing_answer = text_to_textnodes(text)
        self.assertEqual(testing_answer, correct_answer)

    def test_multiple_bold(self):
        text = "**one** and **two**"
        correct_answer = [
            TextNode("one", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.BOLD),
        ]
        testing_answer = text_to_textnodes(text)
        self.assertEqual(testing_answer, correct_answer)

    def test_bold_and_italic_combo(self):
        text = "**bold** and _italic_ together"
        correct_answer = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" together", TextType.TEXT),
        ]
        testing_answer = text_to_textnodes(text)
        self.assertEqual(testing_answer, correct_answer)

    def test_multiple_images_and_links(self):
        text = "![one](https://a.com/1.png) and [link](https://boot.dev) and ![two](https://a.com/2.png)"
        correct_answer = [
            TextNode("one", TextType.IMAGE, "https://a.com/1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "https://a.com/2.png"),
        ]
        testing_answer = text_to_textnodes(text)
        self.assertEqual(testing_answer, correct_answer)

    def test_unmatched_delimiter_raises(self):
        text = "This is **unmatched bold"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_inlined_delimeters(self):
        text = "This is **__inlined__** text!"
        correct_answer = [
            TextNode("This is ", TextType.TEXT),
            TextNode("__inlined__", TextType.BOLD),
            TextNode(" text!", TextType.TEXT),
        ]
        testing_answer = text_to_textnodes(text)
        self.assertEqual(testing_answer, correct_answer)
