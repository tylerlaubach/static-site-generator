from textnode import TextType, TextNode
from htmlnode import LeafNode
import re

def text_node_to_html_node(text_node):
    '''Converts text node to equivalent HTML node'''
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag='b', value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag='i', value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag='code', value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag='a', value=text_node.text, props={'href': text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag='img', value='', props={'src': text_node.url, 'alt': text_node.text})
    else:
        raise Exception("text_type is invalid")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    '''Splits text type nodes based on text_type syntax'''
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            node_text_segs = node.text.split(delimiter)
            if len(node_text_segs) % 2 == 0:
                raise Exception("unmatched delimiters in text")

            for i, seg in enumerate(node_text_segs):
                if i % 2 == 0:
                    if seg:
                        new_nodes.append(TextNode(seg, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(seg, text_type))

    return new_nodes

def split_all_delimiters(nodes):
    '''Splits text nodes into code, bold, and italic TextTypes'''
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes

def extract_markdown_images(text):
    '''Takes raw markdown text with images and returns a list of tuples with the alt text and URL'''
    image_pattern = r'!\[(.*?)\]\((.*?)\)'
    return re.findall(image_pattern, text)

def extract_markdown_links(text):
    '''Takes raw markdown text with links and returns a list of tuples with the alt text and URL'''
    link_pattern = r'(?<!\!)\[(.*?)\]\((.*?)\)'
    return re.findall(link_pattern, text)

def split_nodes_image(old_nodes):
    '''Splits TextType.TEXT nodes with markdown-style images into TEXT and IMAGE nodes'''
    image_pattern = r'(!\[.*?\]\(.*?\))'
    image_info_pattern = r'!\[(.*?)\]\((.*?)\)'

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        splits = [s for s in re.split(image_pattern, node.text) if s]

        for split in splits:
            match = re.fullmatch(image_info_pattern, split)
            if match:
                alt_text, url = match.group(1), match.group(2)
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            else:
                new_nodes.append(TextNode(split, TextType.TEXT))
            
    return new_nodes

def split_nodes_link(old_nodes):
    link_pattern = r'(?<!\!)(\[.*?\]\(.*?\))'
    link_info_pattern = r'(?<!\!)\[(.*?)\]\((.*?)\)'

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        splits = [s for s in re.split(link_pattern, node.text) if s]

        for split in splits:
            match = re.fullmatch(link_info_pattern, split)
            if match:
                alt_text, url = match.group(1), match.group(2)
                new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            else:
                new_nodes.append(TextNode(split, TextType.TEXT))
            
    return new_nodes

def text_to_textnodes(text):
    '''Takes a string with markdown text and returns a list of TextNodes'''
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_image([node])
    nodes = split_nodes_link(nodes)
    nodes = split_all_delimiters(nodes)

    return nodes

def markdown_to_blocks(markdown):
    '''Splits a markdown string into a list of blocks'''
    return [block.strip() for block in markdown.split('\n\n') if block.strip()]


# markdown = """
# This is **bolded** paragraph

# This is another paragraph with _italic_ text and `code` here
# This is the same paragraph on a new line





# - This is a list
# - with items
# """
# print(markdown_to_blocks(markdown))