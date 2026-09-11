#!/bin/sh
# audit.sh — run the auditor from a terminal, without opening a chat.
#
#   ./tools/audit.sh fixtures/broken-vat-total-in-euros.md      one invoice
#   ./tools/audit.sh fixtures/*.md                              a batch (rules.md §6)
#   ./tools/audit.sh invoice.md > audits/2026-09-11-acme.md     keep the report
#
# This is the auditor itself, so it does what the checkers in tools/ never
# do: it calls Claude. It needs the Claude Code CLI installed and signed in
# (https://claude.com/claude-code); nothing else. It runs from the repo
# root so CLAUDE.md loads and the auditor's own rules apply.
#
# The report goes to stdout. Nothing is saved unless you redirect it, and
# audits/ is git-ignored so a saved report of a real supplier invoice can
# never be committed by accident.

set -u
cd "$(dirname "$0")/.." || exit 1

if ! command -v claude >/dev/null 2>&1; then
    echo "audit.sh: the 'claude' command is not installed or not on PATH." >&2
    echo "Install Claude Code (https://claude.com/claude-code), sign in, and try again." >&2
    exit 1
fi

if [ "$#" -eq 0 ]; then
    echo "usage: ./tools/audit.sh INVOICE.md [INVOICE.md ...]" >&2
    echo "       one file audits that invoice; several files audit them as a batch (rules.md §6)" >&2
    exit 2
fi

for f in "$@"; do
    if [ ! -f "$f" ]; then
        echo "audit.sh: no such file: $f" >&2
        exit 1
    fi
done

if [ "$#" -eq 1 ]; then
    exec claude -p "Audit $1"
fi

exec claude -p "Audit every one of these invoices, one full audit each, then the summary table from rules.md §6: $*"
