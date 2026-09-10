#!/usr/bin/env python3
"""Verify every reference/ file against its recorded SHA-256 — offline.

This is integrity, not freshness. It proves the standard text sitting in
this checkout is byte-identical to what was there when the hash was
recorded; it says nothing about whether the live source has since changed
(that is tools/check_freshness.sh's job, and it needs the network to do it).
A hash mismatch means the text under this auditor moved without anyone
updating the manifest — regenerating the hash is not a fix for that unless
the change was a deliberate, disclosed re-fetch.

Runs offline, stdlib only, no API key.

Usage:
    python3 tools/check_reference_integrity.py             # verify against the manifest
    python3 tools/check_reference_integrity.py --write      # (re)write the manifest
    python3 tools/check_reference_integrity.py --self-test  # prove the check fires
"""
import hashlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REFERENCE = REPO / "reference"
MANIFEST = REFERENCE / "MANIFEST.md"

MANIFEST_LINE = re.compile(r"^([0-9a-f]{64})  (\S+)$")


def sha256_of(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def current_hashes(reference_dir):
    return {
        p.name: sha256_of(p)
        for p in sorted(reference_dir.glob("*.md"))
        if p.name not in ("CATALOG.md", "MANIFEST.md")
    }


def read_manifest(path):
    if not path.is_file():
        return None
    hashes = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = MANIFEST_LINE.match(line)
        if m:
            hashes[m.group(2)] = m.group(1)
    return hashes


def write_manifest(path, hashes):
    lines = [
        "# Reference integrity manifest",
        "",
        "SHA-256 of every file in reference/ (except this one and CATALOG.md), recorded",
        "at the access dates stated in each file's own header. Verify with:",
        "",
        "```bash",
        "python3 tools/check_reference_integrity.py",
        "```",
        "",
        "A mismatch means the text changed without the manifest being regenerated on",
        "purpose. Regenerating with `--write` after a deliberate re-fetch is correct;",
        "regenerating to silence an unexplained mismatch defeats the entire point.",
        "",
        "```",
    ]
    for name, h in sorted(hashes.items()):
        lines.append(f"{h}  {name}")
    lines.append("```")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def diff(expected, actual):
    problems = []
    for name in sorted(set(expected) | set(actual)):
        if name not in actual:
            problems.append(f"{name}: in the manifest but the file is missing")
        elif name not in expected:
            problems.append(f"{name}: exists but is not in the manifest — re-write it deliberately")
        elif expected[name] != actual[name]:
            problems.append(f"{name}: hash mismatch — expected {expected[name][:12]}…, got {actual[name][:12]}…")
    return problems


def self_test():
    """Prove the check fires: a manifest matching its files passes; a
    manifest with one deliberately wrong hash fails by name."""
    testdata = REPO / "tools" / "testdata" / "integrity"
    clean_dir = testdata / "clean"
    broken_dir = testdata / "broken"
    failures = []

    clean_manifest = read_manifest(clean_dir / "MANIFEST.md")
    clean_actual = current_hashes(clean_dir)
    clean_problems = diff(clean_manifest, clean_actual)
    if clean_problems:
        failures.append(f"clean testdata raised problems it shouldn't have: {clean_problems}")

    broken_manifest = read_manifest(broken_dir / "MANIFEST.md")
    broken_actual = current_hashes(broken_dir)
    broken_problems = diff(broken_manifest, broken_actual)
    if not broken_problems:
        failures.append("broken testdata (planted wrong hash) reported no mismatch — check did not fire")

    if failures:
        print("SELF-TEST FAILED — the integrity check can no longer be trusted:")
        for f in failures:
            print(f"  ✗ {f}")
        return 1
    print(f"SELF-TEST PASSED — clean manifest: 0 mismatches; "
          f"broken manifest: caught {broken_problems[0]}")
    return 0


def main(argv):
    if argv and argv[0] == "--self-test":
        return self_test()

    actual = current_hashes(REFERENCE)

    if argv and argv[0] == "--write":
        write_manifest(MANIFEST, actual)
        print(f"wrote {MANIFEST.relative_to(REPO)} ({len(actual)} file(s))")
        return 0

    expected = read_manifest(MANIFEST)
    if expected is None:
        print(f"REFERENCE INTEGRITY CHECK FAILED — {MANIFEST.relative_to(REPO)} does not exist; "
              f"run with --write to create it")
        return 1

    problems = diff(expected, actual)
    if problems:
        print(f"REFERENCE INTEGRITY CHECK FAILED — {len(problems)} problem(s):")
        for p in problems:
            print(f"  ✗ {p}")
        return 1
    print(f"REFERENCE INTEGRITY CHECK PASSED — {len(actual)} reference file(s) match their recorded SHA-256.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
