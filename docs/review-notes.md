# Severity judgment calls — for professional review

The severity table in [rules.md §4](../rules.md) was drafted by Claude. These are the calls that involved judgment rather than plain reading; each stands unless you overrule it, and any change is a one-line edit to the table (then re-run `python3 tools/check_citations.py`).

1. **Missing "reverse charge" reference → invalid-invoice** [reg 14(1)(o)]. Reasoning: the omission misdirects who accounts for the VAT, so the document misstates the VAT position — the defect defeats the invoice, not just a field. Arguable alternative: defective-field, correctable by reissue like any other particular.
2. **Missing sequential number → defective-field** [reg 14(1)(a)]. Reasoning: the supply and its VAT remain fully identified; the defect is record-keeping, not substance. Arguable alternative: invalid-invoice, since HMRC treats numbering as a hard requirement.
3. **Customer name missing → invalid-invoice, but address missing (name present) → defective-field** [reg 14(1)(e)]. The line drawn: with no name the document cannot evidence *whose* input tax it is; with a name but no address it still can.
4. **Gross total excluding VAT missing → defective-field** [reg 14(1)(i)] — recomputable from compliant lines. Arguable alternative: invalid-invoice.
5. **Missing margin-scheme reference → invalid-invoice** [reg 14(1)(n)] — mirrors the reverse-charge call (item 1): the wording is what tells the customer no input tax is recoverable.
6. **Internally inconsistent VAT arithmetic → invalid-invoice** [reg 14(1)(h); reg 14(1)(l)] — a stated VAT total that does not follow from the lines misstates "the total amount of VAT chargeable".
7. **Classification wording** (rules.md §1 step 2): a ≤£250 invoice is audited against the simplified particulars first, escalating to the full checklist only where the issuer clearly intended a full invoice. Sense-check that this matches how you'd triage in practice.

## Outcome — reviewed and signed off 2026-09-11 (a practising UK chartered accountant)

1. **Reverse-charge wording missing → changed to defective-field** (was invalid-invoice), with a split: it is invalid-invoice only where the reverse-charge supply still shows a separate, reclaimable VAT amount (a buyer could wrongly claim it); where the invoice is gross-only with just the wording missing, it is defective-field — nothing is wrongly reclaimable and a gross-only figure is itself an obvious prompt to check the treatment.
2. **Kept** — missing invoice number stays defective-field.
3. **Customer name missing → changed to defective-field** (was invalid-invoice); name and address now graded the same. HMRC's test is who actually received the supply, the name is only prima facie evidence, and a £250-or-under receipt does not need a customer name at all (handled by classification). Research: ACCA and AccountingWEB, Sept 2026.
4. **Kept** — missing net (pre-VAT) subtotal stays defective-field.
5. **Margin-scheme wording missing → changed to the same split as item 1**: invalid-invoice only where a separate reclaimable VAT amount is shown; defective-field where the supply is gross-only with the wording missing.
6. **Kept** — VAT that does not follow from the lines stays invalid-invoice.
7. **Classification wording tidied** — a £250-or-under invoice is now always judged against the simplified particulars; the woolly "only escalate if the issuer clearly intended a full invoice" caveat is removed.

Knock-on updates made in the same change: the severity table and classification wording in [rules.md](../rules.md); the reverse-charge worked audit in [examples.md](../examples.md) (now "defective particulars"); the reverse-charge row in [judge-answer-key/EXPECTED.md](../judge-answer-key/EXPECTED.md); dated notes on the two run receipts that pre-date this sign-off ([cold-walk.md](cold-walk.md), [batch-run.md](batch-run.md)); and [decisions.md](decisions.md).
