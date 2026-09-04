#!/usr/bin/env python3
"""Validate the auditor's files against the text in reference/.

Two gates, both offline, stdlib only, no API key:

1. Citations — every bracketed citation must resolve to a provision that
   exists (and is not revoked) in reference/.
2. Quotes — every double-quoted span in the auditor's own files must appear
   verbatim (after whitespace/punctuation normalisation) in a fixture invoice
   or in the shipped standard, so a fabricated quote fails mechanically no
   matter how convincing it reads.

Exit 0 when both gates pass; exit 1 with one line per failure otherwise.

Usage:
    python3 tools/check_citations.py               # check the repo's own files
    python3 tools/check_citations.py FILE [FILE…]  # citation-check specific files
    python3 tools/check_citations.py --self-test   # prove both gates fire
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

# Quote-grounding scope: the files whose double-quoted spans must all be
# grounded. README/AGENTS quote coined instructions, so they stay out.
QUOTE_FILES = ["identity.md", "rules.md", "examples.md", "docs/cold-walk.md"]
QUOTE_SPAN = re.compile(r"\"([^\"]{4,160})\"")

# What neither gate checks — printed with every result so a clean run never
# overclaims.
LIMITS = ("Not checked by this tool: paraphrases of the standard (only quoted "
          "spans and citations), VAT number checksums, and whether a severity "
          "call is legally right — those are the auditor's and the reviewer's job.")


def normalise(text):
    text = text.lower()
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("*", "").replace("`", "").replace(",", "")
    return re.sub(r"\s+", " ", text)


def quote_sources():
    """The texts a quoted span may legitimately come from: the fixture
    invoices and the shipped standard."""
    sources = []
    for path in sorted((REPO / "fixtures").glob("*.md")):
        if path.name != "EXPECTED.md":
            sources.append(normalise(path.read_text(encoding="utf-8")))
    for path in sorted(REFERENCE.glob("*.md")):
        sources.append(normalise(path.read_text(encoding="utf-8")))
    return sources


def check_quotes(path, sources):
    errors = []
    text = path.read_text(encoding="utf-8")
    for m in QUOTE_SPAN.finditer(text):
        span = m.group(1)
        if any(normalise(span) in s for s in sources):
            continue
        line_no = text.count("\n", 0, m.start()) + 1
        short = " ".join(span.split())
        if len(short) > 60:
            short = short[:57] + "..."
        errors.append((path, line_no, f'ungrounded quote "{short}" — appears in no fixture and no reference/ card'))
    return errors


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

    sources = quote_sources()

    clean_errors, clean_n = check_file(clean)
    clean_errors.extend(check_quotes(clean, sources))
    if clean_errors:
        failures.append(f"clean file raised {len(clean_errors)} error(s): {clean_errors}")
    if clean_n == 0:
        failures.append("clean file contained no citations — self-test is vacuous")
    if not QUOTE_SPAN.search(clean.read_text(encoding="utf-8")):
        failures.append("clean file contained no quoted span — quote gate untested on honest prose")

    broken_errors, _ = check_file(broken)
    broken_errors.extend(check_quotes(broken, sources))
    planted = [
        "reg 14 has no element (z)",
        "regulation 15 is not shipped",
        "§9.9 is not in the shipped sections",
        "reg 14(f) is revoked",
        "reg 14(k) is revoked",
        "malformed citation",
        "ungrounded quote",
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
    print(f"SELF-TEST PASSED — clean file: {clean_n} citations and its quoted span, 0 errors; "
          f"broken file: all {len(planted)} planted defect classes caught.")
    return 0


def main(argv):
    if argv and argv[0] == "--self-test":
        return self_test()
    explicit = bool(argv)
    files = [Path(a) for a in argv] if argv else [f for f in DEFAULT_FILES if f.is_file()]
    errors, total = run(files)
    quotes = 0
    if not explicit:  # quote-grounding is a repo invariant, not a per-file ask
        sources = quote_sources()
        for name in QUOTE_FILES:
            path = REPO / name
            if path.is_file():
                errors.extend(check_quotes(path, sources))
                quotes += len(QUOTE_SPAN.findall(path.read_text(encoding="utf-8")))
    if errors:
        print(f"CHECK FAILED — {len(errors)} problem(s) ({total} citations, {quotes} quoted spans examined):")
        for path, line_no, msg in errors:
            try:
                rel = path.relative_to(REPO)
            except ValueError:
                rel = path
            print(f"  ✗ {rel}:{line_no}  {msg}")
        print(LIMITS)
        return 1
    if explicit:
        print(f"CITATION CHECK PASSED — {total} citations across {len(files)} file(s) all resolve against reference/.")
    else:
        print(f"CHECK PASSED — {total} citations resolve against reference/ and all "
              f"{quotes} quoted spans in {len(QUOTE_FILES)} auditor file(s) are grounded "
              f"in a fixture or the standard.")
    print(LIMITS)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
