#!/usr/bin/env python3
"""Prove the checkers are offline — not just claim it.

README.md and AGENTS.md both assert "no network, no API key, Python 3
standard library only" for tools/check_citations.py and
tools/check_arithmetic.py. This script turns that assertion into a
mechanical check: it looks for an actual `import` of a network-,
subprocess-, or hosted-LLM-capable module, or an actual call site against
one of those modules, in each checker's source — so a future edit that
quietly adds a network call (an "also verify against the live source"
shortcut, an update check, anything) cannot pass CI silently.

Matching real import statements and real call sites, not any occurrence of
the word anywhere in the file, means this script can safely scan its own
source too — its docstring and its own list of forbidden names are just
prose and a string literal to this scanner, not an import or a call site.

Runs offline, stdlib only, no API key.

Usage:
    python3 tools/check_no_network.py             # scan the checker scripts
    python3 tools/check_no_network.py --self-test  # prove the scan itself fires
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Module names whose mere import signals the offline guarantee may have
# been broken, plus dotted names whose *call* (not just mention) signals
# the same thing for modules that are otherwise legitimate (os, asyncio).
FORBIDDEN_IMPORTS = ["urllib", "requests", "httpx", "socket", "ftplib",
                     "smtplib", "telnetlib", "subprocess",
                     "openai", "anthropic"]
FORBIDDEN_CALLS = ["subprocess.run", "subprocess.call", "subprocess.Popen",
                    "os.system", "os.popen", "requests.get", "requests.post",
                    "urllib.request", "socket.socket", "asyncio.open_connection",
                    "http.client"]

IMPORT_RE = re.compile(
    r"^\s*(?:import|from)\s+(" + "|".join(re.escape(m) for m in FORBIDDEN_IMPORTS) + r")\b"
)
CALL_RE = re.compile(
    r"\b(" + "|".join(re.escape(c) for c in FORBIDDEN_CALLS) + r")\s*\("
)

CHECKED_FILES = ["check_citations.py", "check_arithmetic.py"]


def scan(path):
    """Return a list of (line_no, matched_name, line_text) for every real
    import or call site of a forbidden network/subprocess/LLM module —
    not for the word appearing in a docstring, comment, or string literal
    that merely talks about it."""
    hits = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        m = IMPORT_RE.match(line)
        if m:
            hits.append((i, m.group(1), line.strip()))
            continue
        m = CALL_RE.search(line)
        if m:
            hits.append((i, m.group(1), line.strip()))
    return hits


def run(filenames):
    return {name: scan(REPO / "tools" / name) for name in filenames
            if (REPO / "tools" / name).is_file()}


def self_test():
    """Prove the scanner fires: a clean testdata script must pass, and a
    script with a planted network import must fail by name."""
    testdata = REPO / "tools" / "testdata"
    clean = testdata / "clean-no-network.py"
    planted = testdata / "planted-network-call.py"
    failures = []

    clean_hits = scan(clean)
    if clean_hits:
        failures.append(f"clean testdata script flagged: {clean_hits}")

    planted_hits = scan(planted)
    if not planted_hits:
        failures.append("planted network-import testdata script raised nothing — scanner did not fire")
    elif not any(name == "requests" for _, name, _ in planted_hits):
        failures.append(f"planted script's 'requests' import was not the token caught: {planted_hits}")

    if failures:
        print("SELF-TEST FAILED — the no-network scanner can no longer be trusted:")
        for f in failures:
            print(f"  ✗ {f}")
        return 1
    print(f"SELF-TEST PASSED — clean testdata script: 0 hits; "
          f"planted testdata script: caught {planted_hits[0][1]!r} at line {planted_hits[0][0]}.")
    return 0


def main(argv):
    if argv and argv[0] == "--self-test":
        return self_test()

    results = run(CHECKED_FILES)
    # This scanner checks itself too — it must obey its own rule. Real
    # import/call matching means its own docstring and FORBIDDEN_* lists
    # (prose and string literals, not imports or calls) don't self-flag.
    results["check_no_network.py"] = scan(Path(__file__))

    total_hits = sum(len(h) for h in results.values())
    if total_hits:
        print(f"NO-NETWORK CHECK FAILED — {total_hits} forbidden import/call found:")
        for name, hits in results.items():
            for line_no, token, text in hits:
                print(f"  ✗ tools/{name}:{line_no}  forbidden {token!r} — {text}")
        return 1
    checked = ", ".join(CHECKED_FILES)
    print(f"NO-NETWORK CHECK PASSED — {checked} and this scanner itself contain no "
          f"network, subprocess, or hosted-LLM import or call. The offline claim is proven, not asserted.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
