# Cold-walk receipt

**Date:** 4 September 2026
**Setup:** a fresh Claude agent session with no project context, no web access, and no prior knowledge of this repo was pointed at the folder and told only what a stranger would be told: *drop into this folder and Claude becomes a VAT invoice auditor — try it on one of the test invoices.* It was then asked to audit `fixtures/broken-simplified-over-limit.md` — a fixture deliberately **not** worked in examples.md. Nothing about the folder's structure, rules or reference cards was explained to it.

Disclosure: the stranger here is a fresh Claude session, not a human. The walk is reproducible by any human cold: clone the repo, open Claude Code in the folder, ask for that audit.

> **Note added 2026-09-11 (after the severity sign-off):** this run pre-dates it. In the walk below the missing customer particulars are graded invalid-invoice; under the signed-off severities (docs/review-notes.md item 3) a missing customer name or address is defective-field. The overall verdict is unchanged — the over-limit format and the missing sterling VAT total remain invalid-invoice, so the document is still NON-COMPLIANT — invalid invoice — only the grade on that one line has moved. Left as run rather than rewritten, since it is a transcript.

## What the cold session did (its own account, verbatim)

Files read, in order:

1. `CLAUDE.md` — entry point; routed it to identity.md, rules.md and the catalog, and forbade `judge-answer-key/`
2. `identity.md`
3. `rules.md`
4. `reference/CATALOG.md`
5. `examples.md`
6. `fixtures/broken-simplified-over-limit.md` — the invoice under audit
7. `reference/vat-regulations-1995-reg-16A.md` — for the £250 classification step
8. `reference/vat-regulations-1995-reg-14.md` — for the full checklist walk
9. `reference/vat-notice-700-21-invoicing.md` — for the clarifying notice citations
10. `tools/check_citations.py` — ran it on its own audit output: 17/17 citations resolved

Instructions it obeyed by **not** reading files: it left `judge-answer-key/` unread (the answer sheet — at the time of this walk it still sat inside `fixtures/`; it has since been moved out to a sibling directory so the same discipline no longer depends on the instruction holding), left reg 13 and reg 16 unopened (not needed for these facts), left the other fixtures and `tools/testdata/` unread, and skipped `AGENTS.md` (engineering-only). Where it had not opened reg 16, it declined to cite reg 16(2) and said so — the cite-only-what-you-loaded guardrail holding under pressure.

## What it found

Verdict: **NON-COMPLIANT — invalid invoice** — invalid-invoice: 3 · defective-field: 4 · advisory: 0 · passes: 8.

The planted defect was caught head-on: simplified format at £474.00 gross, over the £250 limit `[reg 16A; 700/21 §4.5]`, classified invalid-invoice exactly as the severity table requires. It then did something better than the answer sheet anticipated: having correctly escalated to the full checklist, it reported the knock-on failures a simplified-format document necessarily has at that value — no customer particulars `[reg 14(1)(e)]`, no VAT amount stated in sterling or at all `[reg 14(1)(l)]`, no net figures `[reg 14(1)(h); reg 14(1)(i)]`, no unit price `[reg 14(1)(m)]`, no date of issue `[reg 14(1)(c)]` — each located, cited, graded, with the reissue arithmetic derived (£395.00 net, £79.00 VAT). Every applicable check it passed was reported as a pass.

The answer sheet (now `judge-answer-key/EXPECTED.md`) was corrected after this walk to acknowledge those knock-on findings — the cold session's reading was right and the answer sheet's one-defect-per-fixture framing was wrong for this fixture. That correction is this receipt's proof of honest testing: the test changed the repo, not the other way round.

## Full transcript of the audit output

The cold session's complete, unedited final message is preserved below.

---

# Audit — fixtures/broken-simplified-over-limit.md

**Intake.** Document headed "RECEIPT / VAT INVOICE — 0523" from Sparkfield Electrical Ltd, Unit 3, Mocklands Trading Estate, Testborough TB2 8XX, VAT No: GB 444 5555 66. No customer is named. Sterling throughout. Gross £474.00 including VAT. Date of supply 30 August 2026. It is not endorsed "This is not a VAT invoice", so it stands to be audited as a VAT invoice [reg 14(3)].

