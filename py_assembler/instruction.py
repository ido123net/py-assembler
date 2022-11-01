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

INSTRUCTIONS = (R_INSTRUCTIONS, I_INSTRUCTIONS, J_INSTRUCTIONS)


class InvalidInsrtuction(Exception):
    pass


class InstuctionType(Enum):
    R = 0
    I = 1  # noqa: E741
    J = 2


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
        return InstuctionType.R
    if instruct in I_INSTRUCTIONS:
        return InstuctionType.I
    if instruct in J_INSTRUCTIONS:
        return InstuctionType.J
    raise InvalidInsrtuction(f"{instruct!r} is not valid instruction!")
