from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://boot.dev")
    print(text_node)
    
    html_node = HTMLNode(
        "<a>",
        "link", 
        None, 
        {"href": "https://www.google.com", "target": "_blank"},
        )
    
    print(html_node)
    print(html_node.props_to_html())
    
if __name__ == "__main__":
    main()