import os

from extract_title import extract_title
from markdown_to_html_node import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f"Generating a page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        from_path_content = f.read()
    with open(template_path) as f:
        template_path_content = f.read()
    html_string = markdown_to_html_node(from_path_content).to_html()
    title = extract_title(from_path_content)
    template_path_content = template_path_content.replace("{{ Title }}", title)
    template_path_content = template_path_content.replace("{{ Content }}", html_string)
    dest_path_dir = os.path.dirname(dest_path)
    os.makedirs(dest_path_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_path_content)


def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content) is True:
        dest_dir_path = dest_dir_path.replace(".md", ".html")
        generate_page(dir_path_content, template_path, dest_dir_path)
    else:
        files = os.listdir(dir_path_content)
        for file in files:
            x = os.path.join(dir_path_content, file)
            y = os.path.join(dest_dir_path, file)
            if os.path.isfile(x) is True:
                y = y.replace(".md", ".html")
                generate_page(x, template_path, y)
            else:
                generate_pages_recursively(x, template_path, y)
