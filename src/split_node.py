from src.textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        raw_parts = node.text.split(delimiter)
        if len(raw_parts) % 2 == 0:
            raise Exception(
                f"Can not find matching closing delimeter - {delimiter} - invalid markdown syntax"
            )

        processed_parts: list[TextNode] = []

        for i in range(len(raw_parts)):
            if not raw_parts[i]:
                continue
            if i % 2 == 0:
                processed_parts.append(TextNode(raw_parts[i], TextType.TEXT))
                continue
            processed_parts.append(TextNode(raw_parts[i], text_type))

        new_nodes.extend(processed_parts)

    return new_nodes
