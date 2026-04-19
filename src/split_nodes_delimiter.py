from textnode import TextNode, TextType


def split_nodes_delimeter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type.value != "text":
            new_nodes.append(node)
        else:
            new_node = []
            text = node.text
            texts = text.split(delimiter)
            if len(texts) % 2 == 0:
                raise Exception("invalid Markdown sythax")
            for i in range(0, len(texts)):
                if texts[i] == " ":
                    pass
                else:
                    if i % 2 == 0:
                        new_node.append(TextNode(f"{texts[i]}", TextType.TEXT))
                    if i % 2 == 1:
                        new_node.append(TextNode(f"{texts[i]}", text_type))
            new_nodes.extend(new_node)
    return new_nodes
