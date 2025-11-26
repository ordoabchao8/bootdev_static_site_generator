import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ] 
        )
    
    def test_split_bold_delimiter(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT)
            ]
        )
    
    def test_split_italic_delimiter(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT)
            ]
        )
    
    def test_split_with_no_delimiter(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [TextNode("This is plain text", TextType.TEXT)]
        )
    
    def test_split_with_unmatched_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)
            
    def test_non_text_node_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual([node], new_nodes) 

class TestExtractMarkdown(unittest.TestCase):      
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://boot.dev)")
        self.assertListEqual([("link", "https://boot.dev")], matches)
        
    def test_extract_markdown_multiple_images(self):
        text = (
            "This is text with several images -  "
            "![image](https://i.imgur.com/zjjcJKZ.png) "
            "![image](https://i.imgur.com/zjjcJKZ.png)" 
            "![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("image","https://i.imgur.com/zjjcJKZ.png"),
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches
        )
        
    def test_extract_markdown_images_no_matches(self):
        matches = extract_markdown_images("This is text with no images at all")
        self.assertListEqual([], matches)
        
    def test_extract_markdown_links_no_matches(self):
        matches = extract_markdown_links("This is text with no links at all")
        self.assertListEqual([], matches)
        
    def test_extract_markdown_images_only_with_links(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links_only_with_images(self):
        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)")
        self.assertListEqual([("link", "https://boot.dev")], matches)
         
class TestSplitNodesLink(unittest.TestCase):
    def test_split_multiple_links(self):
        node = TextNode(
            "This is text with a [link to boot.dev](https://www.boot.dev) and another [link to youtube](https://www.youtube.com)",
            TextType.TEXT,
        )
        
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link to boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link to youtube", TextType.LINK, "https://www.youtube.com"),
            ],
            new_nodes
        )
    
    def test_split_single_link(self):
        node = TextNode(
            "This is text with a [link to boot.dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link to boot.dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes
        )
        
    def test_split_link_only(self):
        node = TextNode(
            "[link to boot.dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link to boot.dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes
        )
    
    def test_split_links_no_link(self):
        node = TextNode("No links here!", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("No links here!", TextType.TEXT)
            ],
            new_nodes
        )
    # Link or Image nodes already within the old nodes should be left alone during processing of text nodes.    
    def test_split_links_with_link_nodes_already_existing(self):
        old_nodes = [
            TextNode("This is text with a [link to boot.dev](https://www.boot.dev) and another [link to youtube](https://www.youtube.com)", TextType.TEXT),
            TextNode("second link to boot.dev", TextType.LINK, "https://www.boot.dev")
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link to boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link to youtube", TextType.LINK, "https://www.youtube.com"),
                TextNode("second link to boot.dev", TextType.LINK, "https://www.boot.dev")
            ],
            new_nodes
        )
        
    def test_split_links_empty_text(self):
        old_nodes = [TextNode("[link to boot.dev](https://www.boot.dev)[link to youtube.com](https://www.youtube.com)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("link to boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("link to youtube.com", TextType.LINK, "https://www.youtube.com")
            ],
            new_nodes
        )
        
    def test_split_links_mixed_list_of_nodes(self):
        old_nodes = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("link to boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode("This is a link to youtube.com [link](https://www.youtube.com)", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("link to boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("This is a link to youtube.com ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.youtube.com"),
            ],
            new_nodes
        )
        
    def test_split_links_multiple_text_nodes(self):
        old_nodes = [
            TextNode("This is text with a [link to boot.dev](https://www.boot.dev)", TextType.TEXT),
            TextNode("This is text with a [link to youtube](https://www.youtube.com)", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link to boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link to youtube", TextType.LINK, "https://www.youtube.com")
            ],
            new_nodes
        )
        
    def test_split_links_text_before(self):
        node = TextNode(
            "This a link with text BEFORE the link [link to boot.dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This a link with text BEFORE the link ", TextType.TEXT),
                TextNode("link to boot.dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes
        )
        
    def test_split_links_text_after(self):
        node = TextNode(
            "[link to boot.dev](https://www.boot.dev) This is a link with text AFTER the link",
            TextType.TEXT,
        )
        
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link to boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" This is a link with text AFTER the link", TextType.TEXT),
            ],
            new_nodes
        )
    
    def test_split_link_in_middle(self):
        node = TextNode(
            "This is text with a link in the middle [link](https://www.boot.dev) of the text",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link in the middle ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" of the text", TextType.TEXT),  
            ],
            new_nodes
        )
    
    
class TestSplitNodesImage(unittest.TestCase):
    def test_split_multiple_images(self):
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
        
    def test_split_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
        
    def test_split_image_only(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
      
    def test_split_images_no_image(self):
        node = TextNode("No images here!", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("No images here!", TextType.TEXT)
            ],
            new_nodes
        )
    
    def test_split_images_with_image_nodes_already_existing(self):
        old_nodes = [
            TextNode("This is text with a ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes
        )
        
    def test_split_images_empty_text(self):
        old_nodes = [TextNode("![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes
        )
           
    def test_split_images_mixed_list_of_nodes(self):
        old_nodes = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("link to boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode("This is an image ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("link to boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("This is an image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes
        )
             
    def test_split_images_multiple_text_nodes(self):
        old_nodes = [
            TextNode("This is text with a ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            TextNode("This is text with a ![second image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes
        )
    
    def test_split_images_text_before(self):
        node = TextNode(
            "This an image with text BEFORE the image ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This an image with text BEFORE the image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes
        )
     
    def test_split_images_text_after(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) This is an image with text AFTER the image",
            TextType.TEXT,
        )
        
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" This is an image with text AFTER the image", TextType.TEXT),
            ],
            new_nodes
        )
    
    def test_split_image_in_middle(self):
        node = TextNode(
            "This is text with an image in the middle ![image](https://i.imgur.com/zjjcJKZ.png) of the text",
            TextType.TEXT,
        )
        
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image in the middle ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" of the text", TextType.TEXT),
            ],
            new_nodes
        )
 
class TestTextToTextNodes(unittest.TestCase):
    def test_full_complex_markdown_string(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
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
            ],
            nodes
        )
    
    def test_only_bold(self):
        text = "This is text with a **bold** word"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT)
            ],
            nodes
        )
    
    def test_only_italic(self):
        text = "This is text with an _italic_ word"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT)                                
            ],
            nodes
        )
        
    def test_only_code(self):
        text = "This is text with `code` markdown"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" markdown", TextType.TEXT)
            ],
            nodes
        )
        
if __name__ == "__main__":
    unittest.main()