import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node

def generate_page(source_path, template_path, destination_path):
    print(f"Generating page from {source_path} to {destination_path} using {template_path}")
    with open(source_path, "r") as file:
        markdown_content = file.read()
    
    with open(template_path, "r") as file:
        template_content = file.read()
      
    nodes = markdown_to_html_node(markdown_content)
    html_nodes = nodes.to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_nodes)
    
    dirpath = os.path.dirname(destination_path)
    
    if dirpath != "" and not os.path.exists(destination_path):
        os.makedirs(dirpath, exist_ok=True)
        
    with open(destination_path, "w") as file:
        file.write(template_content)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    content_dir = Path(dir_path_content)
    dest_dir = Path(dest_dir_path)
    dest_dir.mkdir(parents=True, exist_ok=True)
        
    for path in content_dir.iterdir():
        if path.is_file() and path.suffix == ".md":
            dest_file = dest_dir / (path.stem + ".html")
            generate_page(path, template_path, dest_file)
        if path.is_dir():
            dest_subdir = dest_dir / path.name
            generate_page_recursive(path, template_path, dest_subdir)
       
def extract_title(markdown: str) -> str:    
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            line = line[1:].strip()
            return line
    raise Exception("Error no title found in markdown provided")