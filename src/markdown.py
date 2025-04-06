from enum import Enum
import re

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

