from enum import Enum


class LineType(Enum):
    COMMENT = "comment"
    INSTRUCTION = "instruction"
    DIRECTIVE = "directive"


def line_type(line: str) -> LineType:
    line = line.strip()
    if line == "" or line.startswith(";"):
        return LineType.COMMENT
    elif line.split(":")[-1].strip().startswith("."):
        return LineType.DIRECTIVE
    else:
        return LineType.INSTRUCTION
