# Batch-run receipt

**Date:** 10 September 2026
**Setup:** a fresh Claude agent session with no prior context was pointed at this folder and given one request: *Audit every invoice in fixtures/.* That is the batch shape [rules.md §6](../rules.md) exists for, and the thing §6 most needs to survive is the temptation a batch creates: to give the later invoices a lighter walk because the earlier ones looked similar, or to let a defect found on one colour the reading of the next. The session was asked to return every audit block in full plus the closing summary, then to say whether any invoice got a shorter walk than the first and whether anything crossed between invoices.

Disclosure: as with the other receipts, this is one agent session producing the whole run in a single pass, not a human bookkeeper working a stack. The session had never seen `judge-answer-key/` and left it unread.

## What it found (my read, before the transcript)

All ten fixtures audited, in directory order, none abbreviated: every full-checklist invoice carries one line per applicable reg 14(1) particular plus 14(4) and arithmetic; the two short-form documents carry one line per reg 16A or reg 16(1) particular plus the three ruled-out references and the exempt-supply check. The pass counts vary only because the applicable checklists vary. Every verdict matches the answer key the session never opened. The two batch-only checks in §6 (a reference number repeated across documents; one supplier with two VAT numbers) were both run and both correctly came back negative, reported once in the summary and nowhere else. On the one place cross-contamination would have been easiest, INV-2044's missing VAT number, the session reported it as missing rather than filling it in from the four other Bluewharf documents in the same batch that carry the number. It closed by running the repo's own citation and integrity checkers on its draft; both passed.

Two things worth reading closely. The unnumbered invoice and CN-118 now carry the corrected reg 14(1)(a) wording (present, in a format consistent with a series; continuity not provable from one document), which is the fix made earlier today showing up live. And the simplified-format receipt over £250 gets the same escalation the earlier cold walk gave it, with the session noting on its own that the modified-invoice alternative the notice mentions is not shipped in reference/ and saying so rather than guessing.

## Full transcript

---

# Batch audit — fixtures/ (10 invoices, audited in directory order)

Each invoice below gets its own complete audit under rules.md §§1–5; the summary table at the end follows the audits and never replaces them.

---

## 1. fixtures/broken-arithmetic-vat-total.md — INV-2049

**Invoice:** fixtures/broken-arithmetic-vat-total.md

**Intake.** Sales invoice INV-2049 from Bluewharf Joinery Ltd (14 Sample Wharf, Testborough TB1 4XX) to Harrold & Vane Ltd, sterling throughout, stated gross "Total payable: £1,426.00"; time of supply 1 September 2026, date of issue 2 September 2026. The document is not endorsed "This is not a VAT invoice", so reg 14(3) is not engaged.

**Classification.** Gross consideration exceeds £250, so the full checklist applies [reg 14(1)]. The supplier's registration number carries a GB prefix and the customer address is a UK one, so the Northern Ireland/EU additional particulars are not engaged [reg 14(2)].

**Checklist.**

```
[pass] Invoice reference — "INV-2049" is present, in a format consistent with a sequential series; whether the series is unbroken across the issuer's full run cannot be shown by one document [reg 14(1)(a)]
[pass] Time of supply — "Time of supply: 1 September 2026" [reg 14(1)(b)]
[pass] Date of issue — "Date of issue: 2 September 2026", stated separately from the time of supply [reg 14(1)(c)]
[pass] Supplier particulars — "Bluewharf Joinery Ltd", "14 Sample Wharf, Testborough TB1 4XX" and "VAT registration number: GB 111 2222 33" all present [reg 14(1)(d)]
[pass] Customer particulars — "Harrold & Vane Ltd" at "9 Placeholder Row, Mockton MK9 2YY" [reg 14(1)(e)]
[pass] Description — "Oak door blanks, 838mm" and "Site fitting labour", each sufficient to identify the goods or services [reg 14(1)(g)]
[pass] Per description: quantity/extent (6 and 2 days), VAT rate (20% on both lines) and net amount (£510.00 and £640.00) all shown [reg 14(1)(h)]
[pass] Gross total payable excluding VAT — "Total net: £1,150.00" [reg 14(1)(i)]
[pass] Cash discount — ruled out: no discount or settlement terms are mentioned anywhere on the invoice, and a rate is only required where one is offered [reg 14(1)(j)]
[pass] Total VAT chargeable in sterling — "Total VAT: £276.00" is present and expressed in sterling; whether the figure follows from the lines is tested at the arithmetic step below [reg 14(1)(l)]
[pass] Unit price — "£85.00" and "£320.00 per day", shown for every line [reg 14(1)(m)]
[pass] Margin scheme — ruled out: no works of art, antiques, collectors' items, second-hand goods or tour-operator wording anywhere on the invoice; oak door blanks and site fitting labour carry no margin-scheme indication [reg 14(1)(n)]
[pass] Reverse charge — ruled out: the customer is charged VAT directly at "20%" on every line rather than the supplier shifting the liability, so the person supplied is not the one liable to account for the tax [reg 14(1)(o)]
[pass] Free zone — ruled out: nothing on the invoice places the supply within Item 1 of Group 22 of Schedule 8 (free zones) [reg 14(1)(p)]
[pass] Exempt/zero-rated distinction — ruled out: both lines are charged at the standard 20% rate, so there is no exempt or zero-rated line to distinguish [reg 14(4)]
```

**Arithmetic.** Line 1: 6 × £85.00 = £510.00 ✓, VAT at 20% = £102.00 ✓. Line 2: 2 × £320.00 = £640.00 ✓, VAT at 20% = £128.00 ✓. Net total £510.00 + £640.00 = £1,150.00 ✓, matching "Total net: £1,150.00". VAT total: the two line VAT amounts £102.00 + £128.00 = £230.00, and 20% of £1,150.00 = £230.00 — but the invoice states "Total VAT: £276.00", £46.00 more than the lines and rate support (£276.00 would be 24% of the net, or 20% of £1,380.00; no line, rate or note on the document yields it, and it is far beyond rounding). Gross: £1,150.00 + £276.00 = £1,426.00 does match the stated "Total payable: £1,426.00", so the gross faithfully carries the wrong VAT figure; on the lines shown the gross should be £1,150.00 + £230.00 = £1,380.00.

