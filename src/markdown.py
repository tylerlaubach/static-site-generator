from enum import Enum
import re
from conversions import markdown_to_blocks, text_to_textnodes, text_node_to_html_node
from htmlnode import ParentNode, LeafNode

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def block_to_block_type(markdown_block):
    '''Takes a single markdown block and returns its BlockType'''
    # Heading
    heading_pattern = r'^#{1,6} .+'
    if re.match(heading_pattern, markdown_block):
        return BlockType.HEADING
    # Code
    if markdown_block.startswith('```') and markdown_block.endswith('```'):
        return BlockType.CODE
    # Quote/Unordered List/Ordered List
    lines = [line for line in markdown_block.split('\n')]
    if all(item.startswith('>') for item in lines):
        return BlockType.QUOTE
    if all(item.startswith('- ') for item in lines):
        return BlockType.UNORDERED_LIST
    for i, line in enumerate(lines):
        if not line.startswith(f'{i + 1}. '):
            break
    else:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    '''Converts text into a list of component HTMLNodes'''
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]

def get_tag_for_block_type(block_type, block):
    '''Accepts a block_type and block, and returns the proper tag'''
    tag_map = {
        BlockType.PARAGRAPH: 'p',
        BlockType.CODE: 'code',
        BlockType.QUOTE: 'blockquote',
        BlockType.UNORDERED_LIST: 'ul',
        BlockType.ORDERED_LIST: 'ol',
    }

    if block_type == BlockType.HEADING:
        header_num = len(block.split(' ')[0]) # Count number of # characters
        return f'h{header_num}'
    else:
        if block_type not in tag_map:
            return ValueError('block_type is invalid')
        return tag_map[block_type]
    
def get_text_for_block(block_type, block):
    '''Accepts a non-list-type block and returns a cleaned string'''
    if block_type == BlockType.PARAGRAPH:
        return block
    elif block_type == BlockType.HEADING:
        return block.split(' ', maxsplit=1)[1]
    elif block_type == BlockType.CODE:
        return block[3:-3].strip()
    elif block_type == BlockType.QUOTE:
        return '\n'.join([line.lstrip('> ').strip() for line in block.split('\n')])
    else:
        raise ValueError("unsupported block_type")
    
def get_list_items_for_block(block_type, block):
    '''Accepts a list-type block and returns a list of cleaned strings'''
    if block_type == BlockType.UNORDERED_LIST:
        return [line.lstrip('- ').strip() for line in block.split('\n')]
    elif block_type == BlockType.ORDERED_LIST:
        return [line.split('. ', maxsplit=1)[1].strip() for line in block.split('\n')]
    else:
        raise ValueError("only works for unordered_list or ordered_list")
    
def get_cleaned_text(block_type, block):
    '''Returns cleaned text values from a markdown block'''
    if block_type in [BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST]:
        return get_list_items_for_block(block_type, block)
    else:
        return get_text_for_block(block_type, block)


def markdown_to_html_node(markdown):
    '''Converts a full markdown document into a single parent HTMLNode'''
    # Convert to blocks
    blocks = markdown_to_blocks(markdown)
    html_children = []
    # Loop over each block
    for block in blocks:
        # Determine block type
        block_type = block_to_block_type(block)
        # Based on the type of block, create a new HTMLNode with the proper data
        if block_type == BlockType.CODE:
            # Special case – no inline markdown parsing
            tag = get_tag_for_block_type(block_type, block)
            text = get_cleaned_text(block_type, block)
            html_children.append(LeafNode(tag=tag, value=text))
        elif block_type in [BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST]:
            # Handle list blocks
            items = get_list_items_for_block(block_type, block)
            list_item_nodes = []
            for item in items:
                children = text_to_children(item)
                list_item_nodes.append(ParentNode('li', children))
            
            tag = get_tag_for_block_type(block_type, block)
            html_children.append(ParentNode(tag, list_item_nodes))

        else:
            # All other block types
            text = get_text_for_block(block_type, block)
            children = text_to_children(text)
            tag = get_tag_for_block_type(block_type, block)
            html_children.append(ParentNode(tag, children))

    return ParentNode(tag='div', children=html_children)

# md = '- item one\n- item two'
# print(markdown_to_html_node(md).to_html())