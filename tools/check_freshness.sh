#!/bin/sh
# check_freshness.sh
#
# The one part of this repo that touches the network. Everything else — the
# auditor, check_citations.py, check_arithmetic.py, check_no_network.py — is
# offline by design and by check_no_network.py's own proof. This script is
# deliberately outside that guarantee: it exists to catch the standard itself
# moving under the reference/ text this repo ships.
#
# For every source vendored in reference/ it does two things:
#   1. Fetches the source URL and checks the HTTP status. A non-200 is how a
#      withdrawn or moved page announces itself.
#   2. Greps the live page for a canary: a short exact phrase taken from our
#      vendored copy. If the canary is gone, the publisher changed the text
#      and our copy has gone stale without anything failing loudly.
#
# A vendored standard that quietly drifts from its source is worse than no
# standard at all, because a clean audit then means nothing.
#
#   ./tools/check_freshness.sh          check everything
#   ./tools/check_freshness.sh -q       only print problems
#
# Needs curl and nothing else. Not run in CI (see AGENTS.md) — run it by hand
# before relying on this auditor for anything that matters, and periodically
# after that. A failure here means re-fetch the source, re-run
# tools/check_citations.py and tools/check_arithmetic.py, and update the
# access date in the affected reference/ file's header — never hand-edit the
# vendored text itself.

set -u
cd "$(dirname "$0")/.." || exit 1

QUIET=0
[ "${1:-}" = "-q" ] && QUIET=1
say() { [ "$QUIET" -eq 0 ] && echo "$@"; return 0; }

UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
ok=0; stale=0; unreachable=0

# file : source URL : canary phrase (must appear verbatim, mid-sentence, in
# the live page — chosen from the operative text itself, not the header).
#
# Pick canaries from plain, unamended stretches of text. legislation.gov.uk
# marks up amended passages with editorial change-delimiters and footnote
# links ("[F1...]") that survive simple tag-stripping as literal bracket and
# reference-code text — reference/vat-regulations-1995-reg-16.md's own
# extraction already omits these (see its header), so a canary drawn from
# inside one will report a false "stale" against a page that has not
# actually changed. Confirmed against reg 16's live page: a canary spanning
# "does not exceed £250" false-fails because that figure sits inside a
# change-marked clause; "shall not be required to provide a VAT invoice",
# a few words earlier in the same provision, does not and is the canary
# used below.
SOURCES='
reference/vat-regulations-1995-reg-13.md|https://www.legislation.gov.uk/uksi/1995/2518/regulation/13|makes a taxable supply in the United Kingdom to a taxable person
reference/vat-regulations-1995-reg-14.md|https://www.legislation.gov.uk/uksi/1995/2518/regulation/14|a sequential number based on one or more series which uniquely identifies the document
reference/vat-regulations-1995-reg-16.md|https://www.legislation.gov.uk/uksi/1995/2518/regulation/16|shall not be required to provide a VAT invoice
reference/vat-regulations-1995-reg-16A.md|https://www.legislation.gov.uk/uksi/1995/2518/regulation/16A|the consideration for a supply does not exceed £250
reference/vat-notice-700-21-invoicing.md|https://www.gov.uk/guidance/record-keeping-for-vat-notice-70021|a sequential number based on one or more series which uniquely identifies the document
'

say "Checking every vendored standard in reference/ against its live source."
say ""

echo "$SOURCES" | while IFS='|' read -r file url canary; do
    [ -z "$file" ] && continue
    if [ ! -f "$file" ]; then
        say "  ? $file — file not found, skipping"
        continue
    fi

    body=$(curl -s -L -A "$UA" -w '\n__STATUS__:%{http_code}' "$url" 2>/dev/null)
    status=$(echo "$body" | grep -o '__STATUS__:[0-9]*$' | cut -d: -f2)

    if [ -z "$status" ] || [ "$status" = "000" ]; then
        say "  ✗ UNREACHABLE  $file — could not fetch $url"
        unreachable=$((unreachable + 1))
        continue
    fi
    if [ "$status" != "200" ]; then
        say "  ✗ HTTP $status  $file — $url is no longer serving 200; the source may have moved or been withdrawn"
        stale=$((stale + 1))
        continue
    fi
    # legislation.gov.uk wraps amended figures in change-marker spans
    # ("does not exceed <span...>[</span><a...>£250") that split a canary
    # phrase mid-string even when the wording is unchanged. Strip tags
    # before matching, the same way the vendored text itself was extracted
    # (see reference/*.md headers) — a plain grep against raw HTML gives
    # false "stale" reports on pages that haven't actually changed.
    stripped=$(echo "$body" | sed -e 's/<[^>]*>//g' -e 's/&#160;/ /g' -e 's/&nbsp;/ /g')
    if echo "$stripped" | tr -s '[:space:]' ' ' | grep -qF "$canary"; then
        say "  ok  $file — HTTP 200, canary phrase present"
        ok=$((ok + 1))
    else
        say "  ✗ CANARY MISSING  $file — $url returns 200 but no longer contains: \"$canary\""
        say "      the publisher changed this page; re-fetch and re-check the vendored text"
        stale=$((stale + 1))
    fi
done

say ""
say "Note: counts above are per-subshell (the while loop runs in a pipe) — read the"
say "per-line result, not a summary total. Any ✗ line is a real problem to act on."
