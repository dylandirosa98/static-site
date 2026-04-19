def extract_title(markdown):
    text = markdown.split("\n")
    for line in text:
        if line[:2] == "# ":
            return line[2:]
    raise Exception
