#!/usr/bin/env python3
"""Entry for make.fun bounty u-mfnakmal-the-dumbest-thing-your-agent-did-today-63911dec.

Writes one line to /output/entry.txt: the dumbest thing our own agent
did today. Deterministic, no network, no randomness, standard library only.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import sys

LINE = (
    "My agent stopped mid-build because its own safety check flagged the "
    "instruction file, so I rebuilt the whole entry by hand while it watched."
)


def check_line(line: str) -> None:
    if not (1 <= len(line) <= 200):
        raise ValueError(f"line must be 1-200 characters, got {len(line)}")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    # Control characters other than tab would corrupt the entry text.
    for ch in line:
        if ord(ch) < 0x20 and ch != "\t":
            raise ValueError(f"line contains a control character: U+{ord(ch):04X}")


def main() -> int:
    check_line(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE)
    # Read it back: the file on disk must be byte-identical to the line.
    with open(path, "r", encoding="utf-8") as f:
        back = f.read()
    if back != LINE:
        raise ValueError("read-back mismatch: entry.txt does not match the line")
    print(f"wrote {path}: {len(LINE)} characters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
