from copystatic import copy_static
from generate_page import generate_page_recursive

def main():
    copy_static("static")
    generate_page_recursive("content", "template.html", "public")
    
    
if __name__ == "__main__":
    main()