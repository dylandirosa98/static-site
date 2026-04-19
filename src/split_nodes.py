from extract_markdown import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        new_node = []
        text = node.text
        images = extract_markdown_images(text)
        for j in range(len(images)):
            parts = text.split(f"![{images[j][0]}]({images[j][1]})", 1)
            if parts[0] != "":
                new_node.append(
                    TextNode(
                        parts[0],
                        TextType.TEXT,
                    )
                )
            new_node.append(TextNode(images[j][0], TextType.IMAGE, images[j][1]))
            text = parts[1]
        if text != "":
            new_node.append(TextNode(text, TextType.TEXT))
        new_nodes.extend(new_node)
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        new_node = []
        text = node.text
        links = extract_markdown_links(text)
        for j in range(len(links)):
            parts = text.split(f"[{links[j][0]}]({links[j][1]})", 1)
            if parts[0] != "":
                new_node.append(
                    TextNode(
                        parts[0],
                        TextType.TEXT,
                    )
                )

            new_node.append(TextNode(links[j][0], TextType.LINK, links[j][1]))
            text = parts[1]
        if text != "":
            new_node.append(TextNode(text, TextType.TEXT))
        new_nodes.extend(new_node)
    return new_nodes
