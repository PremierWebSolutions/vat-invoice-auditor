# Severity judgment calls — for Andy's review

The severity table in [rules.md §4](../rules.md) was drafted by Claude. These are the calls that involved judgment rather than plain reading; each stands unless you overrule it, and any change is a one-line edit to the table (then re-run `python3 tools/check_citations.py`).

1. **Missing "reverse charge" reference → invalid-invoice** [reg 14(1)(o)]. Reasoning: the omission misdirects who accounts for the VAT, so the document misstates the VAT position — the defect defeats the invoice, not just a field. Arguable alternative: defective-field, correctable by reissue like any other particular.
2. **Missing sequential number → defective-field** [reg 14(1)(a)]. Reasoning: the supply and its VAT remain fully identified; the defect is record-keeping, not substance. Arguable alternative: invalid-invoice, since HMRC treats numbering as a hard requirement.
3. **Customer name missing → invalid-invoice, but address missing (name present) → defective-field** [reg 14(1)(e)]. The line drawn: with no name the document cannot evidence *whose* input tax it is; with a name but no address it still can.
4. **Gross total excluding VAT missing → defective-field** [reg 14(1)(i)] — recomputable from compliant lines. Arguable alternative: invalid-invoice.
5. **Missing margin-scheme reference → invalid-invoice** [reg 14(1)(n)] — mirrors the reverse-charge call (item 1): the wording is what tells the customer no input tax is recoverable.
6. **Internally inconsistent VAT arithmetic → invalid-invoice** [reg 14(1)(h); reg 14(1)(l)] — a stated VAT total that does not follow from the lines misstates "the total amount of VAT chargeable".
7. **Classification wording** (rules.md §1 step 2): a ≤£250 invoice is audited against the simplified particulars first, escalating to the full checklist only where the issuer clearly intended a full invoice. Sense-check that this matches how you'd triage in practice.

Once reviewed, record the outcome here (item by item: kept / changed to what) and update [decisions.md](decisions.md).