```
[invalid-invoice] VAT total — "Total VAT: £276.00" does not follow from the lines and rates shown: the line VAT amounts ("£102.00" + "£128.00") and 20% of the net total (£1,150.00) both give £230.00, a £46.00 difference that no rounding explains, and the gross "Total payable: £1,426.00" carries the same error — reissue (or credit and reissue) showing the VAT total that follows from the lines (£230.00) and the total payable that follows from it (£1,380.00); until then the document misstates the VAT position and the customer's input tax evidence is at risk [reg 14(1)(h); reg 14(1)(l)]
```

**Verdict: NON-COMPLIANT — invalid invoice** — invalid-invoice: 1 · defective-field: 0 · advisory: 0 · passes: 15

---

## 2. fixtures/broken-exempt-on-simplified.md — Kettle Lane Stores & Post Office till receipt, 2 September 2026

**Invoice:** fixtures/broken-exempt-on-simplified.md

**Intake.** Document headed "TILL RECEIPT / VAT INVOICE" from Kettle Lane Stores & Post Office, self-described on the document as "(retailer)", 41 Kettle Lane, Testborough TB4 6XX; no customer named; sterling; a single date, "Date: 2 September 2026"; gross "Total payable: £179.17". No reference number appears anywhere. The document is not endorsed "This is not a VAT invoice", so reg 14(3) is not engaged.

**Classification.** Gross consideration £179.17 is £250 or less and the issuer identifies itself as a retailer, so the document may stand as a retailer's invoice and is audited against the retailer's particulars [reg 16(1)]; the notice's retailer paragraph is [700/21 §4.4]. Nothing on the document suggests the issuer intended a full invoice (no customer, no number, VAT-inclusive figures), so there is no escalation to the full checklist. A customer's name and a reference number are not among the reg 16(1) particulars, so their absence is not a finding here. The full-invoice distinguishing rule [reg 14(4)] applies only to an invoice carrying the reg 14(1) particulars; its counterpart for this document is the prohibition on exempt supplies [reg 16(2)], checked in the special references below.

**Checklist.**

```
[pass] Retailer particulars — "Kettle Lane Stores & Post Office", "41 Kettle Lane, Testborough TB4 6XX" and "VAT No: GB 555 6666 77" all present [reg 16(1)(a)]
[pass] Time of supply — the document carries one date, "Date: 2 September 2026"; on a till receipt the transaction date is the time of supply, and nothing on the document suggests the goods changed hands on any other day [reg 16(1)(b)]
[pass] Description — "Box A4 copier paper × 2", "Printer ink cartridges × 3" and "First class postage stamps, book of 50 (exempt)", each sufficient to identify the goods [reg 16(1)(c)]
[pass] Total amount payable including VAT — "Total payable: £179.17" [reg 16(1)(d)]
[pass] Per rate of VAT chargeable, gross including VAT and the rate — for the one chargeable rate the document states "Of which standard-rated goods £94.17 including VAT at 20%." [reg 16(1)(e)]
[pass] Margin scheme — ruled out: no works of art, antiques, collectors' items, second-hand goods or tour-operator wording anywhere on the receipt; copier paper, ink cartridges and postage stamps carry no margin-scheme indication [reg 14(1)(n)]
[pass] Reverse charge — ruled out: the retailer charges VAT within the price ("including VAT at 20%") rather than shifting the liability to the customer [reg 14(1)(o)]
[pass] Free zone — ruled out: nothing on the receipt places the supply within Item 1 of Group 22 of Schedule 8 (free zones) [reg 14(1)(p)]
[invalid-invoice] Exempt line — the receipt lists "First class postage stamps, book of 50 (exempt)" at "£85.00" and repeats "Postage stamps exempt from VAT: £85.00."; an invoice provided under regulation 16 "shall not contain any reference to any exempt supply", and the notice's retailer paragraph (4.4) and simplified paragraph (4.5) both say "exempt supplies must not be included in this type of VAT invoice" — reissue either as a retailer's invoice confined to the standard-rated goods (£94.17) with no reference to the exempt stamps, or as a full VAT invoice under reg 14(1) that distinguishes the exempt supply; until then the customer's input tax evidence is at risk [reg 16(2); 700/21 §4.5]
```

**Arithmetic.** £19.20 + £74.97 + £85.00 = £179.17 ✓, matching "Total payable: £179.17". Standard-rated goods £19.20 + £74.97 = £94.17 ✓, matching the stated £94.17 at 20%; the VAT within that gross at 20% is £94.17 × 20/120 = £15.70 (rounded from £15.695), which is not separately stated and is not a reg 16(1) particular. Exempt line £85.00 ✓; £94.17 + £85.00 = £179.17 ✓. Per-item prices are not stated (not a reg 16(1) particular) but each line total divides cleanly by its quantity: £19.20 ÷ 2 = £9.60; £74.97 ÷ 3 = £24.99.

```
[pass] Arithmetic — the three lines sum to the stated total, and the per-rate gross plus the exempt figure sum to the same total [reg 16(1)(e)]
```

**Verdict: NON-COMPLIANT — invalid invoice** — invalid-invoice: 1 · defective-field: 0 · advisory: 0 · passes: 9

---

## 3. fixtures/broken-missing-sequential-number.md — unnumbered Bluewharf invoice, 19 August 2026

**Invoice:** fixtures/broken-missing-sequential-number.md

**Intake.** Sales invoice headed only "INVOICE" — no number follows the heading and none appears elsewhere — from Bluewharf Joinery Ltd (14 Sample Wharf, Testborough TB1 4XX) to Harrold & Vane Ltd, sterling, gross "Total payable: £648.00"; time of supply and date of issue both 19 August 2026. The document is not endorsed "This is not a VAT invoice", so reg 14(3) is not engaged.

**Classification.** Gross consideration exceeds £250, so the full checklist applies [reg 14(1)]. GB-prefixed supplier number and a UK customer address, so [reg 14(2)] is not engaged.

**Checklist.**

