import unittest

from htmlnode import HTMLNode

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
        
        
    