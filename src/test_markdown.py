import unittest
from markdown import BlockType, block_to_block_type

class TestMarkdown(unittest.TestCase):
    def test_block_to_block_heading(self):
        markdown_block = """###### This is a heading"""
        self.assertEqual(BlockType.HEADING, block_to_block_type(markdown_block))

    def test_block_to_block_code(self):
        markdown_block = """```
this
is
code
```"""
        self.assertEqual(BlockType.CODE, block_to_block_type(markdown_block))

    def test_block_to_block_quote(self):
        markdown_block = """>this
>is
>quoted
>text"""
        self.assertEqual(BlockType.QUOTE, block_to_block_type(markdown_block))

    def test_block_to_block_unordered_list(self):
        markdown_block = """- this
- is
- an unordered
- list"""
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(markdown_block))

    def test_block_to_block_ordered_list(self):
        markdown_block = """1. this
2. is
3. an ordered
4. list"""
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(markdown_block))

    def test_block_to_block_paragraph(self):
        markdown_block = """-this is a ```paragraph``` with some 1. tricky characters"""
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(markdown_block))