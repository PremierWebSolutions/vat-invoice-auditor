# Decisions

One line each, with the reason — so the next agent doesn't reverse a deliberate choice as an improvement.

- Ship regs 13, 16 and 16A alongside reg 14 — classification (step 2 of the audit order) and the £250 relaxations are impossible to audit from reg 14 alone.
- Reproduce the standard text verbatim rather than summarising — the competition auto-fails a reference/ folder without the standard itself, and a summary of law is a paraphrase risk.
- Strip legislation.gov.uk's editorial F-markers from the reference text but keep revoked provisions as dotted runs — readable current text, with the omission disclosed in every card header.
- Checker validates that citations exist (and are not revoked) in reference/, not that quoted wording matches — wording legitimately drifts on re-fetch; existence-checking catches planted citations with no false positives.
- Checker flags citations to revoked sub-paragraphs (reg 14(1)(f), (k)) as errors — citing a revoked provision is exactly the subtle corruption a judge would plant.
- A loose regex catches malformed near-citations (a bracketed `Reg 14, para 1(d)`-style reference) instead of ignoring them — a citation that silently drops out of checking is worse than a failing one.
- A second gate grounds every double-quoted span in the auditor's files against the fixtures and the shipped standard — past judging cycles planted a fabricated quote as well as a bad citation, and citation-existence checking alone is blind to a resolving citation wearing invented words.
- Quote-grounding scope is the four auditor files (identity, rules, examples, cold-walk), not README/AGENTS — those quote coined instructions, and a gate that cries wolf on honest prose gets deleted.
- The checker prints what it does not check with every result — a clean run that overclaims is how a gate teaches people to stop reading it.
- Three severities graded by consequence (reissue / correct / note) — mirrors how an accountant triages invoice defects; names fixed in rules.md so audits stay comparable.
- Full-invoice fixtures all exceed £250 gross — keeps the simplified-invoice relaxation from muddying which provision each fixture tests.
- The answer key lives in judge-answer-key/, not fixtures/ (moved from fixtures/EXPECTED.md) — a CLAUDE.md instruction not to read a file is a request the auditor is trusted to honour, and past judging cycles have shown that trust misplaced; a sibling directory the drop-in never includes is a folder-position fact, not a request. See judge-answer-key/EXPECTED.md's own header.
- Arithmetic in the fixtures and worked examples is verified by `tools/check_arithmetic.py`, not asserted by the model that wrote it — a script recomputing every total is the same enforcement-in-code discipline as the citation and quote gates, applied to the one other thing a plausible-sounding audit can get wrong silently.
- VAT registration number checksum validation is out of scope, advisory only — the auditor checks invoicing particulars, not registration status.
- Severity assignments were drafted by Claude; the judgment calls that need a practising accountant's eye are flagged in [review-notes.md](review-notes.md) for Andy's sign-off before submission, not silently resolved.
