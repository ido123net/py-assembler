from __future__ import annotations

import pytest

from py_assembler.instruction import Instruction
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
            Instruction("MAIN", "add", ["$3", "$5", "$9"]),
        ),
        (
            "LOOP:   ori     $9,-5,$2",
            Instruction("LOOP", "ori", ["$9", "-5", "$2"]),
        ),
        (
            "la val1",
            Instruction(None, "la", ["val1"]),
        ),
        (
            "   jmp	   Next",
            Instruction(None, "jmp", ["Next"]),
        ),
        (
            "Next:   move    $20,$4",
            Instruction("Next", "move", ["$20", "$4"]),
        ),
        (
            "	bgt	$4,	$2,	END",
            Instruction(None, "bgt", ["$4", "$2", "END"]),
        ),
        (
            "END:    stop",
            Instruction("END", "stop", []),
        ),
    ),
)
def test_instruction_line_parse(input_s, expected):
    assert instruction_line_parse(input_s) == expected