**Classification.** Gross consideration including VAT is £474.00 — over £250 — so the full checklist applies [reg 14(1)]. The document is drawn in simplified format (supplier particulars, time of supply, description, VAT-inclusive total and rate — nothing more), and the issuer is an electrical contractor, not a retailer, so the simplified-invoice relaxation is the relevant comparison — and it is not available at this value:

```
[invalid-invoice] Whole document — headed "RECEIPT / VAT INVOICE — 0523" and drawn in
simplified format ("Total payable (including VAT): £474.00" with a rate but no net or
VAT figures), but a simplified invoice is permitted only where the consideration for
the supply does not exceed £250, and this supply is £474.00 including VAT — reissue as
a full VAT invoice (or a modified VAT invoice showing VAT-inclusive values)
[reg 16A; 700/21 §4.5]
```

Reg 14(2) is not engaged: the supplier's registration carries a GB prefix and nothing identifies the business for VAT in Northern Ireland.

**Checklist** (full particulars, reg 14(1)(a)–(p); (f) and (k) revoked and skipped):

```
[pass] Sequential invoice number — "0523" in the heading uniquely identifies the document [reg 14(1)(a)]
[pass] Time of supply — "Date of supply: 30 August 2026" [reg 14(1)(b)]
[defective-field] Date of issue — no issue date appears; the only date on the document is
"Date of supply: 30 August 2026", and nothing on the face confirms the document was issued
that same day — state the date of issue on reissue (the regulation requires it; the notice
reads it as needed where it differs from the time of supply, which this document leaves
unverifiable, so the nearest analogue in the severity table applies) [reg 14(1)(c); 700/21 §4.1]
[pass] Supplier particulars — "Sparkfield Electrical Ltd", "Unit 3, Mocklands Trading
Estate, Testborough TB2 8XX" and "VAT No: GB 444 5555 66" all present [reg 14(1)(d)]
[invalid-invoice] Customer particulars — no customer name or address appears anywhere on
the document — reissue naming the person supplied and their address; until then the
document cannot stand as that customer's evidence for the VAT charged [reg 14(1)(e)]
[pass] Description — "Rewire of garage supply, replacement distribution board and
testing", sufficient to identify the services supplied [reg 14(1)(g)]
[defective-field] Per-description particulars — the line "Rewire of garage supply,
replacement distribution board and testing — £474.00" shows the VAT rate (20%) but no
amount payable excluding VAT; £474.00 is the VAT-inclusive figure — restate the line
net of VAT on reissue [reg 14(1)(h)]
[defective-field] Gross total payable excluding VAT — only "Total payable (including
VAT): £474.00" is stated; no VAT-exclusive total appears — show the net total (£395.00
on the stated facts) on reissue [reg 14(1)(i)]
[pass] Cash discount — none offered on the face of the document, so no rate is required [reg 14(1)(j)]
[invalid-invoice] VAT total — no amount of VAT chargeable is stated anywhere, in sterling
or otherwise; "Amount includes VAT at 20%: gross £474.00 at standard rate." gives only
the rate, never the VAT amount — reissue stating the total VAT chargeable in sterling
(£79.00 on the stated facts) [reg 14(1)(l); 700/21 §4.1]
[defective-field] Unit price — no VAT-exclusive unit price is shown; the only figure
attached to the supply is the VAT-inclusive £474.00 — state the unit price on reissue [reg 14(1)(m)]
[pass] Margin scheme, reverse charge, free zone references — none engaged on these facts [reg 14(1)(n); reg 14(1)(o); reg 14(1)(p)]
[pass] Exempt/zero-rated distinction — not engaged: the single supply is standard-rated [reg 14(4)]
```

**Arithmetic.** The document states one amount: £474.00 gross including VAT at 20%. Recomputed: £474.00 ÷ 1.20 = £395.00 net; VAT = £395.00 × 20% = £79.00; £395.00 + £79.00 = £474.00 ✓. The stated gross is internally consistent with the stated rate. The net and VAT figures here are derived, not stated — they are what the reissued full invoice must show.

```
[pass] Arithmetic — the one stated amount recomputes exactly against the stated 20% rate [reg 14(1)(h)]
```

**Special references.** No margin scheme, reverse-charge or free-zone facts appear, and no exempt supply is included on the document, so the ban on exempt supplies in simplified and retailers' invoices is not engaged either — both covered by the pass lines above.

**Verdict: NON-COMPLIANT — invalid invoice** — invalid-invoice: 3 · defective-field: 4 · advisory: 0 · passes: 8
