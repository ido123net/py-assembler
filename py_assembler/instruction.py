from __future__ import annotations

from dataclasses import dataclass

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


@dataclass
class Instruction:
    """This class represent an instruction"""

    label: str | None
    intruction: str
    parameter: list[str]
