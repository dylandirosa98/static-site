import unittest

from block_type import BlockType, block_to_block_type
from extract_markdown import extract_markdown_images, extract_markdown_links
from extract_title import extract_title
from markdown_to_blocks import markdown_to_blocks
from markdown_to_html_node import markdown_to_html_node
from split_nodes import split_nodes_images, split_nodes_links
from split_nodes_delimiter import split_nodes_delimeter
from text_node_to_html_node import text_node_to_html_node
from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_extract_title(self):
        md = "# This is **bolded** paragraph\n text in a p tag here This is another paragraph with _italic_ text and code here"
        self.assertEqual(extract_title(md), "This is **bolded** paragraph")

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

    def test_block(self):
        block = "###### jkskjjjsdjdjdjd"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block1(self):
        block = "```\nthis is code and it is good code\n this is really good code \n yes it is \n iknow```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block2(self):
        block = ">\n>this is code and it is good code\n> this is really good code \n > yes it is \n> iknow"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block3(self):
        block = "1. \n2. this is code and it is good code\n3. this is really good code \n4. > yes it is \n5. > iknow"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block4(self):
        block = "-  \n- this is code and it is good code\n- this is really good code \n- > yes it is \n- > iknow"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block5(self):
        block = "###### heyyyyyyy \n- this is code and it is good code\n- this is really good code \n- > yes it is \n- > iknow"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.BOLD, "url.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text1(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is a text node"},
        )

    def test_delimiter(self):
        node = TextNode("This is a 'CODE HERE' text node", TextType.TEXT)

        self.assertEqual(
            split_nodes_delimeter([node], "'", TextType.CODE),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("CODE HERE", TextType.CODE),
                TextNode(" text node", TextType.TEXT),
            ],
        )

    def test_delimiter1(self):
        node = TextNode("This is a 'CODE HERE' text node", TextType.TEXT)
        node2 = TextNode("This is a **bold text ** yeahhhh **bold**", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimeter([node, node2], "**", TextType.BOLD),
            [
                TextNode("This is a 'CODE HERE' text node", TextType.TEXT),
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold text ", TextType.BOLD),
                TextNode(" yeahhhh ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("", TextType.TEXT),
            ],
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
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
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links1(self):
        node = TextNode(
            "[image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links2(self):
        node = TextNode(
            "[image](https://i.imgur.com/zjjcJKZ.png)[second image](https://i.imgur.com/3elNhQu.png) and another ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and another ", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_text = text_to_textnodes(text)
        self.assertListEqual(
            [
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
            ],
            new_text,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


if __name__ == "__main__":
    unittest.main()