```
[defective-field] Invoice reference — the heading reads "INVOICE" with nothing after it, and no reference number appears in any field on the document; a full VAT invoice must carry a sequential number based on one or more series which uniquely identifies the document — correct on reissue or by supplementary document showing the number from the issuer's series, and raise with the issuer's bookkeeper [reg 14(1)(a)]
[pass] Time of supply — "Time of supply: 19 August 2026" [reg 14(1)(b)]
[pass] Date of issue — "Date of issue: 19 August 2026", same day as the supply, stated [reg 14(1)(c)]
[pass] Supplier particulars — "Bluewharf Joinery Ltd", "14 Sample Wharf, Testborough TB1 4XX" and "VAT registration number: GB 111 2222 33" all present [reg 14(1)(d)]
[pass] Customer particulars — "Harrold & Vane Ltd" at "9 Placeholder Row, Mockton MK9 2YY" [reg 14(1)(e)]
[pass] Description — "Radiator cover cabinets, painted MDF", sufficient to identify the goods [reg 14(1)(g)]
[pass] Per description: quantity (12), VAT rate (20%) and net amount (£540.00) shown [reg 14(1)(h)]
[pass] Gross total payable excluding VAT — "Total net: £540.00" [reg 14(1)(i)]
[pass] Cash discount — ruled out: no discount or settlement terms are mentioned anywhere on the invoice, and a rate is only required where one is offered [reg 14(1)(j)]
[pass] Total VAT chargeable in sterling — "Total VAT: £108.00" [reg 14(1)(l)]
[pass] Unit price — "£45.00" per cabinet [reg 14(1)(m)]
[pass] Margin scheme — ruled out: no works of art, antiques, collectors' items, second-hand goods or tour-operator wording anywhere on the invoice; painted MDF radiator cover cabinets carry no second-hand or other margin-scheme indication [reg 14(1)(n)]
[pass] Reverse charge — ruled out: the customer is charged VAT directly at "20%" rather than the supplier shifting the liability, so the person supplied is not the one liable to account for the tax [reg 14(1)(o)]
[pass] Free zone — ruled out: nothing on the invoice places the supply within Item 1 of Group 22 of Schedule 8 (free zones) [reg 14(1)(p)]
[pass] Exempt/zero-rated distinction — ruled out: the single line is charged at the standard 20% rate, so there is no exempt or zero-rated line to distinguish [reg 14(4)]
```

**Arithmetic.** 12 × £45.00 = £540.00 ✓; VAT at 20% × £540.00 = £108.00 ✓; net £540.00 + VAT £108.00 = £648.00 ✓, matching "Total payable: £648.00".

```
[pass] Arithmetic — the line, the VAT total and the gross total recompute exactly [reg 14(1)(h)]
```

**Verdict: NON-COMPLIANT — defective particulars** — invalid-invoice: 0 · defective-field: 1 · advisory: 0 · passes: 15

---

## 4. fixtures/broken-missing-unit-price.md — CN-118

**Invoice:** fixtures/broken-missing-unit-price.md

**Intake.** Document headed "INVOICE — CN-118" from Quillmark Consulting Ltd (Suite 2, Example House, Mockton MK1 5YY) to Harrold & Vane Ltd, sterling, gross "Total payable: £3,780.00"; time of supply 31 August 2026, date of issue 1 September 2026. It is headed as an invoice and carries positive amounts, so the CN- prefix is read as the issuer's series label and nothing more; nothing on the document marks it as anything other than an invoice. The document is not endorsed "This is not a VAT invoice", so reg 14(3) is not engaged.

**Classification.** Gross consideration exceeds £250, so the full checklist applies [reg 14(1)]. GB-prefixed supplier number and a UK customer address, so [reg 14(2)] is not engaged.

**Checklist.**

```
[pass] Invoice reference — "CN-118" is present, in a format consistent with a sequential series; whether the series is unbroken across the issuer's full run cannot be shown by one document [reg 14(1)(a)]
[pass] Time of supply — "Time of supply: 31 August 2026" [reg 14(1)(b)]
[pass] Date of issue — "Date of issue: 1 September 2026", stated separately from the time of supply [reg 14(1)(c)]
[pass] Supplier particulars — "Quillmark Consulting Ltd", "Suite 2, Example House, Mockton MK1 5YY" and "VAT registration number: GB 222 3333 44" all present [reg 14(1)(d)]
[pass] Customer particulars — "Harrold & Vane Ltd" at "9 Placeholder Row, Mockton MK9 2YY" [reg 14(1)(e)]
[pass] Description — "Systems migration consultancy, August 2026", sufficient to identify the services [reg 14(1)(g)]
[pass] Per description: extent (18 hours), VAT rate (20%) and net amount (£3,150.00) shown [reg 14(1)(h)]
[pass] Gross total payable excluding VAT — "Total net: £3,150.00" [reg 14(1)(i)]
[pass] Cash discount — ruled out: no discount or settlement terms are mentioned anywhere on the invoice, and a rate is only required where one is offered [reg 14(1)(j)]
[pass] Total VAT chargeable in sterling — "Total VAT: £630.00" [reg 14(1)(l)]
[defective-field] Unit price — the line table has no unit-price column (its headings are Extent, Description, Net, VAT rate and VAT) and no hourly rate is stated anywhere on the document; the net of "£3,150.00" for "18 hours" implies £175.00 per hour, but an implied figure is not a stated one and the regulation requires "the unit price" — correct on reissue or by supplementary document showing the hourly rate, and raise with the issuer's bookkeeper [reg 14(1)(m)]
[pass] Margin scheme — ruled out: no works of art, antiques, collectors' items, second-hand goods or tour-operator wording anywhere on the invoice; consultancy services are not a margin-scheme category [reg 14(1)(n)]
[pass] Reverse charge — ruled out: the customer is charged VAT directly at "20%" rather than the supplier shifting the liability, so the person supplied is not the one liable to account for the tax [reg 14(1)(o)]
[pass] Free zone — ruled out: nothing on the invoice places the supply within Item 1 of Group 22 of Schedule 8 (free zones) [reg 14(1)(p)]
[pass] Exempt/zero-rated distinction — ruled out: the single line is charged at the standard 20% rate, so there is no exempt or zero-rated line to distinguish [reg 14(4)]
```

**Arithmetic.** The line cannot be recomputed as quantity × unit price because no unit price is stated; £3,150.00 ÷ 18 hours = £175.00 per hour exactly, so the stated net is at least consistent with a whole-pound hourly rate. VAT at 20% × £3,150.00 = £630.00 ✓; net £3,150.00 + VAT £630.00 = £3,780.00 ✓, matching "Total payable: £3,780.00".

```
[pass] Arithmetic — the VAT total and the gross total recompute exactly from the stated net; the line itself can only be checked for divisibility because the unit price is missing (the finding above) [reg 14(1)(h)]
```

**Verdict: NON-COMPLIANT — defective particulars** — invalid-invoice: 0 · defective-field: 1 · advisory: 0 · passes: 15

