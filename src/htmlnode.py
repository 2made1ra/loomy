class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if not self.props:
            return ""

        props: list[str] = [""]

        for key, value in self.props.items():
            props.append(f'{key}="{value}"')

        return " ".join(props)

    def __repr__(self) -> str:
        return f"HTMLNode(\n{self.tag}\n{self.value}\n{self.children}\n{self.props}\n)"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode(\n{self.tag}\n{self.value}\n{self.props}\n)"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)
        self.children: list[HTMLNode] = children

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("all parent nodes must have a tag")
        if len(self.children) == 0:
            raise ValueError("parent node must contain at least one child")
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
