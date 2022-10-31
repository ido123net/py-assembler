from __future__ import annotations

import argparse
import pathlib
from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="assembler")
    parser.add_argument(
        "files",
        nargs="+",
        help="list off files to run the assembler on",
        type=pathlib.Path,
    )
    args = parser.parse_args(argv)
    for filename in args.files:
        with open(filename) as f:
            data = f.read()
        print(data.splitlines())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