---

## 5. fixtures/broken-missing-vat-number.md — INV-2044

**Invoice:** fixtures/broken-missing-vat-number.md

**Intake.** Sales invoice INV-2044 from Bluewharf Joinery Ltd (14 Sample Wharf, Testborough TB1 4XX) to Harrold & Vane Ltd, sterling, gross "Total payable: £912.00"; time of supply 26 August 2026, date of issue 27 August 2026. The document is not endorsed "This is not a VAT invoice", so reg 14(3) is not engaged.

**Classification.** Gross consideration exceeds £250, so the full checklist applies [reg 14(1)]. No registration number of any prefix appears on the document (the finding below) and the customer address is a UK one, so nothing engages [reg 14(2)].

**Checklist.**

```
[pass] Invoice reference — "INV-2044" is present, in a format consistent with a sequential series; whether the series is unbroken across the issuer's full run cannot be shown by one document [reg 14(1)(a)]
[pass] Time of supply — "Time of supply: 26 August 2026" [reg 14(1)(b)]
[pass] Date of issue — "Date of issue: 27 August 2026", stated separately from the time of supply [reg 14(1)(c)]
[invalid-invoice] Supplier block — no VAT registration number appears anywhere on the document; the block reads "Bluewharf Joinery Ltd" then "14 Sample Wharf, Testborough TB1 4XX" and stops, so the name and address are present but the third required particular is missing — reissue showing the supplier's VAT registration number; until then the customer's input tax evidence is at risk [reg 14(1)(d); 700/21 §4.1]
[pass] Customer particulars — "Harrold & Vane Ltd" at "9 Placeholder Row, Mockton MK9 2YY" [reg 14(1)(e)]
[pass] Description — "Window seat units, oak veneer", sufficient to identify the goods [reg 14(1)(g)]
[pass] Per description: quantity (4), VAT rate (20%) and net amount (£760.00) shown [reg 14(1)(h)]
[pass] Gross total payable excluding VAT — "Total net: £760.00" [reg 14(1)(i)]
[pass] Cash discount — ruled out: no discount or settlement terms are mentioned anywhere on the invoice, and a rate is only required where one is offered [reg 14(1)(j)]
[pass] Total VAT chargeable in sterling — "Total VAT: £152.00" [reg 14(1)(l)]
[pass] Unit price — "£190.00" per unit [reg 14(1)(m)]
[pass] Margin scheme — ruled out: no works of art, antiques, collectors' items, second-hand goods or tour-operator wording anywhere on the invoice; oak-veneer window seat units carry no second-hand or other margin-scheme indication [reg 14(1)(n)]
[pass] Reverse charge — ruled out: the customer is charged VAT directly at "20%" rather than the supplier shifting the liability, so the person supplied is not the one liable to account for the tax [reg 14(1)(o)]
[pass] Free zone — ruled out: nothing on the invoice places the supply within Item 1 of Group 22 of Schedule 8 (free zones) [reg 14(1)(p)]
[pass] Exempt/zero-rated distinction — ruled out: the single line is charged at the standard 20% rate, so there is no exempt or zero-rated line to distinguish [reg 14(4)]
```

**Arithmetic.** 4 × £190.00 = £760.00 ✓; VAT at 20% × £760.00 = £152.00 ✓; net £760.00 + VAT £152.00 = £912.00 ✓, matching "Total payable: £912.00".

```
[pass] Arithmetic — the line, the VAT total and the gross total recompute exactly [reg 14(1)(h)]
```

**Verdict: NON-COMPLIANT — invalid invoice** — invalid-invoice: 1 · defective-field: 0 · advisory: 0 · passes: 15

---

## 6. fixtures/broken-reverse-charge-wording.md — SC-0912

**Invoice:** fixtures/broken-reverse-charge-wording.md

**Intake.** Sales invoice SC-0912 from Mortarline Groundworks Ltd (The Yard, Fictive Lane, Testborough TB3 1XX) to Harrold & Vane Ltd, described on the invoice as "(main contractor, VAT-registered, CIS-registered)"; sterling; gross "Total payable: £4,200.00" with "Total VAT: £0.00" and the closing note "VAT not charged."; time of supply and date of issue both 22 August 2026. The document is not endorsed "This is not a VAT invoice", so reg 14(3) is not engaged.

**Classification.** Gross consideration exceeds £250, so the full checklist applies [reg 14(1)]. On the invoice's own facts — construction groundworks supplied by a subcontractor to a customer the invoice itself labels a VAT-registered, CIS-registered main contractor, with no VAT charged — the document presents a supply where the person supplied is liable to pay the tax, so the reverse-charge reference requirement is engaged [reg 14(1)(o)]. GB-prefixed supplier number and a UK customer address, so [reg 14(2)] is not engaged.

**Checklist.**

```
[pass] Invoice reference — "SC-0912" is present, in a format consistent with a sequential series; whether the series is unbroken across the issuer's full run cannot be shown by one document [reg 14(1)(a)]
[pass] Time of supply — "Time of supply: 22 August 2026" [reg 14(1)(b)]
[pass] Date of issue — "Date of issue: 22 August 2026", same day as the supply, stated [reg 14(1)(c)]
[pass] Supplier particulars — "Mortarline Groundworks Ltd", "The Yard, Fictive Lane, Testborough TB3 1XX" and "VAT registration number: GB 777 8888 99" all present [reg 14(1)(d)]
[pass] Customer particulars — "Harrold & Vane Ltd" at "9 Placeholder Row, Mockton MK9 2YY" [reg 14(1)(e)]
[pass] Description — "Groundworks at Plot 7, Mockton site — labour and materials, per agreed schedule", sufficient to identify the services [reg 14(1)(g)]
[pass] Per description: quantity (1) and net amount (£4,200.00) shown; the VAT rate column shows only a dash, which is the reverse-charge treatment whose missing reference is the finding at (o) below — no separate defect is raised on the rate, because what rate a reverse-charge line must display turns on guidance not shipped in reference/ [reg 14(1)(h)]
[pass] Gross total payable excluding VAT — "Total net: £4,200.00" [reg 14(1)(i)]
[pass] Cash discount — ruled out: no discount or settlement terms are mentioned anywhere on the invoice, and a rate is only required where one is offered [reg 14(1)(j)]
[pass] Total VAT chargeable in sterling — "Total VAT: £0.00", stated in sterling and consistent with the supplier charging no VAT on a supply the customer accounts for [reg 14(1)(l)]
[pass] Unit price — "£4,200.00" for the single agreed-schedule supply [reg 14(1)(m)]
[pass] Margin scheme — ruled out: no works of art, antiques, collectors' items, second-hand goods or tour-operator wording anywhere on the invoice; groundworks labour and materials are not a margin-scheme category [reg 14(1)(n)]
[invalid-invoice] VAT treatment wording — the invoice charges no VAT and says only "VAT not charged."; where the invoice relates to a supply on which the person supplied is liable to pay the tax it must state the reference "reverse charge", and this document nowhere does — reissue stating "reverse charge" so the customer knows the VAT is theirs to account for; until then the document misstates the VAT position and the customer's input tax evidence is at risk [reg 14(1)(o)]
[pass] Free zone — ruled out: nothing on the invoice places the supply within Item 1 of Group 22 of Schedule 8 (free zones) [reg 14(1)(p)]
[pass] Exempt/zero-rated distinction — ruled out: the single line is a reverse-charge construction supply, not an exempt or zero-rated one, so there is nothing to distinguish [reg 14(4)]
```

