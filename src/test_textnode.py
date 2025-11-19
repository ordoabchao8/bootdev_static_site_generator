import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a TextNode", TextType.BOLD)
        node2 = TextNode("This is a TextNode", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_not_eq(self):
        node = TextNode("This is a bold TextNode", TextType.BOLD)
        node2 = TextNode("This is a different bold TextNode", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_url_is_none(self):
        node = TextNode("This is a bold TextNode", TextType.BOLD)
        self.assertIsNone(node.url)
        
    def test_url_not_none(self):
        node = TextNode("This is anchor text", TextType.LINK, "https://boot.dev")
        self.assertIsNotNone(node.url)
        
    def test_text_type_not_eq(self):
        node = TextNode("This is a bold TextNode", TextType.BOLD)
        node2 = TextNode("This is a italic TextNode", TextType.ITALIC)
        self.assertNotEqual(node.text_type, node2.text_type)
        
    def test_url_not_eq(self):
        node = TextNode("This is anchor text", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is anchor text", TextType.LINK, "https://youtube.com")
        self.assertNotEqual(node, node2)
    
    def test_url_eq(self):
        node = TextNode("This is anchor text", TextType.LINK, "https://boot.dev")
        node2= TextNode("This is anchor text", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)
    
if __name__ == "__main__":
    unittest.main()