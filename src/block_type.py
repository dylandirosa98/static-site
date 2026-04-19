import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def block_to_block_type(block):
    if block[0:4] == "```\n" and block[-3:] == "```":
        return BlockType.CODE
    if re.match(r"^#{1,6}\s", block) is not None:
        return BlockType.HEADING
    quote = block.split("\n")
    x = True
    for i in range(len(quote)):
        if quote[i][0] == ">":
            pass
        else:
            x = False
    if x is True:
        return BlockType.QUOTE
    unorder = block.split("\n")
    y = True
    for i in range(len(unorder)):
        if unorder[i][0] == "-" and unorder[i][1] == " ":
            pass
        else:
            y = False
    if y is True:
        return BlockType.UNORDERED_LIST
    order = block.split("\n")
    z = True
    for i in range(len(order)):
        if order[i][0] == f"{i + 1}" and order[i][1:3] == ". ":
            pass
        else:
            z = False
    if z is True:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
