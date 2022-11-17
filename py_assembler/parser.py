from __future__ import annotations

import logging
import re
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)

pattern = re.compile(
    r"^(?:([a-zA-Z][a-zA-Z0-9]{0,30}):\s)?\s*(\.?[\w]+)(?:\s+([\"\$0-9\,a-zA-Z\s-]*))?$",
)


class InvalidLine(Exception):
    def __init__(self, line: str, *args: object) -> None:
        self.line = line
        super().__init__(*args)

    def __str__(self) -> str:
        return f"{self.line!r} is not following the requirements."


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


def split_line(line: str) -> tuple[str | Any, ...]:
    match = pattern.search(line.strip())
    if match is None:
        raise InvalidLine(line)
    return match.groups()
