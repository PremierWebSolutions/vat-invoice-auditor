# Rules — audit order, citations, severity

## 1. Audit order

Run every audit in this exact order. Each numbered step produces either passes or findings — silence is not an option for any step that applies.

1. **Intake.** Identify the document: issuer, customer, date(s), currency, gross value. If it is endorsed "This is not a VAT invoice" (delivery notes, pro formas), stop and report that it falls outside reg 14 by design [reg 14(3)].
2. **Classify.** Decide which checklist applies:
   - Gross consideration (including VAT) **£250 or less** → the invoice *may* stand as a **simplified invoice** [reg 16A] (or a **retailer's invoice** [reg 16] if the issuer is a retailer). Audit against the simplified particulars first; only escalate to the full checklist if the issuer clearly intended a full invoice.
   - Gross consideration **over £250** → the **full checklist** [reg 14(1)] applies. A simplified-format invoice over £250 is itself a finding.
   - Issuer identified for VAT in Northern Ireland invoicing a person in an EU member state → the additional particulars of [reg 14(2)] also apply.
3. **Walk the checklist in provision order.** For a full invoice that means reg 14(1)(a) through (p), skipping revoked sub-paragraphs (f) and (k); for a simplified invoice, reg 16A(a)–(e) (or reg 16(1)(a)–(e)). One PASS or one finding per particular. **On reg 14(1)(a):** a single invoice can only show that a reference number is present and formatted consistently with a sequential series — never that it is genuinely unbroken across the issuer's full run, which needs the whole series and is outside what one document can prove. Say so; don't claim more than the document in front of you supports.
4. **Arithmetic.** Recompute each line (quantity × unit price = net), each VAT amount at the stated rate, the net total, and the VAT total. The VAT total must be expressed in sterling whatever the invoice currency [reg 14(1)(l)]. Report the recomputation, not just its conclusion.
5. **Special references.** Check whether the facts trigger a required wording and whether it is present: margin scheme [reg 14(1)(n)], reverse charge [reg 14(1)(o)], free zone [reg 14(1)(p)], mixed exempt/zero-rated supplies distinguished [reg 14(4)], no exempt supply on a simplified or retailer's invoice [reg 16(2); 700/21 §4.5]. **A pass on any of these is a ruled-out verdict, not a shrug — it must name the specific fact on the invoice that rules the trigger out**: *no antiques, art, collectors' items or tour-operator wording anywhere on the invoice, so no margin-scheme reference is required* reads as a ruled-out verdict; a bare *not engaged* does not. A reference that could apply on the facts shown and isn't checked is a missed finding, not a pass by default.
6. **Report** in the format of §3 below, closing with the verdict of §4.

## 2. Citation format

Every finding and every pass carries exactly one bracketed citation, in one of these two forms — nothing else counts as a citation:

- **Regulation:** `[reg 14(1)(a)]`, `[reg 14(2)]`, `[reg 16A(c)]`, `[reg 16(2)]` — regulation number, then paragraph/sub-paragraph elements in order, each in its own parentheses.
- **Notice:** `[700/21 §4.1]`, `[700/21 §3.1]` — section number as headed in the notice.

Two citations may be paired in one bracket where the notice clarifies the regulation: `[reg 14(1)(l); 700/21 §4.1]`.

Cite only provisions whose text is shipped in [reference/](reference/CATALOG.md). Every citation must resolve against those files, and every double-quoted span (invoice text or the standard's words) must be a real quote of its source — `tools/check_citations.py` verifies both mechanically, and a citation that does not resolve or a quote that appears nowhere is a defect in the audit itself.

## 3. Finding format

```
[invalid-invoice] Supplier block — no VAT registration number appears anywhere on the
document (the block reads "Bluewharf Joinery Ltd, 14 Sample Wharf, Testborough") —
reissue showing the supplier's VAT registration number [reg 14(1)(d); 700/21 §4.1]
```

Four parts, in order: severity tag, **location on the invoice** (field or line, quoting the invoice's own text), **what is wrong, specifically**, **what to do**, then the citation. Passes are one line each:

```
[pass] Invoice reference — "INV-2041" is present, in a format consistent with a sequential series [reg 14(1)(a)]
```

## 4. Severity classification

Three severities. Use these three and no others.

| Severity | Meaning | Consequence stated in the report |
|---|---|---|
| **invalid-invoice** | The defect defeats the document: it cannot stand as the VAT invoice for the supply, or it misstates the VAT position | Must be reissued (or credited and reissued); customer's input tax evidence is at risk until then |
| **defective-field** | A required particular is missing or wrong, but the document still identifies the supply and its VAT | Correct on reissue or by supplementary document; raise with the issuer's bookkeeper |
| **advisory** | No breach of the shipped provisions — best practice, or a risk flag outside this auditor's scope | Note only; no reissue required |

### Assignment table

| Defect | Severity | Citation |
|---|---|---|
| Supplier VAT registration number missing | invalid-invoice | [reg 14(1)(d)] |
| Supplier name or address missing | invalid-invoice | [reg 14(1)(d)] |
| Description insufficient to identify the supply | invalid-invoice | [reg 14(1)(g)] |
| Time of supply absent and not inferable from any date on the document | invalid-invoice | [reg 14(1)(b)] |
| VAT total absent, or not expressed in sterling | invalid-invoice | [reg 14(1)(l)] |
| Stated VAT does not follow from the lines and rates shown (beyond rounding) | invalid-invoice | [reg 14(1)(h); reg 14(1)(l)] |
| Simplified-format invoice where gross consideration exceeds £250 | invalid-invoice | [reg 16A; 700/21 §4.5] |
| "Reverse charge" reference missing where the customer must account for the VAT | invalid-invoice | [reg 14(1)(o)] |
| Margin scheme reference missing where a margin scheme applied | invalid-invoice | [reg 14(1)(n)] |
| Exempt supply included on a simplified or retailer's invoice | invalid-invoice | [reg 16(2); 700/21 §4.5] |
| Customer name missing | invalid-invoice | [reg 14(1)(e)] |
| Customer address missing (name present) | defective-field | [reg 14(1)(e)] |
| No reference number present anywhere on the invoice | defective-field | [reg 14(1)(a)] |
| Same reference number seen on two documents audited together | defective-field | [reg 14(1)(a)] |
| Date of issue absent where it differs from the time of supply | defective-field | [reg 14(1)(c)] |
| Unit price missing | defective-field | [reg 14(1)(m)] |
| Quantity or extent missing for a description | defective-field | [reg 14(1)(h)] |
| Rate of VAT not shown per description | defective-field | [reg 14(1)(h)] |
| Gross total payable excluding VAT missing | defective-field | [reg 14(1)(i)] |
| Rate of an offered cash discount not shown | defective-field | [reg 14(1)(j)] |
| Exempt/zero-rated lines not distinguished on a mixed full invoice | defective-field | [reg 14(4)] |
| Net amounts in a foreign currency (VAT total properly in sterling) | advisory — permitted | [reg 14(1)(h)] |
| VAT registration number present but format looks unusual | advisory — this auditor does not verify checksums | [reg 14(1)(d)] |
| Rounding differences of a penny per line | advisory | [reg 14(1)(h)] |

A defect not in this table gets the severity its nearest analogue has, with the reasoning stated in the finding. Never leave a finding unclassified.

## 5. Verdict

Close every audit with exactly one of:

- **NON-COMPLIANT — invalid invoice** — one or more invalid-invoice findings.
- **NON-COMPLIANT — defective particulars** — defective-field findings only.
- **COMPLIANT (with advisories)** — advisory findings only.
- **COMPLIANT** — every applicable check passed.

Followed by the counts: `invalid-invoice: n · defective-field: n · advisory: n · passes: n`.
