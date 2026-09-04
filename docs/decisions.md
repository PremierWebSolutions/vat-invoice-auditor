# Decisions

One line each, with the reason — so the next agent doesn't reverse a deliberate choice as an improvement.

- Ship regs 13, 16 and 16A alongside reg 14 — classification (step 2 of the audit order) and the £250 relaxations are impossible to audit from reg 14 alone.
- Reproduce the standard text verbatim rather than summarising — the competition auto-fails a reference/ folder without the standard itself, and a summary of law is a paraphrase risk.
- Strip legislation.gov.uk's editorial F-markers from the reference text but keep revoked provisions as dotted runs — readable current text, with the omission disclosed in every card header.
- Checker validates that citations exist (and are not revoked) in reference/, not that quoted wording matches — wording legitimately drifts on re-fetch; existence-checking catches planted citations with no false positives.
- Checker flags citations to revoked sub-paragraphs (reg 14(1)(f), (k)) as errors — citing a revoked provision is exactly the subtle corruption a judge would plant.
- A loose regex catches malformed near-citations (a bracketed `Reg 14, para 1(d)`-style reference) instead of ignoring them — a citation that silently drops out of checking is worse than a failing one.
- Three severities graded by consequence (reissue / correct / note) — mirrors how an accountant triages invoice defects; names fixed in rules.md so audits stay comparable.
- Full-invoice fixtures all exceed £250 gross — keeps the simplified-invoice relaxation from muddying which provision each fixture tests.
- fixtures/EXPECTED.md is quarantined from the auditor (CLAUDE.md says never read it during an audit) — an answer sheet in context would make every test vacuous.
- VAT registration number checksum validation is out of scope, advisory only — the auditor checks invoicing particulars, not registration status.
- Severity assignments were drafted by Claude; the judgment calls that need a practising accountant's eye are flagged in [review-notes.md](review-notes.md) for Andy's sign-off before submission, not silently resolved.
