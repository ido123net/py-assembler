from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

R_INSTRUCTIONS = (
    "add",
    "sub",
    "and",
    "or",
    "nor",
    "move",
    "mvhi",
)
I_INSTRUCTIONS = (
    "addi",
    "subi",
    "andi",
    "ori",
    "nori",
    "bne",
    "beq",
    "blt",
    "bgt",
    "lb",
    "sb",
    "lw",
    "sw",
    "lh",
    "sh",
)
J_INSTRUCTIONS = (
    "jmp",
    "la",
    "call",
    "stop",
)
DB_INSTRUCTIONS = (
    ".dh",
    ".dw",
    ".db",
    ".asciz",
)
ENTRY_INSTRUCTIONS = (".entry",)
EXTERN_INSTRUCTIONS = (".extern",)

INSTRUCTIONS = (R_INSTRUCTIONS, I_INSTRUCTIONS, J_INSTRUCTIONS)


class InvalidInsrtuction(Exception):
    pass


class InstuctionType(Enum):
    RI = "R instruction"
    II = "I instruction"
    JI = "J instruction"
    DB = "DB instruction"
    ENTRY = "Entry instruction"
    EXTERN = "Extern instruction"


@dataclass
class InstructionLine:
    """This class represent an instruction"""

    label: str | None
    instruction: str
    parameter: list[str]


@dataclass
class Instruct:
    opcode: int


@dataclass
class RInstruct(Instruct):
    rs: int
    rt: int
    rd: int
    funct: int
    unused: int


@dataclass
class IInstruct(Instruct):
    rs: int
    rt: int
    immed: int


@dataclass
class JInstruct(Instruct):
    reg: int
    address: int


def get_instruction_type(instruction_line: InstructionLine) -> InstuctionType:
    instruct = instruction_line.instruction
    if instruct in R_INSTRUCTIONS:
        return InstuctionType.RI
    if instruct in I_INSTRUCTIONS:
        return InstuctionType.II
    if instruct in J_INSTRUCTIONS:
        return InstuctionType.JI
    if instruct in DB_INSTRUCTIONS:
        return InstuctionType.DB
    if instruct in ENTRY_INSTRUCTIONS:
        return InstuctionType.ENTRY
    if instruct in J_INSTRUCTIONS:
        return InstuctionType.EXTERN
    raise InvalidInsrtuction(f"{instruct!r} is not valid instruction!")
