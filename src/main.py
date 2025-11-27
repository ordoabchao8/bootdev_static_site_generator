from copystatic import copy_static
from generate_page import generate_page_recursive
import sys

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    copy_static("static")
    generate_page_recursive("content", "template.html", "docs", basepath)
    
    
if __name__ == "__main__":
    main()