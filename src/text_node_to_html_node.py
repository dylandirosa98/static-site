from htmlnode import LeafNode


def text_node_to_html_node(node):
    if node.text_type.value == "text":
        return LeafNode(None, node.text)
    if node.text_type.value == "bold":
        return LeafNode("b", node.text)
    if node.text_type.value == "italic":
        return LeafNode("i", node.text)
    if node.text_type.value == "code":
        return LeafNode("code", node.text)

    if node.text_type.value == "link":
        return LeafNode("a", node.text, {"href": node.url})
    if node.text_type.value == "image":
        return LeafNode("img", "", {"src": node.url, "alt": node.text})
    else:
        raise Exception("wrong type")
