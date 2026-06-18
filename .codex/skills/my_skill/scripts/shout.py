#!/usr/bin/env python3
"""Print provided text in uppercase."""

from __future__ import annotations

import sys


def main() -> int:
    text = " ".join(sys.argv[1:]).strip()
    if not text:
        text = sys.stdin.read().strip()

    if text in {"stop", "quit"}:
        print("Stopped.")
        return 0

    print(text.upper())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
