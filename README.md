# UK VAT Invoice Auditor

A drop-in folder that turns a Claude project into an auditor for UK VAT sales invoices. Give it an invoice; it checks every particular the law requires, cites the exact provision for each finding, classifies severity, and reports what passed as well as what failed.

The standard it enforces ships **in the folder, verbatim and version-dated**: regulations 13, 14, 16 and 16A of the Value Added Tax Regulations 1995 (SI 1995/2518) and sections 3–4 of HMRC's Record keeping notice (VAT Notice 700/21) — see [reference/CATALOG.md](reference/CATALOG.md) for versions and access dates.

## Quick start

**Claude Code:** open a terminal in this folder and start a session — [CLAUDE.md](CLAUDE.md) wires the auditor up automatically. Then:

> Audit this invoice: *(paste the invoice text, or give a file path)*

**claude.ai project:** create a project, upload this folder to project knowledge, and set the project instructions to: *"You are the auditor defined in identity.md. Follow it exactly."*

To see it work immediately, run it on the included test invoices:

> Audit fixtures/broken-vat-total-in-euros.md

and compare the output against [examples.md](examples.md).

## What to feed it

One sales invoice at a time, as text: a pasted invoice body, a markdown file, or text extracted from a PDF. It audits the document in front of it — it does not need (and should not be given) your accounting records, customer lists, or anything else.

What comes back: a classification (full / simplified / retailer invoice), a check-by-check walk with one citation per line, findings graded **invalid-invoice / defective-field / advisory**, explicit passes, and a one-line verdict with counts. The format is specified in [rules.md](rules.md) and demonstrated in [examples.md](examples.md).

## What's in the folder

| File | Role |
|---|---|
| [identity.md](identity.md) | Who the auditor is — the entry point |
| [rules.md](rules.md) | Audit order, citation grammar, severity table, verdicts |
| [examples.md](examples.md) | Three worked audits showing the exact expected output |
| [reference/](reference/CATALOG.md) | The standard itself — verbatim, version-dated, one card per provision |
| [fixtures/](fixtures/EXPECTED.md) | Ten synthetic test invoices (2 compliant, 8 broken) with an answer sheet |
| [tools/check_citations.py](tools/check_citations.py) | Offline checker: every citation must resolve against reference/ |

Do **not** load the whole folder into context for an audit. The auditor reads [reference/CATALOG.md](reference/CATALOG.md) and opens only the card the invoice in front of it needs — a full invoice needs reg 14 and one notice section, nothing more. [fixtures/EXPECTED.md](fixtures/EXPECTED.md) is the answer sheet: keep it away from the auditor when testing it.

## Checking the citations

Every citation in this repo resolves mechanically against the shipped standard text. No network, no API key, Python 3 standard library only:

```bash
python3 tools/check_citations.py
```

Exit 0 means every citation in the auditor's files points at a provision that exists (and is not revoked) in reference/. A planted or corrupted citation fails the run with the file, line and reason. To prove the checker itself fires, run its self-test — a clean fixture must pass and a deliberately broken one must trigger all six planted defects:

```bash
python3 tools/check_citations.py --self-test
```

Both run in CI on every push ([.github/workflows/check.yml](.github/workflows/check.yml)).

## The standard's version pin

Legislation and guidance change. Each file in [reference/](reference/CATALOG.md) carries its source URL, the version it reproduces, and the date it was accessed (4 September 2026; no outstanding amendments were pending at that date). To refresh: re-fetch from the source URL, replace the text below the header, update the access date — never hand-edit the standard text.

## Limits

- It audits **UK VAT sales invoice particulars** — nothing else. VAT liability, rates, input tax recovery, penalties and planning are out of scope, and the auditor says so rather than answering.
- It cites only the provisions shipped in reference/. If an answer would need anything else, it names the gap instead of citing from memory.
- It does not verify VAT registration number checksums — a present-but-odd number is an advisory, not a verdict.
- Every invoice in [fixtures/](fixtures/EXPECTED.md) is synthetic. No real business, person, VAT number or bank detail appears anywhere in this repository.
- None of this is tax advice.

## Licence

The auditor's own files are MIT-licensed ([LICENSE](LICENSE)). The files in [reference/](reference/CATALOG.md) reproduce Crown copyright material — public sector information licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/), from [legislation.gov.uk](https://www.legislation.gov.uk/uksi/1995/2518) and [GOV.UK](https://www.gov.uk/guidance/record-keeping-for-vat-notice-70021), with source and access date stated in each file.

[AGENTS.md](AGENTS.md) is the engineering ruleset for agents *working on* this repo — users of the auditor never need it.
