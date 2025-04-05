import unittest
from textnode import TextNode, TextType
from conversions import *

class TestConversions(unittest.TestCase):
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
        
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],
                             matches)
        
    def test_extract_markdown_images_and_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        images =  extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], images)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], links)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_with_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a [link](https://www.boot.dev)", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        correct_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(correct_result, text_to_textnodes(text))
    
    def test_text_to_textnodes_multiples(self):
        text = 'This is **text** with **multiple** bold and _italic_ _words_ and `code` `blocks` and ![image1](https://i.imgur.com/sample1.jpeg) and ![image2](https://i.imgur.com/sample2.jpeg) and [link1](https://boot.dev) and [link2](https://google.com)'
        correct_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with ", TextType.TEXT),
            TextNode("multiple", TextType.BOLD),
            TextNode(" bold and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("words", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("blocks", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "https://i.imgur.com/sample1.jpeg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "https://i.imgur.com/sample2.jpeg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://google.com"),
        ]
        self.assertListEqual(correct_result, text_to_textnodes(text))
    
    def test_text_to_textnodes_adjacent_delimiters(self):
        text = 'This is **Text****With****Multiple**_Italic__Words_'
        correct_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("Text", TextType.BOLD),
            TextNode("With", TextType.BOLD),
            TextNode("Multiple", TextType.BOLD),
            TextNode("Italic", TextType.ITALIC),
            TextNode("Words", TextType.ITALIC),
        ]
        self.assertListEqual(correct_result, text_to_textnodes(text))

if __name__ == "__main__":
    unittest.main()