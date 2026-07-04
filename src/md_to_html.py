from src.block_type import BlockType, block_to_block_type, markdown_to_blocks
from src.htmlnode import HTMLNode, ParentNode
from src.textnode import TextNode, TextType, text_node_to_html_node
from src.utils import text_to_textnodes


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes: list[HTMLNode] = []

    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))

    return html_nodes


def paragraph_to_html(block: str) -> ParentNode:
    text = " ".join(block.split("\n"))
    children = text_to_children(text)
    return ParentNode("p", children)


def heading_to_html(block: str) -> ParentNode:
    level, text = block.split(" ", maxsplit=1)
    children = text_to_children(text)
    return ParentNode(f"h{len(level)}", children)


def quote_to_html(block: str) -> ParentNode:
    lines = block.split("\n")
    stripped_lines = []
    for line in lines:
        stripped_lines.append(line.removeprefix("> "))
    text = " ".join(stripped_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def or_list_to_html(block: str) -> ParentNode:
    lines = block.split("\n")
    strip_lines = []
    for line in lines:
        strip_lines.append(line.split(" ", 1)[1])
    children = []
    for line in strip_lines:
        children.append(ParentNode("li", text_to_children(line)))
    return ParentNode("ol", children)


def uor_list_to_html(block: str) -> ParentNode:
    lines = block.split("\n")
    strip_lines = []
    for line in lines:
        strip_lines.append(line.split(" ", 1)[1])
    children = []
    for line in strip_lines:
        children.append(ParentNode("li", text_to_children(line)))
    return ParentNode("ul", children)


def code_to_html(block: str) -> ParentNode:
    text_node = TextNode(block.removeprefix("```\n").removesuffix("```"), TextType.CODE)
    html_node_leaf = text_node_to_html_node(text_node)
    return ParentNode("pre", [html_node_leaf])


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children: list[HTMLNode] = []

    for block in blocks:
        type = block_to_block_type(block)
        match type:
            case BlockType.PARAGRAPH:
                children.append(paragraph_to_html(block))
            case BlockType.HEADING:
                children.append(heading_to_html(block))
            case BlockType.QUOTE:
                children.append(quote_to_html(block))
            case BlockType.ORDERED_LIST:
                children.append(or_list_to_html(block))
            case BlockType.UNORDERED_LIST:
                children.append(uor_list_to_html(block))
            case BlockType.CODE:
                children.append(code_to_html(block))

    return ParentNode("div", children)
