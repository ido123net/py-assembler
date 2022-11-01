from __future__ import annotations

import re
from enum import Enum

from py_assembler.instruction import InstructionLine
from py_assembler.instruction import INSTRUCTIONS


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


def is_valid_label(label: str) -> bool:
    if len(label) > 31 or len(label.split()) != 1:
        return False

    for instruction_type in INSTRUCTIONS:
        if label in instruction_type:
            return False

    return re.compile(r"[a-zA-Z][a-zA-Z0-9]*").match(label) is not None


def instruction_line_parse(instruction_line: str) -> InstructionLine:
    if ":" in instruction_line:
        label, _, instruction = instruction_line.partition(":")
    else:
        label, instruction = None, instruction_line
    cmd, *args = re.split(r"[\s,]+", instruction.strip())
    return InstructionLine(label, cmd, args)
