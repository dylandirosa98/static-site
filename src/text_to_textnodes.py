from split_nodes import split_nodes_images, split_nodes_links
from split_nodes_delimiter import split_nodes_delimeter
from textnode import TextNode, TextType


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_delimeter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimeter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimeter(nodes, "`", TextType.CODE)
    return nodes
