import unittest

from htmlnode import HTMLNode


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
