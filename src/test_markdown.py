import unittest
from markdown import *
from htmlnode import ParentNode, LeafNode

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

    def test_markdown_to_html_node_paragraph(self):
        md = 'This is a paragraph with **bold** text.'
        correct_result = ParentNode('div', children=[
            ParentNode('p', children=[
                LeafNode(None, 'This is a paragraph with '),
                LeafNode('b', 'bold'),
                LeafNode(None, ' text.')
            ])
        ])
        self.assertEqual(correct_result.__repr__(), markdown_to_html_node(md).__repr__())

    def test_markdown_to_html_node_heading(self):
        md = '###### THIS IS A HEADING'
        correct_result = ParentNode('div', children=[
            ParentNode('h6', children=[
                LeafNode(None, 'THIS IS A HEADING'),
            ])
        ])
        self.assertEqual(correct_result.__repr__(), markdown_to_html_node(md).__repr__())

    def test_markdown_to_html_node_code(self):
        md = '```this is a code block```'
        correct_result = ParentNode('div', children=[
            LeafNode('code', 'this is a code block'),
        ])
        self.assertEqual(correct_result.__repr__(), markdown_to_html_node(md).__repr__())

    def test_markdown_to_html_node_quote(self):
        md = "> This is a quote\n> with multiple lines"
        correct_result = ParentNode('div', children=[
            ParentNode('blockquote', children=[
                LeafNode(None, 'This is a quote\nwith multiple lines'),
            ])
        ])
        self.assertEqual(correct_result.__repr__(), markdown_to_html_node(md).__repr__())

    def test_markdown_to_html_node_unordered_list(self):
        md = "- item one\n- item two"
        correct_result = ParentNode('div', children=[
            ParentNode('ul', children=[
                ParentNode('li', children=[LeafNode(None, 'item one')]),
                ParentNode('li', children=[LeafNode(None, 'item two')]),
            ])
        ])
        self.assertEqual(correct_result.__repr__(), markdown_to_html_node(md).__repr__())

    def test_markdown_to_html_node_ordered_list(self):
        md = "1. first\n2. second"
        correct_result = ParentNode('div', children=[
            ParentNode('ol', children=[
                ParentNode('li', children=[LeafNode(None, 'first')]),
                ParentNode('li', children=[LeafNode(None, 'second')]),
            ])
        ])
        self.assertEqual(correct_result.__repr__(), markdown_to_html_node(md).__repr__())

    def test_markdown_to_html_node_combined(self):
        md = """## Heading

This is a **paragraph** with _style_.

> This is a quote

"""
        correct_result = ParentNode('div', children=[
            ParentNode('h2', children=[
                LeafNode(None, 'Heading')
            ]),
            ParentNode('p', children=[
                LeafNode(None, 'This is a '),
                LeafNode('b', 'paragraph'),
                LeafNode(None, ' with '),
                LeafNode('i', 'style'),
                LeafNode(None, '.')
            ]),
            ParentNode('blockquote', children=[
                LeafNode(None, 'This is a quote'),
            ])
        ])
        self.assertEqual(correct_result.__repr__(), markdown_to_html_node(md).__repr__())