import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_props_is_none(self):
        node = HTMLNode("a", "link", None, None)
        self.assertEqual(node.props_to_html(), "")
        
    def test_props_is_empty(self):
        node = HTMLNode("a", "link", None, {})
        self.assertEqual(node.props_to_html(), "")
        
    def test_props_has_value(self):
        node = HTMLNode("a", "link", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(),' href="https://www.google.com" target="_blank"')
        
    def test_to_html(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)    
    
    def test_htmlnode_repr(self):
        node = HTMLNode("a", "link", None, {"href": "https://www.google.com", "target": "_blank"})
        r = repr(node)
        self.assertIn("a", r)
        self.assertIn("link", r)
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_none_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)
    
    def test_leaf_none_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), f"{node.value}")
        
    def test_leaf_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), f"<{node.tag}{node.props_to_html()}>{node.value}</{node.tag}>")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_to_html_multiple_parents(self):
        child_node = LeafNode("b", "child")
        parent_node = ParentNode("span", [child_node])
        second_parent = ParentNode("div",[parent_node])
        third_parent = ParentNode("p", [second_parent])
        self.assertEqual(
            third_parent.to_html(),
            "<p><div><span><b>child</b></span></div></p>",
        )
    
    def test_parent_to_html_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("span", None).to_html()
        
    def test_parent_to_html_multiple_children(self):
        child_node = LeafNode("b", "child")
        second_child_node = LeafNode("i", "second_child")
        third_child_node = LeafNode("p", "third child")
        parent_node = ParentNode("div", [child_node, second_child_node, third_child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>child</b><i>second_child</i><p>third child</p></div>"
        )
    
    def test_parent_props_is_none(self):
        # When no props are provided, the tag should have no attributes
        child_node = LeafNode("b", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>child</b></div>"
        )
        
    def test_parent_with_props(self):
        # When props are provided, the tag should have attributes
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("a", [child_node], {"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(
            parent_node.to_html(),
            '<a href="https://boot.dev" target="_blank"><span>child</span></a>'
        
        )
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertIsNone(html_node.props)
        
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
        self.assertIsNone(html_node.props)
        
    def test_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")
        self.assertIsNone(html_node.props)
        
    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
        self.assertIsNone(html_node.props)
        
    def test_link(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot.dev")
        self.assertIsNotNone(html_node.props)
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})
        
    def test_image(self):
        node = TextNode("Funny Cat Picture", TextType.IMAGE, "https://boot.dev/funny_cat.jpeg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": node.url, "alt": node.text})
        
if __name__ == "__main__":
    unittest.main()