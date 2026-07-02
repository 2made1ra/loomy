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

    def to_html(self) -> None:
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
