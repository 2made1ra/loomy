import unittest

from htmlnode import HTMLNode, LeafNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "hello")
        assert node.props_to_html() == ""

    def test_props_to_html(self):
        node = HTMLNode("p", "some link", props={"href": "localhost"})
        assert node.props_to_html() == ' href="localhost"'

    def test_repr(self):
        node = HTMLNode()
        self.assertHasAttr(node, "tag")
        self.assertHasAttr(node, "children")

    def test_to_html(self):
        node = HTMLNode("p", "some_text")
        self.assertRaises(NotImplementedError, node.to_html)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "link", {"href": "https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">link</a>')

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "soprano")
        self.assertEqual(node.to_html(), "<i>soprano</i>")
