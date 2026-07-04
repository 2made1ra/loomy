import unittest

from src.block_type import BlockType, block_to_block_type


class TestBlockType(unittest.TestCase):
    def test_heading(self):
        text = "##### Heading 5"
        received_type = block_to_block_type(text)
        expected_type = BlockType.HEADING
        self.assertEqual(received_type, expected_type)

    def test_code(self):
        text = """```
Hello, world!
```"""
        received_type = block_to_block_type(text)
        expected_type = BlockType.CODE
        self.assertEqual(received_type, expected_type)

    def test_un_list(self):
        text = """- This is a list
- with items"""
        received_type = block_to_block_type(text)
        expected_type = BlockType.UNORDERED_LIST
        self.assertEqual(received_type, expected_type)

    def test_or_list(self):
        text = """1. first
2. second"""
        received_type = block_to_block_type(text)
        expected_type = BlockType.ORDERED_LIST
        self.assertEqual(received_type, expected_type)

    def test_quote(self):
        text = """> first
> second"""
        received_type = block_to_block_type(text)
        expected_type = BlockType.QUOTE
        self.assertEqual(received_type, expected_type)

    def test_paragraph(self):
        text = "just a text"
        received_type = block_to_block_type(text)
        expected_type = BlockType.PARAGRAPH
        self.assertEqual(received_type, expected_type)
