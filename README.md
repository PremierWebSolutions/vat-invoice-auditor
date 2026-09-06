# UK VAT Invoice Auditor

A drop-in folder that turns a Claude project into an auditor for UK VAT sales invoices. Give it an invoice and it checks every particular the law requires, cites the exact provision for each finding, classifies severity, and reports what passed as well as what failed.

The standard it enforces ships in the folder, verbatim and version-dated: regulations 13, 14, 16 and 16A of the Value Added Tax Regulations 1995 (SI 1995/2518) and sections 3 and 4 of HMRC's Record keeping notice (VAT Notice 700/21). See [reference/CATALOG.md](reference/CATALOG.md) for versions and access dates.

## Quick start

**Claude Code:** open a terminal in this folder and start a session. [CLAUDE.md](CLAUDE.md) wires the auditor up automatically. Then:

> Audit this invoice: *(paste the invoice text, or give a file path)*

**claude.ai project:** create a project, upload this folder to project knowledge, and set the project instructions to: *"You are the auditor defined in identity.md. Follow it exactly."*

To see it work immediately, run it on one of the included test invoices:

> Audit fixtures/broken-vat-total-in-euros.md

and compare the output against [examples.md](examples.md).

## What to feed it

One sales invoice at a time, as text: a pasted invoice body, a markdown file, or text extracted from a PDF. It audits the document in front of it. It does not need (and should not be given) your accounting records, customer lists, or anything else.

What comes back: a classification (full, simplified or retailer invoice), a check-by-check walk with one citation per line, findings graded **invalid-invoice / defective-field / advisory**, explicit passes, and a one-line verdict with counts. The format is specified in [rules.md](rules.md) and demonstrated in [examples.md](examples.md).

## What's in the folder

| File | Role |
|---|---|
| [identity.md](identity.md) | Who the auditor is: the entry point |
| [rules.md](rules.md) | Audit order, citation grammar, severity table, verdicts |
| [examples.md](examples.md) | Three worked audits showing the exact expected output |
| [reference/](reference/CATALOG.md) | The standard itself, verbatim and version-dated, one card per provision |
| [fixtures/](fixtures/) | Ten synthetic test invoices (2 compliant, 8 broken) — inputs only, no answers |
| [tools/check_citations.py](tools/check_citations.py) | Offline checker: every citation and quote must resolve against reference/ or a fixture |
| [tools/check_arithmetic.py](tools/check_arithmetic.py) | Offline checker: every fixture's net/VAT/total arithmetic is recomputed from its own numbers |

The drop-in unit is the five things above the line: identity, rules, examples, reference, and the fixtures as plain invoice text. **The answer key is not in that folder.** It lives in [judge-answer-key/](judge-answer-key/EXPECTED.md), a sibling directory the auditor is never pointed at and a real production setup never uploads — separated by folder position, not by an instruction the auditor is trusted to police itself. Do not load the whole repo into context for an audit either way: the auditor reads [reference/CATALOG.md](reference/CATALOG.md) and opens only the card the invoice in front of it needs; a full invoice needs reg 14 and one notice section, nothing more. If you set the folder up for real production use rather than testing, leave `fixtures/`, `judge-answer-key/`, `tools/` and `docs/` out entirely — they exist to test and evidence the auditor, not to audit anything.

## Checking the citations, quotes and arithmetic

Three mechanical gates guard the auditor's files, so nothing in it is trusted on the model's say-so alone. No network, no API key, Python 3 standard library only:

```bash
python3 tools/check_citations.py
python3 tools/check_arithmetic.py
```

`check_citations.py` checks two things. Every citation points at a provision that exists (and is not revoked) in reference/. And every double-quoted span in the auditor's files appears verbatim in a fixture invoice or in the shipped standard — a fabricated quote fails mechanically no matter how convincing it reads. `check_arithmetic.py` recomputes every fixture invoice's line items, VAT and totals from its own stated numbers — the script does the sums, so a plausible-looking "recomputes exactly" claim is either true or the run fails, and an invoice shape the parser doesn't recognise is a hard failure rather than a silent skip. Any kind of plant fails its run with the file, line and reason, and both tools print what they do not check. To prove the gates themselves fire, run each self-test: a clean fixture must pass and a deliberately broken one must trigger every planted defect.

```bash
python3 tools/check_citations.py --self-test
python3 tools/check_arithmetic.py --self-test
```

All four run in CI on every push ([.github/workflows/check.yml](.github/workflows/check.yml)).

## The standard's version pin

Legislation and guidance change. Each file in [reference/](reference/CATALOG.md) carries its source URL, the version it reproduces, and the date it was accessed (4 September 2026; no outstanding amendments were pending at that date). To refresh: re-fetch from the source URL, replace the text below the header, and update the access date. Never hand-edit the standard text.

## Limits

- It audits UK VAT sales invoice particulars and nothing else. VAT liability, rates, input tax recovery, penalties and planning are out of scope, and the auditor says so rather than answering.
- It cites only the provisions shipped in reference/. If an answer would need anything else, it names the gap instead of citing from memory.
- It does not verify VAT registration number checksums; a present-but-odd number is an advisory, not a verdict.
- Every invoice in [fixtures/](fixtures/) is synthetic. No real business, person, VAT number or bank detail appears anywhere in this repository.
- None of this is tax advice.

## Receipts

Two evidence files, both outside the drop-in folder: [docs/cold-walk.md](docs/cold-walk.md) is a fresh session using the auditor with no prior context, catching a planted defect and correcting the answer sheet when its own reading was better than mine. [docs/refusal-under-pressure.md](docs/refusal-under-pressure.md) is the same kind of session run through four disguised requests to skip the audit — a yes/no shortcut, a request to draft a replacement invoice, a request to certify compliance under deadline pressure, a request to skip straight to a ranking — with the full transcript published, not just the claim that it refused correctly.

## Licence

The auditor's own files are MIT-licensed ([LICENSE](LICENSE)). The files in [reference/](reference/CATALOG.md) reproduce Crown copyright material — public sector information licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/), from [legislation.gov.uk](https://www.legislation.gov.uk/uksi/1995/2518) and [GOV.UK](https://www.gov.uk/guidance/record-keeping-for-vat-notice-70021), with source and access date stated in each file.

[AGENTS.md](AGENTS.md) is the engineering ruleset for agents working on this repo. Users of the auditor never need it.
