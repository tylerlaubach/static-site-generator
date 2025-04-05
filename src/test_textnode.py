import unittest
from textnode import TextNode, TextType
from conversions import text_node_to_html_node, split_all_delimiters

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("test node", TextType.ITALIC, None)
        node2 = TextNode("test node", TextType.ITALIC, None)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("test node", TextType.ITALIC, None)
        node2 = TextNode("test node", TextType.ITALIC, "https://www.hotmail.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, 'www.msn.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props['src'], 'www.msn.com')
        self.assertEqual(html_node.props['alt'], 'This is an image node')

    def test_split_all_delimiters_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_node = split_all_delimiters([node])
        self.assertEqual(new_node, 
                         [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT),
                        ])

    def test_split_all_delimiters_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_node = split_all_delimiters([node])
        self.assertEqual(new_node, 
                         [
                            TextNode("This is text with an ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word", TextType.TEXT),
                        ])

    def test_split_all_delimiters_multiple(self):
        node = TextNode("This is **bold and _italic_** text", TextType.TEXT)
        new_node = split_all_delimiters([node])
        self.assertEqual(new_node, 
                         [
                            TextNode("This is ", TextType.TEXT),
                            TextNode("bold and _italic_", TextType.BOLD),
                            TextNode(" text", TextType.TEXT),
                        ])

if __name__ == "__main__":
    unittest.main()