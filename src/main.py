import os

from src.copy_static import copy_static
from src.page_generator import generate_pages_recursive


def main():
    copy_static()
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    path_to_content = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "content/"))
    path_to_template = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "template.html"))
    path_to_public = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "public/"))
    generate_pages_recursive(path_to_content, path_to_template, path_to_public)


if __name__ == "__main__":
    main()
