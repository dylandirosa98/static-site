from block_type import BlockType, block_to_block_type
from htmlnode import ParentNode
from markdown_to_blocks import markdown_to_blocks
from text_node_to_html_node import text_node_to_html_node
from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    new_blocks = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.CODE:
            text = block[4:-3]
            lines = text.split("\n")
            text = "\n".join([line.strip() for line in lines])
            html_node = text_node_to_html_node((TextNode(text, TextType.TEXT)))
            code_node = ParentNode("code", [html_node])
            pre_node = ParentNode("pre", [code_node])
            new_blocks.append(pre_node)
        if block_type == BlockType.HEADING:
            number_of = 0
            for i in range(6):
                if block[i] == "#":
                    number_of += 1
                else:
                    break
            children = text_to_children(block[(number_of + 1) :])
            node = ParentNode(f"h{number_of}", children)
            new_blocks.append(node)
        if block_type == BlockType.ORDERED_LIST:
            lines = block.splitlines()
            li_nodes = []
            for line in lines:
                j = 0
                for i in range(len(line)):
                    if line[i] == " ":
                        j = i
                        break
                children = text_to_children(line[j + 1 :])
                li_node = ParentNode("li", children)
                li_nodes.append(li_node)
            node = ParentNode("ol", li_nodes)
            new_blocks.append(node)
        if block_type == BlockType.PARAGRAPH:
            text = " ".join([line.strip() for line in block.splitlines()])
            children = text_to_children(text)
            node = ParentNode("p", children)
            new_blocks.append(node)
        if block_type == BlockType.QUOTE:
            lines = block.splitlines()
            text = ""
            for line in lines:
                text += line[2:]
            children = text_to_children(text)
            node = ParentNode("blockquote", children)
            new_blocks.append(node)
        if block_type == BlockType.UNORDERED_LIST:
            lines = block.splitlines()
            li_nodes = []
            for line in lines:
                children = text_to_children(line[2:])
                li_node = ParentNode("li", children)
                li_nodes.append(li_node)
            node = ParentNode("ul", li_nodes)
            new_blocks.append(node)
    parent_node = ParentNode("div", new_blocks)
    return parent_node


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    if len(children) == 0:
        return None
    return children
