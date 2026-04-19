def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for i in blocks:
        new_blocks.append(i.strip())
    while "" in new_blocks:
        new_blocks.remove("")
    return new_blocks