**Arithmetic.** Single line: 1 × £4,200.00 = £4,200.00 ✓; VAT shown as £0.00; £4,200.00 + £0.00 = £4,200.00 ✓, matching "Total payable: £4,200.00". Internally consistent with a reverse-charge treatment — which is exactly why the missing reference matters: nothing on the face of the document tells the customer that the VAT is theirs to account for.

```
[pass] Arithmetic — the line and the totals recompute exactly [reg 14(1)(h)]
```

**Scope note.** HMRC's construction reverse-charge guidance (VAT Notice 735) is not shipped in reference/, so this audit cites only reg 14(1)(o) for the wording and does not say what fuller wording or rate display that notice may call for.

**Verdict: NON-COMPLIANT — invalid invoice** — invalid-invoice: 1 · defective-field: 0 · advisory: 0 · passes: 15

---

## 7. fixtures/broken-simplified-over-limit.md — 0523

**Invoice:** fixtures/broken-simplified-over-limit.md

**Intake.** Document headed "RECEIPT / VAT INVOICE — 0523" from Sparkfield Electrical Ltd (Unit 3, Mocklands Trading Estate, Testborough TB2 8XX); no customer named; sterling; one date, "Date of supply: 30 August 2026"; a single VAT-inclusive figure, "Total payable (including VAT): £474.00", with "Amount includes VAT at 20%: gross £474.00 at standard rate." The document is not endorsed "This is not a VAT invoice", so reg 14(3) is not engaged.

**Classification.** Gross consideration £474.00 exceeds £250, so the full checklist applies [reg 14(1)], and the simplified format the issuer has used is itself a finding (first line below). The issuer is an electrical contractor and nowhere describes itself as a retailer, so the relaxation it appears to have relied on is the simplified invoice [reg 16A] under the notice's non-retailer paragraph [700/21 §4.5] — not available at this value. That paragraph also allows, above £250, "a modified VAT invoice, showing VAT inclusive rather than VAT exclusive values"; the particulars of a modified invoice are not shipped in reference/, so this audit walks reg 14(1), the only full checklist shipped, and the VAT-exclusive-figure findings at (h), (i) and (m) below are to be read with that unshipped alternative in mind. GB-prefixed supplier number and no customer shown, so [reg 14(2)] is not engaged.

```
[invalid-invoice] Format — the document is a simplified-format receipt (supplier block, one date, one description, one VAT-inclusive total and a rate) for a supply whose gross consideration is "£474.00"; the simplified particulars are available only where the consideration does not exceed £250, and above that the notice requires "a full VAT invoice or a modified VAT invoice" — reissue as a full VAT invoice showing every reg 14(1) particular; until then the customer's input tax evidence is at risk [reg 16A; 700/21 §4.5]
```

**Checklist.**

```
[pass] Invoice reference — "0523" is present, in a format consistent with a sequential series; whether the series is unbroken across the issuer's full run cannot be shown by one document [reg 14(1)(a)]
[pass] Time of supply — "Date of supply: 30 August 2026" [reg 14(1)(b)]
[pass] Date of issue — the document carries one date, "Date of supply: 30 August 2026"; a receipt is issued at the transaction, nothing on the document indicates a later issue date, and the notice requires a separate date of issue only "where different to the time of supply" [reg 14(1)(c); 700/21 §4.1]
[pass] Supplier particulars — "Sparkfield Electrical Ltd", "Unit 3, Mocklands Trading Estate, Testborough TB2 8XX" and "VAT No: GB 444 5555 66" all present [reg 14(1)(d)]
[invalid-invoice] Customer particulars — no customer name or address appears anywhere on the document (there is no customer block at all); a full VAT invoice must state the name and address of the person to whom the services are supplied — reissue showing the customer's name and address; until then the customer's input tax evidence is at risk [reg 14(1)(e)]
[pass] Description — "Rewire of garage supply, replacement distribution board and testing", sufficient to identify the services [reg 14(1)(g)]
[defective-field] Per description — the extent (one described job) and the VAT rate (20%) are shown, but no amount payable excluding VAT is stated for the description: the only figure is the VAT-inclusive "£474.00" (£395.00 excluding VAT by recomputation) — correct on reissue by stating the VAT-exclusive amount for the description, and raise with the issuer's bookkeeper; severity by nearest analogue in the table, a missing per-description particular under this sub-paragraph [reg 14(1)(h)]
[defective-field] Gross total payable excluding VAT — not stated; the document gives only "Total payable (including VAT): £474.00" (£395.00 excluding VAT by recomputation) — correct on reissue by stating the VAT-exclusive total, and raise with the issuer's bookkeeper [reg 14(1)(i)]
[pass] Cash discount — ruled out: no discount or settlement terms are mentioned anywhere on the document, and a rate is only required where one is offered [reg 14(1)(j)]
[invalid-invoice] Total VAT chargeable in sterling — no VAT amount is stated anywhere; "Amount includes VAT at 20%: gross £474.00 at standard rate." gives the rate but not the amount, and the total amount of VAT chargeable must be stated, "expressed in sterling" (£79.00 by recomputation) — reissue showing the sterling VAT total; until then the customer's input tax evidence is at risk [reg 14(1)(l); 700/21 §4.1]
[defective-field] Unit price — not stated; the single job is priced only VAT-inclusive at "£474.00", and the notice's own worked example prices each unit exclusive of VAT, so the £395.00 unit price is implied but nowhere shown — correct on reissue by stating the unit price, and raise with the issuer's bookkeeper [reg 14(1)(m)]
[pass] Margin scheme — ruled out: no works of art, antiques, collectors' items, second-hand goods or tour-operator wording anywhere on the document; electrical rewiring services are not a margin-scheme category [reg 14(1)(n)]
[pass] Reverse charge — ruled out on the face of the document: the supplier charges VAT within the price ("includes VAT at 20%") rather than shifting the liability; whether the unnamed customer's status could have called for a different treatment is a liability question outside this auditor's scope [reg 14(1)(o)]
[pass] Free zone — ruled out: nothing on the document places the supply within Item 1 of Group 22 of Schedule 8 (free zones) [reg 14(1)(p)]
[pass] Exempt/zero-rated distinction — ruled out: the single supply is stated "at standard rate", so there is no exempt or zero-rated element to distinguish [reg 14(4)]
```

