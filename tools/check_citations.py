#!/usr/bin/env python3
"""Validate every citation in the auditor's files against the text in reference/.

Runs offline, stdlib only, no API key. Exit 0 when every citation resolves;
exit 1 with one line per failure otherwise.

Usage:
    python3 tools/check_citations.py               # check the repo's own files
    python3 tools/check_citations.py FILE [FILE…]  # check specific files
    python3 tools/check_citations.py --self-test   # prove the checker fires
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REFERENCE = REPO / "reference"

# The strict citation grammar from rules.md §2. Anything that resembles a
# citation but fails this grammar is reported as malformed, not ignored.
STRICT = re.compile(r"\[((?:reg [0-9]+[A-Z]?(?:\([0-9a-zA-Z]+\))*|700/21 §[0-9]+(?:\.[0-9]+)?)(?:; (?:reg [0-9]+[A-Z]?(?:\([0-9a-zA-Z]+\))*|700/21 §[0-9]+(?:\.[0-9]+)?))*)\]")
LOOSE = re.compile(r"\[[^\[\]]*(?:\breg\b|700/21)[^\[\]]*\]", re.IGNORECASE)
REG_PART = re.compile(r"reg ([0-9]+[A-Z]?)((?:\([0-9a-zA-Z]+\))*)$")
NOTICE_PART = re.compile(r"700/21 §([0-9]+(?:\.[0-9]+)?)$")

# Default scan set: every auditor-authored markdown file. reference/ is the
# standard itself and tools/testdata holds deliberately broken input.
DEFAULT_FILES = (sorted(REPO.glob("*.md")) + [REPO / "fixtures" / "EXPECTED.md"]
                 + sorted((REPO / "docs").glob("*.md")))


def reg_file(num):
    return REFERENCE / f"vat-regulations-1995-reg-{num}.md"


def check_reg(num, elements):
    """A regulation citation resolves when its file exists and each bracketed
    element appears at the start of a line, in order, after the previous one."""
    path = reg_file(num)
    if not path.is_file():
        return f"regulation {num} is not shipped in reference/"
    lines = path.read_text(encoding="utf-8").splitlines()
    pos = 0
    for el in elements:
        for i in range(pos, len(lines)):
            if lines[i].startswith(f"({el})"):
                body = lines[i][len(el) + 2:].strip()
                if body and set(body) <= set(". "):
                    return f"reg {num}({el}) is revoked — the reference text is blank at source"
                pos = i + 1
                break
        else:
            return f"reg {num} has no element ({el}) at this position in reference/"
    return None


def check_notice(section):
    """A notice citation resolves when a heading numbered `section` exists in
    the shipped sections of Notice 700/21."""
    path = REFERENCE / "vat-notice-700-21-invoicing.md"
    if not path.is_file():
        return "Notice 700/21 is not shipped in reference/"
    pattern = re.compile(rf"^#+ {re.escape(section)}\.?\s")
    for line in path.read_text(encoding="utf-8").splitlines():
        if pattern.match(line):
            return None
    return f"Notice 700/21 §{section} is not in the shipped sections (3–4) in reference/"


def check_file(path):
    errors = []
    text = path.read_text(encoding="utf-8")
    strict_spans = []
    for m in STRICT.finditer(text):
        strict_spans.append(m.span())
        line_no = text.count("\n", 0, m.start()) + 1
        for part in m.group(1).split("; "):
            rm = REG_PART.match(part)
            nm = NOTICE_PART.match(part)
            if rm:
                elements = re.findall(r"\(([0-9a-zA-Z]+)\)", rm.group(2))
                problem = check_reg(rm.group(1), elements)
            elif nm:
                problem = check_notice(nm.group(1))
            else:  # unreachable given the grammar, kept as a guard
                problem = f"unparseable citation part {part!r}"
            if problem:
                errors.append((path, line_no, f"[{part}] — {problem}"))
    for m in LOOSE.finditer(text):
        if not any(s <= m.start() and m.end() <= e for s, e in strict_spans):
            line_no = text.count("\n", 0, m.start()) + 1
            errors.append((path, line_no, f"{m.group(0)} — malformed citation (does not match the grammar in rules.md §2)"))
    return errors, len(strict_spans)


def run(files):
    all_errors, total = [], 0
    for path in files:
        errors, n = check_file(path)
        all_errors.extend(errors)
        total += n
    return all_errors, total


def self_test():
    """Prove the checker fires: the clean testdata file must produce zero
    errors and the broken one must produce every planted failure."""
    clean = REPO / "tools" / "testdata" / "clean-citations.md"
    broken = REPO / "tools" / "testdata" / "broken-citations.md"
    failures = []

    clean_errors, clean_n = check_file(clean)
    if clean_errors:
        failures.append(f"clean file raised {len(clean_errors)} error(s): {clean_errors}")
    if clean_n == 0:
        failures.append("clean file contained no citations — self-test is vacuous")

    broken_errors, _ = check_file(broken)
    planted = [
        "reg 14 has no element (z)",
        "regulation 15 is not shipped",
        "§9.9 is not in the shipped sections",
        "reg 14(f) is revoked",
        "reg 14(k) is revoked",
        "malformed citation",
    ]
    messages = " | ".join(e[2] for e in broken_errors)
    for expect in planted:
        if expect not in messages:
            failures.append(f"broken file did NOT trigger: {expect!r}")

    if failures:
        print("SELF-TEST FAILED — the checker can no longer be trusted:")
        for f in failures:
            print(f"  ✗ {f}")
        return 1
    print(f"SELF-TEST PASSED — clean file: {clean_n} citations, 0 errors; "
          f"broken file: all {len(planted)} planted defects caught.")
    return 0


def main(argv):
    if argv and argv[0] == "--self-test":
        return self_test()
    files = [Path(a) for a in argv] if argv else [f for f in DEFAULT_FILES if f.is_file()]
    errors, total = run(files)
    if errors:
        print(f"CITATION CHECK FAILED — {len(errors)} problem(s) in {total} citation(s):")
        for path, line_no, msg in errors:
            rel = path.relative_to(REPO) if path.is_relative_to(REPO) else path
            print(f"  ✗ {rel}:{line_no}  {msg}")
        return 1
    print(f"CITATION CHECK PASSED — {total} citations across {len(files)} file(s) all resolve against reference/.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
