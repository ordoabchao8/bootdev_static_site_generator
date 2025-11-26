from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType
from inline_markdown import text_to_children, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "ulist"
    OLIST = "olist"
    
def markdown_to_blocks(markdown):
    new_blocks = []
    split_markdown =  markdown.split("\n\n")
    for block in split_markdown:
        split_block = block.strip()
        
        if split_block != "":
            new_blocks.append(split_block)
        
    return new_blocks

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ","#### ","##### ","###### ")):
            return BlockType.HEADING
        
    elif len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    
    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    
    elif block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> ParentNode:
    block_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING: 
                heading_text = extract_heading_text(block)
                level = extract_heading_level(block)
                children = text_to_children(heading_text)
                heading_node = ParentNode(f"h{level}", children=children)
                block_nodes.append(heading_node)
                
            case BlockType.PARAGRAPH:
                cleaned_string = extract_paragraph_text(block)
                children = text_to_children(cleaned_string)
                block_nodes.append(ParentNode("p", children=children))
                
            case BlockType.QUOTE:
                cleaned_string = extract_quote_text(block)
                children = text_to_children(cleaned_string)
                block_nodes.append(ParentNode("blockquote", children=children))
            
            case BlockType.CODE:
                cleaned_string = extract_code_text(block)
                block_nodes.append(ParentNode("pre", [text_node_to_html_node(TextNode(cleaned_string, TextType.CODE))]))
            
            case BlockType.ULIST:
                cleaned_list_items = extract_unordered_list_text(block)
                children = create_unordered_list_of_parentnodes(cleaned_list_items)
                block_nodes.append(ParentNode("ul", children=children))
                
            case BlockType.OLIST:
                cleaned_list_items = extract_ordered_list_item_text(block)
                children = create_ordered_list_of_parentnodes(cleaned_list_items)
                block_nodes.append(ParentNode("ol", children=children))
                
    return ParentNode("div", children=block_nodes)

def extract_paragraph_text(block: str) -> str:
    new_items = []
    split_block = block.split("\n")
    for item in split_block:
        item = item.strip()
        new_items.append(item)
    return " ".join(new_items)

def extract_heading_level(block: str) -> int:
    count = 0 
    for char in block.lstrip():
        if char != "#":
            break
        count += 1
    return min(count, 6)    

def extract_heading_text(block: str) -> str:
    level = extract_heading_level(block)
    stripped = block.lstrip()
    text_part = stripped[level:]
    if text_part.startswith(" "):
        text_part = text_part[1:]
    return text_part

def extract_quote_text(block: str) -> str:
    cleaned_lines = []
    lines = block.split("\n")
    for line in lines:
        line = line.lstrip()
        if line.startswith(">"):
            cleaned_lines.append(line[1:].lstrip())
        elif line != "":
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)
                    
def extract_code_text(block: str) -> str:   
    lines = block.split("\n")
    inner_lines = lines[1:-1]
    return "\n".join(inner_lines) + "\n"
    
def extract_unordered_list_text(block: str) -> list:
    cleaned_lines = []
    lines = block.split("\n")
    for line in lines:
        line = line.lstrip()
        if line.startswith("-"):
            cleaned_lines.append(f"{line[1:].lstrip()}")
    return cleaned_lines
    
def create_unordered_list_of_parentnodes(cleaned_lines: list) -> list[ParentNode]:
    new_lines = []
    for item in cleaned_lines:
        new_lines.append(ParentNode("li", children=text_to_children(item)))

    return new_lines

def extract_ordered_list_item_text(block: str) -> list:
    cleaned_lines = []
    lines = block.split("\n")
    i = 1
    for line in lines:
        if line.startswith(f"{i}. "):
            cleaned_lines.append(line[3:].lstrip())
        i += 1
    return cleaned_lines

def create_ordered_list_of_parentnodes(cleaned_lines: list) -> list[ParentNode]:
    new_lines = []
    for item in cleaned_lines:
        new_lines.append(ParentNode("li", children=text_to_children(item)))
    return new_lines