**Arithmetic.** The single stated figure is VAT-inclusive: £474.00 ÷ 1.2 = £395.00 net; VAT at 20% × £395.00 = £79.00; £395.00 + £79.00 = £474.00 ✓. The stated gross therefore divides cleanly at the stated rate; there are no line nets, no VAT figure and no unit price on the document to recompute against (each reported above).

```
[pass] Arithmetic — the single gross figure is internally consistent with the stated 20% rate (£395.00 net + £79.00 VAT = £474.00) [reg 14(1)(h)]
```

**Verdict: NON-COMPLIANT — invalid invoice** — invalid-invoice: 3 · defective-field: 3 · advisory: 0 · passes: 11

---

## 8. fixtures/broken-vat-total-in-euros.md — INV-2047

**Invoice:** fixtures/broken-vat-total-in-euros.md

**Intake.** Sales invoice INV-2047 from Bluewharf Joinery Ltd (14 Sample Wharf, Testborough TB1 4XX) to Harrold & Vane Ltd, euros throughout — "All amounts in euros (contract currency). Exchange rate applied: £1 = €1.15." — gross "Total payable: €2,152.80"; time of supply and date of issue both 29 August 2026. The document is not endorsed "This is not a VAT invoice", so reg 14(3) is not engaged.

**Classification.** Gross consideration €2,152.80 (£1,872.00 at the invoice's own stated rate) is well over £250, so the full checklist applies [reg 14(1)]. GB-prefixed supplier number and a UK customer address, so [reg 14(2)] is not engaged.

**Checklist.**

```
[pass] Invoice reference — "INV-2047" is present, in a format consistent with a sequential series; whether the series is unbroken across the issuer's full run cannot be shown by one document [reg 14(1)(a)]
[pass] Time of supply — "Time of supply: 29 August 2026" [reg 14(1)(b)]
[pass] Date of issue — "Date of issue: 29 August 2026", same day as the supply, stated [reg 14(1)(c)]
[pass] Supplier particulars — "Bluewharf Joinery Ltd", "14 Sample Wharf, Testborough TB1 4XX" and "VAT registration number: GB 111 2222 33" all present [reg 14(1)(d)]
[pass] Customer particulars — "Harrold & Vane Ltd" at "9 Placeholder Row, Mockton MK9 2YY" [reg 14(1)(e)]
[pass] Description — "Bespoke shelving bays, oak", sufficient to identify the goods [reg 14(1)(g)]
[advisory] Currency of net amounts — the line and the totals are in euros ("Total net: €1,794.00"); the regulation permits the net amounts to be "expressed in any currency", so this is not a defect — no action needed [reg 14(1)(h)]
[pass] Per description: quantity (8), VAT rate (20%) and net amount (€1,794.00) shown [reg 14(1)(h)]
[pass] Gross total payable excluding VAT — "Total net: €1,794.00" [reg 14(1)(i)]
[pass] Cash discount — ruled out: no discount or settlement terms are mentioned anywhere on the invoice, and a rate is only required where one is offered [reg 14(1)(j)]
[invalid-invoice] VAT total — "Total VAT: €358.80" appears only in euros; the total amount of VAT chargeable must be "expressed in sterling" whatever the invoice currency — reissue showing the sterling VAT total (at the invoice's own stated rate of £1 = €1.15, €358.80 = £312.00); until then the customer's input tax evidence is at risk [reg 14(1)(l); 700/21 §4.1]
[pass] Unit price — "€224.25" per bay [reg 14(1)(m)]
[pass] Margin scheme — ruled out: no works of art, antiques, collectors' items, second-hand goods or tour-operator wording anywhere on the invoice; bespoke oak shelving carries no second-hand or other margin-scheme indication [reg 14(1)(n)]
[pass] Reverse charge — ruled out: the customer is charged VAT directly at "20%" rather than the supplier shifting the liability, so the person supplied is not the one liable to account for the tax [reg 14(1)(o)]
[pass] Free zone — ruled out: nothing on the invoice places the supply within Item 1 of Group 22 of Schedule 8 (free zones) [reg 14(1)(p)]
[pass] Exempt/zero-rated distinction — ruled out: the single line is charged at the standard 20% rate, so there is no exempt or zero-rated line to distinguish [reg 14(4)]
```

**Arithmetic.** 8 × €224.25 = €1,794.00 ✓; VAT at 20% × €1,794.00 = €358.80 ✓; €1,794.00 + €358.80 = €2,152.80 ✓, matching "Total payable: €2,152.80". At the stated rate £1 = €1.15 the sterling equivalents are net £1,560.00, VAT £312.00, gross £1,872.00 — none of which appears on the document.

```
[pass] Arithmetic — internally exact in euros [reg 14(1)(h)]
```

**Verdict: NON-COMPLIANT — invalid invoice** — invalid-invoice: 1 · defective-field: 0 · advisory: 1 · passes: 15

---

## 9. fixtures/compliant-full-invoice.md — INV-2041

**Invoice:** fixtures/compliant-full-invoice.md

**Intake.** Sales invoice INV-2041 from Bluewharf Joinery Ltd (14 Sample Wharf, Testborough TB1 4XX) to Harrold & Vane Ltd, sterling, gross "Total payable: £1,456.80"; time of supply 12 August 2026, date of issue 14 August 2026; payment terms "Payment within 30 days to the account below. No settlement discount offered." followed by bank details. The document is not endorsed "This is not a VAT invoice", so reg 14(3) is not engaged.

**Classification.** Gross consideration exceeds £250, so the full checklist applies [reg 14(1)]. GB-prefixed supplier number and a UK customer address, so [reg 14(2)] is not engaged.

**Checklist.**

```
[pass] Invoice reference — "INV-2041" is present, in a format consistent with a sequential series; whether the series is unbroken across the issuer's full run cannot be shown by one document [reg 14(1)(a)]
[pass] Time of supply — "Time of supply: 12 August 2026" [reg 14(1)(b)]
[pass] Date of issue — "Date of issue: 14 August 2026", stated separately from the time of supply [reg 14(1)(c)]
[pass] Supplier particulars — "Bluewharf Joinery Ltd", "14 Sample Wharf, Testborough TB1 4XX" and "VAT registration number: GB 111 2222 33" all present [reg 14(1)(d)]
[pass] Customer particulars — "Harrold & Vane Ltd" at "9 Placeholder Row, Mockton MK9 2YY" [reg 14(1)(e)]
[pass] Description — "Oak door blanks, 838mm", "Site fitting labour" and "Brass hinge sets", each sufficient to identify the goods or services [reg 14(1)(g)]
[pass] Per description: quantity/extent (6, 2 days and 10), VAT rate (20% on every line) and net amount (£510.00, £640.00 and £64.00) all shown [reg 14(1)(h)]
[pass] Gross total payable excluding VAT — "Total net: £1,214.00" [reg 14(1)(i)]
[pass] Cash discount — none offered ("No settlement discount offered"), so no rate is required [reg 14(1)(j)]
[pass] Total VAT chargeable in sterling — "Total VAT: £242.80" [reg 14(1)(l)]
[pass] Unit price — "£85.00", "£320.00 per day" and "£6.40", shown for every line [reg 14(1)(m)]
[pass] Margin scheme — ruled out: no works of art, antiques, collectors' items, second-hand goods or tour-operator wording anywhere on the invoice; door blanks, hinge sets and fitting labour carry no margin-scheme indication [reg 14(1)(n)]
[pass] Reverse charge — ruled out: the customer is charged VAT directly at "20%" on every line rather than the supplier shifting the liability, so the person supplied is not the one liable to account for the tax [reg 14(1)(o)]
[pass] Free zone — ruled out: nothing on the invoice places the supply within Item 1 of Group 22 of Schedule 8 (free zones) [reg 14(1)(p)]
[pass] Exempt/zero-rated distinction — ruled out: every line is charged at the standard 20% rate, so there is no exempt or zero-rated line to distinguish [reg 14(4)]
```

**Arithmetic.** 6 × £85.00 = £510.00 (VAT £102.00) ✓; 2 × £320.00 = £640.00 (VAT £128.00) ✓; 10 × £6.40 = £64.00 (VAT £12.80) ✓. Net £510.00 + £640.00 + £64.00 = £1,214.00 ✓; VAT £102.00 + £128.00 + £12.80 = £242.80 ✓, which is also 20% of £1,214.00; gross £1,214.00 + £242.80 = £1,456.80 ✓, matching "Total payable: £1,456.80".

```
[pass] Arithmetic — all lines, the VAT total and the gross total recompute exactly [reg 14(1)(h)]
```

**Verdict: COMPLIANT** — invalid-invoice: 0 · defective-field: 0 · advisory: 0 · passes: 16

---

## 10. fixtures/compliant-simplified-invoice.md — 0517

**Invoice:** fixtures/compliant-simplified-invoice.md

**Intake.** Document headed "RECEIPT / VAT INVOICE — 0517" from Sparkfield Electrical Ltd (Unit 3, Mocklands Trading Estate, Testborough TB2 8XX); no customer named; sterling; one date, "Date of supply: 28 August 2026"; "Total payable (including VAT): £186.00" with "Amount includes VAT at 20%: gross £186.00 at standard rate." The document is not endorsed "This is not a VAT invoice", so reg 14(3) is not engaged.

**Classification.** Gross consideration £186.00 is £250 or less. The issuer is an electrical contractor and nowhere describes itself as a retailer, so the document may stand as a simplified invoice and is audited against the simplified particulars [reg 16A]; the notice's non-retailer paragraph is [700/21 §4.5]. The document carries exactly the simplified particulars and no more, so the issuer clearly intended a simplified invoice and there is no escalation to the full checklist. A customer's name, a date of issue, a VAT-exclusive amount, a unit price and a separate VAT figure are not among the reg 16A particulars, so their absence is not a finding here. The full-invoice distinguishing rule [reg 14(4)] applies only to an invoice carrying the reg 14(1) particulars; its counterpart for this document is the prohibition on exempt supplies, carried for non-retailers by the notice's simplified paragraph and checked in the special references below.

**Checklist.**

```
[pass] Supplier particulars — "Sparkfield Electrical Ltd", "Unit 3, Mocklands Trading Estate, Testborough TB2 8XX" and "VAT No: GB 444 5555 66" all present [reg 16A(a)]
[pass] Time of supply — "Date of supply: 28 August 2026" [reg 16A(b)]
[pass] Description — "Replacement of consumer unit fuse carrier and safety check", sufficient to identify the services [reg 16A(c)]
[pass] Total amount payable including VAT — "Total payable (including VAT): £186.00" [reg 16A(d)]
[pass] Per rate of VAT chargeable, gross including VAT and the rate — for the one chargeable rate the document states "Amount includes VAT at 20%: gross £186.00 at standard rate." [reg 16A(e)]
[pass] Margin scheme — ruled out: no works of art, antiques, collectors' items, second-hand goods or tour-operator wording anywhere on the document; electrical repair services are not a margin-scheme category [reg 14(1)(n)]
[pass] Reverse charge — ruled out on the face of the document: the supplier charges VAT within the price ("includes VAT at 20%") rather than shifting the liability; whether the unnamed customer's status could have called for a different treatment is a liability question outside this auditor's scope [reg 14(1)(o)]
[pass] Free zone — ruled out: nothing on the document places the supply within Item 1 of Group 22 of Schedule 8 (free zones) [reg 14(1)(p)]
[pass] No exempt supply — ruled out: the single supply is stated "at standard rate" and the document contains no reference to any exempt supply, which "must not be included in this type of VAT invoice" [reg 16(2); 700/21 §4.5]
```

**Arithmetic.** £186.00 ÷ 1.2 = £155.00 net; VAT at 20% × £155.00 = £31.00; £155.00 + £31.00 = £186.00 ✓. The single gross figure divides cleanly at the stated rate; a separate VAT figure is neither required nor stated.

```
[pass] Arithmetic — the gross figure is internally consistent with the stated 20% rate (£155.00 net + £31.00 VAT = £186.00) [reg 16A(e)]
```

**Verdict: COMPLIANT** — invalid-invoice: 0 · defective-field: 0 · advisory: 0 · passes: 10

---

## Summary

The two batch-only checks in rules.md §6 were run across all ten documents and neither fires: no reference number appears on more than one document (INV-2049, CN-118, INV-2044, SC-0912, 0523, INV-2047, INV-2041 and 0517 are all distinct, one document is unnumbered and the till receipt carries none), and no supplier shows two different VAT registration numbers across the batch (Bluewharf Joinery Ltd shows GB 111 2222 33 on every document where it shows a number at all; Sparkfield Electrical Ltd shows GB 444 5555 66 on both of its documents). Nothing else from one invoice was carried into another.

| Invoice | Verdict | invalid · defective · advisory · passes | Headline finding |
|---|---|---|---|
| broken-arithmetic-vat-total.md (INV-2049) | NON-COMPLIANT — invalid invoice | 1 · 0 · 0 · 15 | "Total VAT: £276.00" does not follow from the lines, which give £230.00 [reg 14(1)(h); reg 14(1)(l)] |
| broken-exempt-on-simplified.md (Kettle Lane till receipt) | NON-COMPLIANT — invalid invoice | 1 · 0 · 0 · 9 | Exempt line "First class postage stamps, book of 50 (exempt)" on a retailer's invoice [reg 16(2); 700/21 §4.5] |
| broken-missing-sequential-number.md (unnumbered) | NON-COMPLIANT — defective particulars | 0 · 1 · 0 · 15 | No reference number anywhere on the invoice [reg 14(1)(a)] |
| broken-missing-unit-price.md (CN-118) | NON-COMPLIANT — defective particulars | 0 · 1 · 0 · 15 | Unit price (hourly rate) not stated for "18 hours" [reg 14(1)(m)] |
| broken-missing-vat-number.md (INV-2044) | NON-COMPLIANT — invalid invoice | 1 · 0 · 0 · 15 | No supplier VAT registration number anywhere on the document [reg 14(1)(d); 700/21 §4.1] |
| broken-reverse-charge-wording.md (SC-0912) | NON-COMPLIANT — invalid invoice | 1 · 0 · 0 · 15 | "reverse charge" reference missing; the invoice says only "VAT not charged." [reg 14(1)(o)] |
| broken-simplified-over-limit.md (0523) | NON-COMPLIANT — invalid invoice | 3 · 3 · 0 · 11 | Simplified-format receipt for a "£474.00" supply, over the £250 limit [reg 16A; 700/21 §4.5] |
| broken-vat-total-in-euros.md (INV-2047) | NON-COMPLIANT — invalid invoice | 1 · 0 · 1 · 15 | "Total VAT: €358.80" only in euros, not sterling [reg 14(1)(l); 700/21 §4.1] |
| compliant-full-invoice.md (INV-2041) | COMPLIANT | 0 · 0 · 0 · 16 | None — every applicable check passed, e.g. "Total VAT: £242.80" in sterling [reg 14(1)(l)] |
| compliant-simplified-invoice.md (0517) | COMPLIANT | 0 · 0 · 0 · 10 | None — every applicable check passed, e.g. "Total payable (including VAT): £186.00" [reg 16A(d)] |

---

## META

**(a) Count and depth.** Ten invoices audited, every file in fixtures/, in directory order. None was given a shorter walk than the first: each of the seven full-checklist documents has one line for every applicable reg 14(1) particular (a)–(p) less the revoked (f) and (k), plus 14(4) and an arithmetic line; the two documents audited as simplified or retailer's invoices have one line for each of reg 16A(a)–(e) or reg 16(1)(a)–(e), the three reg 14(1)(n)–(p) references ruled out on their facts, the reg 16(2) exempt-supply check and an arithmetic line. The pass counts differ across invoices only because the applicable checklists differ (16 for a full invoice with a cash-discount statement, 15 or 16 lines for the others, 9–10 for the short-form documents) or because a line is a finding rather than a pass, never because a later audit was abbreviated. The two example-covered fixtures (INV-2047 and SC-0912) were walked independently and each carries three lines — (h), (j) and (l) — that examples.md omits, because rules.md requires one line per particular.

**(b) Cross-invoice influence.** None on any finding or pass. The only cross-document reading was the two checks rules.md §6 expressly permits — duplicate reference numbers and one supplier with two VAT numbers — both run over the batch and both negative, reported once in the Summary. In particular, INV-2044's missing VAT number was reported as missing and not filled in from the four other Bluewharf documents, and 0523's simplified format was judged on its own £474.00 gross, not by comparison with 0517.

**(c) Files read, in order.** CLAUDE.md → identity.md → rules.md → reference/CATALOG.md (with a directory listing of the root, fixtures/ and reference/) → examples.md → the ten fixtures in alphabetical order (broken-arithmetic-vat-total.md, broken-exempt-on-simplified.md, broken-missing-sequential-number.md, broken-missing-unit-price.md, broken-missing-vat-number.md, broken-reverse-charge-wording.md, broken-simplified-over-limit.md, broken-vat-total-in-euros.md, compliant-full-invoice.md, compliant-simplified-invoice.md) → reference/vat-regulations-1995-reg-14.md → reference/vat-notice-700-21-invoicing.md → reference/vat-regulations-1995-reg-16.md → reference/vat-regulations-1995-reg-16A.md → the docstring and `main()` of tools/check_citations.py (only to learn how to run it against the draft; it and tools/check_reference_integrity.py were then executed, and both passed — 186 citations resolved, 200 quoted spans grounded, five reference cards matching their recorded hashes). Deliberately left unread: everything under judge-answer-key/; reference/vat-regulations-1995-reg-13.md (no fixture raised whether an invoice was required at all) and reference/MANIFEST.md (consumed only by the integrity script); AGENTS.md, README.md, docs/, .github/ and the remaining tools/ scripts, none of which CLAUDE.md routes an audit to.
