from __future__ import annotations

import pytest

from py_assembler.parser import InvalidLine
from py_assembler.parser import split_line


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        (".entry Next", (None, ".entry", "Next")),
        (".extern wNumber", (None, ".extern", "wNumber")),
        ('STR:    .asciz  "aBcd"', ("STR", ".asciz", '"aBcd"')),
        ("MAIN:   add     $3,$5,$9", ("MAIN", "add", "$3,$5,$9")),
        ("LOOP:   ori     $9,-5,$2", ("LOOP", "ori", "$9,-5,$2")),
        ("        la      val1", (None, "la", "val1")),
        ("   LIST:   .db     6,-9\t\n", ("LIST", ".db", "6,-9")),
        (".extern val1", (None, ".extern", "val1")),
        ("        .dh     27056", (None, ".dh", "27056")),
        ("K:      .dw     31,  -12", ("K", ".dw", "31,  -12")),
        ("END:    stop", ("END", "stop", None)),
        (".entry K", (None, ".entry", "K")),
    ),
)
def test_good_split_line(input_s, expected):
    assert split_line(input_s) == expected


@pytest.mark.parametrize(
    ("input_s"),
    (
        ("..entry Next"),
        ("1bad: .extern wNumber"),
        ("bad : .extern wNumber"),
    ),
)
def test_bad_split_line(input_s):
    with pytest.raises(InvalidLine, match=f"'{input_s}' is not following the requirements."):
        split_line(input_s)
