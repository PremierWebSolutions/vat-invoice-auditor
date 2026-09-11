# UK VAT Invoice Auditor

A drop-in folder that turns a Claude project into an auditor for UK VAT sales invoices. Give it an invoice and it checks every particular the law requires, cites the exact provision for each finding, classifies severity, and reports what passed as well as what failed.

The standard it enforces ships in the folder, verbatim and version-dated: regulations 13, 14, 16 and 16A of the Value Added Tax Regulations 1995 (SI 1995/2518) and sections 3 and 4 of HMRC's Record keeping notice (VAT Notice 700/21). See [reference/CATALOG.md](reference/CATALOG.md) for versions and access dates.

## Audit your own invoices

You need the [Claude Code](https://claude.com/claude-code) command line installed and signed in, and nothing else.

1. Put each invoice you want checked in the [invoices/](invoices/) folder. A PDF is fine (most supplier invoices are PDFs), and so is a plain text file (`.md` or `.txt`). The one exception is a PDF that's just a scan or photo of paper, with no real text in it; type those into a text file first.
2. From this folder, run:

```bash
./tools/audit.sh invoices/*.pdf
```

Each invoice gets its own full audit, followed by a summary table. Everything you put in `invoices/` stays on your machine: that folder is git-ignored, so a real supplier's invoice is never committed to the repo. To keep a copy of the report, redirect it: `./tools/audit.sh invoices/*.pdf > audits/2026-09-11.md` (`audits/` is git-ignored too). Four ready-made sample PDFs (`SAMPLE-1` to `SAMPLE-4`) sit in the folder so you can try it before adding your own — a clean invoice, one that fails, a statement that isn't a VAT invoice, and a simplified receipt.

## See it work first

The tool ships with ten made-up test invoices in [fixtures/](fixtures/) so you can watch it run before feeding it anything real. A correct invoice:

```bash
./tools/audit.sh fixtures/compliant-full-invoice.md
```

One with a fault (a missing supplier VAT number):

```bash
./tools/audit.sh fixtures/broken-missing-vat-number.md
```

All ten at once, as a batch:

```bash
./tools/audit.sh fixtures/*.md
```

Compare any of these against [examples.md](examples.md), which walks three of them through by hand.

## Quick start in a chat

**Claude Code:** open a terminal in this folder, run `claude`, and paste an invoice or name a file: `Audit invoices/that-invoice.md`. [CLAUDE.md](CLAUDE.md) wires the auditor up automatically, and if your first message isn't an audit request it replies with plain instructions rather than doing anything else.

**claude.ai project:** create a project, upload this folder to project knowledge, and set the project instructions to: *"You are the auditor defined in identity.md. Follow it exactly."* Then paste an invoice.

## What to feed it

One sales invoice at a time: a PDF, a markdown or text file, or an invoice pasted straight into the chat. It reads the text inside a PDF, so a software-produced invoice works as-is; only a scan or photo with no text layer needs typing out first. It audits the document in front of it. It does not need (and should not be given) your accounting records, customer lists, or anything else.

What comes back: a classification (full, simplified or retailer invoice), a check-by-check walk with one citation per line, findings graded **invalid-invoice / defective-field / advisory**, explicit passes, and a one-line verdict with counts. The format is specified in [rules.md](rules.md) and demonstrated in [examples.md](examples.md).

## Using it in a bookkeeping workflow

Where this earns its keep is **incoming purchase invoices**: the supplier invoices a bookkeeper processes and reclaims input tax on, which nobody in-house had a hand in producing. Your own outgoing invoices are better policed by your invoicing software, and the one thing that matters most for them (no gaps or repeats across the whole numbered run) needs the full sales ledger, which a document-by-document auditor never sees. This tool audits documents; it is not a ledger check.

For a stack of invoices, hand it the batch in one request:

> Audit every invoice in *(folder, or paste them all)*, one full audit each, then the summary table.

[rules.md §6](rules.md) governs what happens next: each invoice gets its complete audit, nothing found in one is allowed to colour another, and a summary table (verdict, counts, headline finding per invoice) comes last, as an index to the audits, never a substitute for them. Two checks only exist at batch level and are reported there: the same reference number on two documents, and one supplier carrying two different VAT registration numbers. In a chat, nothing is written to disk and the audits are the session's output, so copy what you need into your working papers; from the terminal, `./tools/audit.sh fixtures/*.md > audits/today.md` keeps the whole batch report in one git-ignored file.

## What it checks against, exactly

Not HMRC's VAT material in general, but one deliberately narrow slice of it, chosen because it is the whole of the law on what a VAT invoice must say and nothing else:

- **Regulations 13, 14, 16 and 16A of the Value Added Tax Regulations 1995 (SI 1995/2518)**: who must issue a VAT invoice, the particulars a full invoice must state (reg 14(1)(a)–(p)), and the £250 relaxations for retailers' and simplified invoices. Fetched from legislation.gov.uk's consolidated text.
- **VAT Notice 700/21, sections 3 and 4 only**: HMRC's operational reading of those regulations. The rest of that notice (record keeping, VAT accounts, Making Tax Digital) is out of scope and not shipped.

That is the entire standard. VAT liability, rates, exemption, input tax recovery, penalties, the construction reverse charge in detail (Notice 735), self-billing (Notice 700/62) and the main VAT guide (Notice 700) are **not** in the folder, and [identity.md](identity.md) forbids the auditor from citing any of them from memory: if an answer would need them, it names the gap and stops. The mapping from those provisions to checks (the audit order, the severity of each defect, the verdict lines) is in [rules.md](rules.md) and is this repo's own work, not HMRC's; the severity judgments are drafted by the author and flagged for a practising accountant's review in [docs/review-notes.md](docs/review-notes.md).

## What's in the folder

| File | Role |
|---|---|
| [CLAUDE.md](CLAUDE.md) | What Claude Code loads first: routes to the auditor and answers a stray first message with the usage line |
| [identity.md](identity.md) | Who the auditor is and what it enforces; where CLAUDE.md sends every audit |
| [rules.md](rules.md) | Audit order, citation grammar, severity table, verdicts |
| [examples.md](examples.md) | Three worked audits showing the exact expected output |
| [reference/](reference/CATALOG.md) | The standard itself, verbatim and version-dated, one card per provision |
| [fixtures/](fixtures/) | Ten synthetic test invoices (2 compliant, 8 broken); inputs only, no answers |
| [tools/check_citations.py](tools/check_citations.py) | Offline checker: every citation and quote must resolve against reference/ or a fixture |
| [tools/check_arithmetic.py](tools/check_arithmetic.py) | Offline checker: every fixture's net/VAT/total arithmetic is recomputed from its own numbers |
| [tools/check_no_network.py](tools/check_no_network.py) | Offline checker: proves the checkers above make no network, subprocess or hosted-LLM call |
| [tools/check_reference_integrity.py](tools/check_reference_integrity.py) | Offline checker: every reference/ file matches its recorded SHA-256 ([reference/MANIFEST.md](reference/MANIFEST.md)) |
| [tools/check_freshness.sh](tools/check_freshness.sh) | The one checker that touches the network: tests each vendored standard against its live source (not run in CI; see below) |
| [tools/audit.sh](tools/audit.sh) | The runner: audits one file or a batch from the terminal by calling the Claude CLI |

The drop-in unit is the five things above the line: identity, rules, examples, reference, and the fixtures as plain invoice text. **The answer key is not in that folder.** It lives in [judge-answer-key/](judge-answer-key/EXPECTED.md), a sibling directory the auditor is never pointed at and a real production setup never uploads, separated by folder position, not by an instruction the auditor is trusted to police itself. Do not load the whole repo into context for an audit either way: the auditor reads [reference/CATALOG.md](reference/CATALOG.md) and opens only the card the invoice in front of it needs; a full invoice needs reg 14 and one notice section, nothing more. If you set the folder up for real production use rather than testing, leave `fixtures/`, `judge-answer-key/`, `tools/` and `docs/` out entirely; they exist to test and evidence the auditor, not to audit anything.

## Checking the citations, quotes, arithmetic, isolation and integrity

Four mechanical gates guard the auditor's files, so nothing in it is trusted on the model's say-so alone. No network, no API key, Python 3 standard library only:

```bash
python3 tools/check_citations.py
python3 tools/check_arithmetic.py
python3 tools/check_no_network.py
python3 tools/check_reference_integrity.py
```

`check_citations.py` checks two things: every citation points at a provision that exists (and is not revoked) in reference/, and every double-quoted span in the auditor's files appears verbatim in a fixture invoice or in the shipped standard, so a fabricated quote fails mechanically no matter how convincing it reads. `check_arithmetic.py` recomputes every fixture invoice's line items, VAT and totals from its own stated numbers, so a plausible-looking "recomputes exactly" claim is either true or the run fails, and an invoice shape the parser doesn't recognise is a hard failure rather than a silent skip. `check_no_network.py` proves, by scanning the source of the checkers above rather than trusting their docstrings, that none of them contains an actual import of or call to a network, subprocess, or hosted-LLM-API module; it checks its own source too. `check_reference_integrity.py` verifies every file in reference/ against a SHA-256 recorded in [reference/MANIFEST.md](reference/MANIFEST.md), so a change to the standard's text, deliberate or not, cannot pass unnoticed.

Any kind of plant fails its run with the file, line and reason, and every tool prints what it does not check. To prove the gates themselves fire, run each self-test: a clean fixture must pass and a deliberately broken one must trigger every planted defect.

```bash
python3 tools/check_citations.py --self-test
python3 tools/check_arithmetic.py --self-test
python3 tools/check_no_network.py --self-test
python3 tools/check_reference_integrity.py --self-test
```

All eight runs (four checks, four self-tests) run in CI on every push ([.github/workflows/check.yml](.github/workflows/check.yml)).

A fifth script, [tools/check_freshness.sh](tools/check_freshness.sh), deliberately sits outside that guarantee: it fetches each source URL live and greps for a canary phrase from the vendored text, to catch the standard itself moving. It is the one checker that touches the network, which is exactly why it does not run in CI: run it by hand before relying on this auditor for anything that matters, and periodically after that. ([tools/audit.sh](tools/audit.sh) also reaches the network, because it calls Claude; it is the auditor, not a check on it.)

## The standard's version pin

Legislation and guidance change. Each file in [reference/](reference/CATALOG.md) carries its source URL, the version it reproduces, and the date it was accessed (4 September 2026; no outstanding amendments were pending at that date). To refresh: re-fetch from the source URL, replace the text below the header, and update the access date. Never hand-edit the standard text.

## Limits

- It audits UK VAT sales invoice particulars and nothing else. VAT liability, rates, input tax recovery, penalties and planning are out of scope, and the auditor says so rather than answering.
- It cites only the provisions shipped in reference/. If an answer would need anything else, it names the gap instead of citing from memory.
- It does not verify VAT registration number checksums; a present-but-odd number is an advisory, not a verdict.
- Every invoice in [fixtures/](fixtures/) is synthetic. No real business, person, VAT number or bank detail appears anywhere in this repository.
- None of this is tax advice.

## Receipts

Five evidence files, all outside the drop-in folder:

- [docs/cold-walk.md](docs/cold-walk.md): a fresh session using the auditor with no prior context, catching a planted defect and correcting the answer sheet when its own reading was better than mine.
- [docs/refusal-under-pressure.md](docs/refusal-under-pressure.md): the same kind of session run through four disguised requests to skip the audit entirely: a yes/no shortcut, a request to draft a replacement invoice, a request to certify compliance under deadline pressure, a request to skip straight to a ranking.
- [docs/verdict-under-pressure.md](docs/verdict-under-pressure.md): a different pressure test: whether a correct, already-issued finding survives a user arguing it should change (informal norms, claimed authority, a request for a bare opinion, a genuine technical challenge to what the regulation requires), plus a scope-discipline check: handed a document that was never an invoice at all, does it invent findings or decline correctly.
- [docs/reword-robustness.md](docs/reword-robustness.md): three independent, freshly-started sessions each audited the same underlying defect presented a different way (a casual reformat, a decoy Companies House number standing where a VAT number should be, and a paragraph of prose asserting registration without ever giving a number), to check the finding tracks what the regulation requires rather than the shape of any one fixture. Run in response to a specific test a community member proposed on this competition's own thread; full credit and the quote are in the file.
- [docs/batch-run.md](docs/batch-run.md): one fresh session given all ten fixtures in a single request, under [rules.md §6](rules.md). Every invoice got its full walk, nothing crossed between them (the missing VAT number on one Bluewharf invoice was reported as missing, not filled in from the four other Bluewharf invoices in the same batch), every verdict matched the answer key the session never opened, and the summary table came last.

Every transcript is published in full, not summarised; the claim in each file's own opening section is a read of what follows, not a substitute for it.

## Licence

The auditor's own files are MIT-licensed ([LICENSE](LICENSE)). The files in [reference/](reference/CATALOG.md) reproduce Crown copyright material: public sector information licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/), from [legislation.gov.uk](https://www.legislation.gov.uk/uksi/1995/2518) and [GOV.UK](https://www.gov.uk/guidance/record-keeping-for-vat-notice-70021), with source and access date stated in each file.

[AGENTS.md](AGENTS.md) is the engineering ruleset for agents working on this repo. Users of the auditor never need it.
