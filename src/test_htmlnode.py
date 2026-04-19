import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_html(self):
        node = HTMLNode(1, 1, 1, {"h": 1.0, "j": 22})
        self.assertEqual(node.props_to_html(), ' h="1.0" j="22"')

    def test_html1(self):
        node = HTMLNode(1, 1, 1, {"h": 5.0, "j": 22})
        self.assertEqual(node.props_to_html(), ' h="5.0" j="22"')

    def test_html2(self):
        node = HTMLNode(1, 1, 1, {"h": 1.0, "j": 21})
        self.assertEqual(node.props_to_html(), ' h="1.0" j="21"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<p href="https://www.google.com">Hello, world!</p>'
        )

    def test_leaf_to_html_p1(self):
        node = LeafNode(
            "p",
            "Hello, world!",
        )
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

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

    def test_to_html_with_grandchildren1(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node1 = LeafNode("p", "I dont like it")
        child_node = ParentNode("a", [grandchild_node])
        parent_node = ParentNode("div", [child_node, child_node1])
        self.assertEqual(
            parent_node.to_html(),
            "<div><a><b>grandchild</b></a><p>I dont like it</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
