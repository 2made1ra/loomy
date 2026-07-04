import os
from pathlib import Path

from src.md_to_html import markdown_to_html_node
from src.utils import extract_title


def generate_page(
    from_path: str, template_path: str, dest_path: str, basepath: str
) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html_md = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    gen_html = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", html_md)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(gen_html)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str
) -> None:
    print(f"Generating pages from {dir_path_content}")

    all_entrys = os.listdir(dir_path_content)

    for entry in all_entrys:
        path_to_entry = os.path.join(dir_path_content, entry)
        if os.path.isfile(path_to_entry):
            new_path = os.path.join(dest_dir_path, Path(entry).with_suffix(".html"))
            generate_page(path_to_entry, template_path, new_path, basepath)
        else:
            new_dest_dir = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(
                path_to_entry, template_path, new_dest_dir, basepath
            )
