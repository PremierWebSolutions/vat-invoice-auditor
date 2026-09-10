#!/usr/bin/env python3
"""Self-test fixture — a checker script with no network or LLM calls."""
import re
import sys
from pathlib import Path
from decimal import Decimal

REPO = Path(__file__).resolve().parent


def add(a, b):
    return Decimal(a) + Decimal(b)


def main(argv):
    print("clean, offline, stdlib only")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
