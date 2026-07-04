import re
from collections.abc import Callable

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


def extract_markdown_images(raw_md_text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)]\(([^\(\)]*)\)", raw_md_text)


def extract_markdown_links(raw_md_text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)]\(([^\(\)]*)\)", raw_md_text)


def _split_nodes_by_pattern(
    old_nodes: list[TextNode],
    extractor: Callable[[str], list[tuple[str, str]]],
    pattern_matcher: Callable[[str, str], str],
    type: TextType,
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        entities = extractor(text)
        if not entities:
            new_nodes.append(node)
            continue

        for label, url in entities:
            before, remaining_text = text.split(pattern_matcher(label, url), 1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(label, type, url))
            text = remaining_text

        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_by_pattern(
        old_nodes, extract_markdown_images, lambda x, y: f"![{x}]({y})", TextType.IMAGE
    )


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_by_pattern(
        old_nodes, extract_markdown_links, lambda x, y: f"[{x}]({y})", TextType.LINK
    )


def text_to_textnodes(raw_text: str) -> list[TextNode]:
    node = TextNode(raw_text, TextType.TEXT)
    text_nodes: list[TextNode] = [node]
    delimiters = {"**": TextType.BOLD, "_": TextType.ITALIC, "`": TextType.CODE}

    for key, value in delimiters.items():
        text_nodes = split_nodes_delimiter(text_nodes, key, value)

    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)

    return text_nodes
