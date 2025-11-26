import re

from textnode import TextNode, TextType, text_node_to_html_node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            new_nodes.append(node)
            continue
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(split_node)):
            if split_node[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split_node[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_node[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        extracted_images = extract_markdown_images(original_text)
         
        if len(extracted_images) == 0:
            new_nodes.append(node)
            continue
        
        for image in extracted_images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]
            
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
            
    return new_nodes
            
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        extracted_links = extract_markdown_links(original_text)
        
        if len(extracted_links) == 0:
            new_nodes.append(old_node)
            continue
        
        for link in extracted_links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text):
    return split_nodes_delimiter(
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_link(
                    split_nodes_image(
                        [TextNode(text, TextType.TEXT)]
                    )
                ), 
                "**",
                TextType.BOLD
            ),
            "_", 
            TextType.ITALIC
        ),
        "`", 
        TextType.CODE
    )
    
def text_to_children(text: str) -> list:
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        child = text_node_to_html_node(text_node)
        children.append(child)
    return children
    