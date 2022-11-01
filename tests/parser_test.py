from __future__ import annotations

import pytest

from py_assembler.instruction import get_instruction_type
from py_assembler.instruction import InstructionLine
from py_assembler.instruction import InstuctionType
from py_assembler.instruction import InvalidInsrtuction
from py_assembler.parser import instruction_line_parse
from py_assembler.parser import is_valid_label
from py_assembler.parser import line_type
from py_assembler.parser import LineType


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        (";this is a commant", LineType.COMMENT),
        ("  ; ", LineType.COMMENT),
        ("          ", LineType.COMMENT),
        ("", LineType.COMMENT),
        (".entry Next", LineType.DIRECTIVE),
        (".extern wNumber", LineType.DIRECTIVE),
        ('STR:    .asciz  "aBcd"', LineType.DIRECTIVE),
        ("MAIN:   add     $3,$5,$9", LineType.INSTRUCTION),
        ("LOOP:   ori     $9,-5,$2", LineType.INSTRUCTION),
        ("        la      val1", LineType.INSTRUCTION),
        ("        jmp     Next", LineType.INSTRUCTION),
        ("Next:   move    $20,$4", LineType.INSTRUCTION),
        ("LIST:   .db     6,-9", LineType.DIRECTIVE),
        ("        bgt     $4,$2,END", LineType.INSTRUCTION),
        ("        la      K", LineType.INSTRUCTION),
        ("        sw      $0,4,$10", LineType.INSTRUCTION),
        ("        bne     $31,$9,LOOP", LineType.INSTRUCTION),
        ("        call    val1", LineType.INSTRUCTION),
        ("        jmp     $4", LineType.INSTRUCTION),
        ("        la      wNumber", LineType.INSTRUCTION),
        (".extern val1", LineType.DIRECTIVE),
        ("        .dh     27056", LineType.DIRECTIVE),
        ("K:      .dw     31,-12", LineType.DIRECTIVE),
        ("END:    stop", LineType.INSTRUCTION),
        (".entry K", LineType.DIRECTIVE),
    ),
)
def test_line_type(input_s, expected):
    assert line_type(input_s) == expected


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("validLabel", True),
        ("hEllo", True),
        ("x", True),
        ("He78902", True),
        ("", False),
        ("contain space", False),
        ("1startWithNumber", False),
        ("veryveryveryveryveryverylonglabel", False),
    ),
)
def test_is_valid_label(input_s, expected):
    assert is_valid_label(input_s) == expected


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        (
            "MAIN:   add     $3,$5,$9",
            InstructionLine("MAIN", "add", ["$3", "$5", "$9"]),
        ),
        (
            "LOOP:   ori     $9,-5,$2",
            InstructionLine("LOOP", "ori", ["$9", "-5", "$2"]),
        ),
        (
            "la val1",
            InstructionLine(None, "la", ["val1"]),
        ),
        (
            "   jmp	   Next",
            InstructionLine(None, "jmp", ["Next"]),
        ),
        (
            "Next:   move    $20,$4",
            InstructionLine("Next", "move", ["$20", "$4"]),
        ),
        (
            "	bgt	$4,	$2,	END",
            InstructionLine(None, "bgt", ["$4", "$2", "END"]),
        ),
        (
            "END:    stop",
            InstructionLine("END", "stop", []),
        ),
    ),
)
def test_instruction_line_parse(input_s, expected):
    assert instruction_line_parse(input_s) == expected


@pytest.mark.parametrize(
    ("instruction_line", "instruction_type"),
    (
        (
            InstructionLine("MAIN", "add", ["$3", "$5", "$9"]),
            InstuctionType.R,
        ),
        (
            InstructionLine("LOOP", "ori", ["$9", "-5", "$2"]),
            InstuctionType.I,
        ),
        (
            InstructionLine(None, "la", ["val1"]),
            InstuctionType.J,
        ),
    ),
)
def test_instruction_line_type(instruction_line, instruction_type):
    assert get_instruction_type(instruction_line) == instruction_type


@pytest.mark.parametrize(
    ("instruction", "expected"),
    (
        (
            "NotInstruction",
            "'NotInstruction' is not valid instruction!",
        ),
        (
            "Add",
            "'Add' is not valid instruction!",
        ),
        (
            "ADD",
            "'ADD' is not valid instruction!",
        ),
    ),
)
def test_invalid_instruction(instruction, expected):
    with pytest.raises(InvalidInsrtuction) as excinfo:
        get_instruction_type(InstructionLine(None, instruction, []))
    assert str(excinfo.value) == expected
