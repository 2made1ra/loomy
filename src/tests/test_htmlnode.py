import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("p", [])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_no_tag(self):
        child_node = LeafNode("p", "some test")
        parent_node = ParentNode("", [child_node])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(), '<div class="container"><span>child</span></div>'
        )

    def test_to_html_children_error(self):
        child_node = LeafNode("b", "")
        parent_node = ParentNode("div", [child_node])
        self.assertRaises(ValueError, parent_node.to_html)


if __name__ == "__main__":
    unittest.main()
