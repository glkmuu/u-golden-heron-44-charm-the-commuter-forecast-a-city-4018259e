#!/usr/bin/env python3
"""Charm the Commuter: Forecast a City That Isn't.

Reads entry.txt (one line of weather, at most 140 characters, for a city
that does not exist), validates the gate, and writes it byte-for-byte to
$MAKEFUN_OUTPUT_DIR/entry.txt.

Python 3.13, standard library only.
"""

import os
import sys

MAX_CHARS = 140


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.txt")
    with open(src, "r", encoding="utf-8") as fh:
        text = fh.read()

    # The gate: UTF-8 text of 1 to 140 characters, not only white space,
    # and a single line.
    if not text or not text.strip():
        print("entry is empty or only whitespace", file=sys.stderr)
        return 1
    if "\n" in text.rstrip("\n") or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    line = text.rstrip("\n")
    if len(line) > MAX_CHARS:
        print(f"entry is {len(line)} characters, over the {MAX_CHARS} limit",
              file=sys.stderr)
        return 1
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in line):
        print("entry contains control characters", file=sys.stderr)
        return 1
    if line != line.strip():
        print("entry has leading or trailing whitespace", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
