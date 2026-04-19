class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        if tag is None:
            self.tag = None
        else:
            self.tag = tag
        self.value = value
        self.children = children
        if props is None:
            self.props = {}
        else:
            self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        string = ""
        if self.props is not None:
            for i in self.props:
                string += f' {i}="{self.props[i]}"'
        return string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return f"{self.value}"
        if self.props is None:
            return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError
        if self.children is None:
            raise ValueError("different message")
        text = ""
        if self.children is not None:
            for i in self.children:
                text += i.to_html()
        return f"<{self.tag}>{text}</{self.tag}>"
