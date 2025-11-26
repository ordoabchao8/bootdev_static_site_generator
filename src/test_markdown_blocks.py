import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from main import markdown_to_html_node

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
This is a **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items        
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items"   
            ],
        )
        
    def test_markdown_to_blocks_no_newlines(self):
        md = "This is a single paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a single paragraph"
            ]
        )
        
    def test_markdown_to_blocks_no_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            []
        )
    
    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n  \t  \n    "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
        
    def test_markdown_soft_breaks_preserved(self):
        md = "First line of paragraph\nSecond line of paragraph\n\nAnother block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
              "First line of paragraph\nSecond line of paragraph",
              "Another block"  
            ],
        )
        
    def test_markdown_leading_newlines(self):
        md = "\n\n\n\n# Heading\n\nParagraph\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph"
            ]
        )
    
    def test_markdown_trailing_newlines(self):
        md = "# Heading\n\nParagraph\n\n\n\n- List item 1\n- List item 2\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph",
                "- List item 1\n- List item 2"
            ]
        )
        
class TestBlockToBlockType(unittest.TestCase):
    def test_markdown_block_type_heading(self):
        md = "# Heading"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)
        
    def test_markdown_block_type_code(self):
        md = "```\ncode\n```"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)
        
    def test_markdown_block_type_quote(self):
        md = ">This is a quote"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)
        
    def test_markdown_block_type_ulist(self):
        md = "- First entry in an unordered list"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.ULIST)
        
    def test_markdown_block_type_olist(self):
        md = "1. First entry in an ordered list"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.OLIST)
        
    def test_markdown_block_type_paragraph(self):
        md = "This is a paragraph only"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    def test_markdown_blocks_types_integration(self):
        md = "# Heading\n\n## Second Heading\n\n- item1\n- item2\n\nParagraph\n\n>This is a quote\n\n```\ncode block\n```\n\n> Another Quote Block"
        blocks = markdown_to_blocks(md)
        types = [block_to_block_type(block) for block in blocks]
        self.assertEqual(
            types,
            [BlockType.HEADING, BlockType.HEADING, BlockType.ULIST, BlockType.PARAGRAPH, BlockType.QUOTE, BlockType.CODE, BlockType.QUOTE]
        )
        
        
class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        
    def test_blockquote(self):
        md = """
>This is a blockquote
>same quote

>This is another blockquote        
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote\nsame quote</blockquote><blockquote>This is another blockquote</blockquote></div>"
        )
    
    def test_heading(self):
        md = """
# Heading 1

## Heading 2
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2></div>"
        )
    
    def test_unordered_list(self):
        md = """
- List item 1
- List item 2

- Second list item 1
- Second list item 2        
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>List item 1</li><li>List item 2</li></ul><ul><li>Second list item 1</li><li>Second list item 2</li></ul></div>"
        )
    
    def test_ordered_list(self):
        md = """
1. Ordered List item 1
2. Ordered List item 2

1. Second Ordered List item 1
2. Second Ordered List item 2        
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>1. Ordered List item 1</li><li>2. Ordered List item 2</li></ol><ol><li>1. Second Ordered List item 1</li><li>2. Second Ordered List item 2</li></ol></div>"
        )