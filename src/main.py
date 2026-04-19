import os
import sys

from generate_page import generate_pages_recursively
from static_to_public import static_to_public


def main():
    if sys.argv[0] is None:
        base_path = "/"
    else:
        base_path = sys.argv

    static_to_public("static", "docs")
    generate_pages_recursively("content", "template.html", "docs", base_path)


if __name__ == "__main__":
    main()
