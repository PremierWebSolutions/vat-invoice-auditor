# Worked example audits

Three audits of invoices from [fixtures/](fixtures/), in the exact shape every audit must take: the audit-order steps from [rules.md](rules.md), one line per check, citation on every line, passes reported as prominently as failures.

---

## Example 1 — a compliant full invoice

**Invoice:** [fixtures/compliant-full-invoice.md](fixtures/compliant-full-invoice.md)

**Intake.** Sales invoice INV-2041 from Bluewharf Joinery Ltd to Harrold & Vane Ltd, sterling, gross £1,456.80.

**Classification.** Gross consideration exceeds £250, so the full checklist applies [reg 14(1)].

**Checklist.**

```
[pass] Invoice reference — "INV-2041" is present, in a format consistent with a sequential series [reg 14(1)(a)]
[pass] Time of supply — "Time of supply: 12 August 2026" [reg 14(1)(b)]
[pass] Date of issue — "14 August 2026", stated separately from the time of supply [reg 14(1)(c)]
[pass] Supplier particulars — name, address and VAT registration number GB 111 2222 33 all present [reg 14(1)(d)]
[pass] Customer particulars — "Harrold & Vane Ltd, 9 Placeholder Row, Mockton MK9 2YY" [reg 14(1)(e)]
[pass] Description — three lines, each sufficient to identify the goods or services [reg 14(1)(g)]
[pass] Per description: quantity/extent, VAT rate and net amount all shown [reg 14(1)(h)]
[pass] Gross total payable excluding VAT — "Total net: £1,214.00" [reg 14(1)(i)]
[pass] Cash discount — none offered ("No settlement discount offered"), so no rate is required [reg 14(1)(j)]
[pass] Total VAT chargeable in sterling — "Total VAT: £242.80" [reg 14(1)(l)]
[pass] Unit price — shown for every line [reg 14(1)(m)]
[pass] Margin scheme — ruled out: no antiques, art, collectors' items or tour-operator
wording anywhere on the invoice, and the goods (door blanks, hinge sets) and labour are
not margin-scheme categories [reg 14(1)(n)]
[pass] Reverse charge — ruled out: the customer is charged VAT directly at "20%" on
every line rather than the supplier shifting the liability, so the customer is not the
person liable to account for the tax [reg 14(1)(o)]
[pass] Free zone — ruled out: nothing on the invoice or in the facts places the supply
within Item 1 of Group 22 of Schedule 8 (free zones) [reg 14(1)(p)]
[pass] Exempt/zero-rated distinction — ruled out: every line is charged at the standard
20% rate, so there is no exempt or zero-rated line to distinguish [reg 14(4)]
```

**Arithmetic.** 6 × £85.00 = £510.00 (VAT £102.00); 2 × £320.00 = £640.00 (VAT £128.00); 10 × £6.40 = £64.00 (VAT £12.80). Net £510.00 + £640.00 + £64.00 = £1,214.00 ✓; VAT £102.00 + £128.00 + £12.80 = £242.80 ✓ at 20%; total £1,456.80 ✓.

```
[pass] Arithmetic — all lines, the VAT total and the gross total recompute exactly [reg 14(1)(h)]
```

**Verdict: COMPLIANT** — invalid-invoice: 0 · defective-field: 0 · advisory: 0 · passes: 16

---

## Example 2 — foreign currency invoice, VAT total not in sterling

**Invoice:** [fixtures/broken-vat-total-in-euros.md](fixtures/broken-vat-total-in-euros.md)

**Intake.** Sales invoice INV-2047 from Bluewharf Joinery Ltd to Harrold & Vane Ltd, euros throughout, gross €2,152.80, stated rate £1 = €1.15.

**Classification.** Gross consideration well over £250 — full checklist [reg 14(1)].

**Checklist.**

```
[pass] Invoice reference — "INV-2047" is present, in a format consistent with a sequential series [reg 14(1)(a)]
[pass] Time of supply — "29 August 2026" [reg 14(1)(b)]
[pass] Date of issue — "29 August 2026", same day, stated [reg 14(1)(c)]
[pass] Supplier particulars — name, address, VAT registration number GB 111 2222 33 [reg 14(1)(d)]
[pass] Customer particulars — name and address present [reg 14(1)(e)]
[pass] Description — "Bespoke shelving bays, oak", sufficient [reg 14(1)(g)]
[advisory] Currency of net amounts — lines and totals are in euros ("Total net: €1,794.00");
the regulation permits net amounts "expressed in any currency", so this is not a defect —
no action needed [reg 14(1)(h)]
[pass] Per description: quantity (8), VAT rate (20%) and net amount shown [reg 14(1)(h)]
[pass] Gross total payable excluding VAT — "€1,794.00" [reg 14(1)(i)]
[pass] Cash discount — ruled out: no discount is mentioned anywhere on the invoice, and a
rate is only required where one is offered [reg 14(1)(j)]
[invalid-invoice] VAT total — "Total VAT: €358.80" appears only in euros; the total VAT
chargeable must be expressed in sterling whatever the invoice currency — reissue showing
the sterling VAT (at the invoice's own stated rate of £1 = €1.15, €358.80 = £312.00)
[reg 14(1)(l); 700/21 §4.1]
[pass] Unit price — "€224.25" per bay [reg 14(1)(m)]
[pass] Margin scheme — ruled out: no antiques, art, collectors' items or tour-operator
wording; bespoke oak shelving is not a margin-scheme category [reg 14(1)(n)]
[pass] Reverse charge — ruled out: the invoice charges VAT directly at 20% rather than
shifting the liability to the customer [reg 14(1)(o)]
[pass] Free zone — ruled out: nothing places the supply within Item 1 of Group 22 of
Schedule 8 (free zones) [reg 14(1)(p)]
[pass] Exempt/zero-rated distinction — ruled out: the single line is charged at the
standard 20% rate, so there is no exempt or zero-rated line to distinguish [reg 14(4)]
```

**Arithmetic.** 8 × €224.25 = €1,794.00 ✓; VAT at 20% = €358.80 ✓; total €2,152.80 ✓.

```
[pass] Arithmetic — internally exact in euros [reg 14(1)(h)]
```

**Verdict: NON-COMPLIANT — invalid invoice** — invalid-invoice: 1 · defective-field: 0 · advisory: 1 · passes: 15

---

## Example 3 — construction reverse charge without the required reference

**Invoice:** [fixtures/broken-reverse-charge-wording.md](fixtures/broken-reverse-charge-wording.md)

**Intake.** Sales invoice SC-0912 from Mortarline Groundworks Ltd (subcontractor) to Harrold & Vane Ltd, described on the invoice as a VAT-registered, CIS-registered main contractor. Gross £4,200.00, no VAT charged.

**Classification.** Gross over £250 — full checklist [reg 14(1)]. On the invoice's own facts — construction services supplied to a VAT- and CIS-registered contractor — this is a supply on which the person supplied is liable to account for the VAT, so the reverse-charge reference requirement is engaged [reg 14(1)(o)].

**Checklist.**

```
[pass] Invoice reference — "SC-0912" is present, in a format consistent with a sequential series [reg 14(1)(a)]
[pass] Time of supply — "22 August 2026" [reg 14(1)(b)]
[pass] Date of issue — "22 August 2026", stated [reg 14(1)(c)]
[pass] Supplier particulars — name, address, VAT registration number GB 777 8888 99 [reg 14(1)(d)]
[pass] Customer particulars — name and address present [reg 14(1)(e)]
[pass] Description — "Groundworks at Plot 7, Mockton site — labour and materials", sufficient [reg 14(1)(g)]
[defective-field] VAT treatment wording — the invoice charges no VAT and says only
"VAT not charged."; where the person supplied is liable to pay the tax the invoice must
state the reference "reverse charge", and this one nowhere does — correct on reissue so
the customer is told in terms to account for the VAT. Graded defective, not invalid: the
invoice shows no separate VAT amount (gross only), so there is nothing here a buyer could
wrongly reclaim, which is the risk that would make a reverse-charge defect invalid [reg 14(1)(o)]
[pass] Gross total payable excluding VAT — "£4,200.00" [reg 14(1)(i)]
[pass] Unit price — £4,200.00 for the single agreed-schedule supply [reg 14(1)(m)]
[pass] Margin scheme — ruled out: no antiques, art, collectors' items or tour-operator
wording; groundworks labour and materials are not a margin-scheme category [reg 14(1)(n)]
[pass] Free zone — ruled out: nothing places the supply within Item 1 of Group 22 of
Schedule 8 (free zones) [reg 14(1)(p)]
[pass] Exempt/zero-rated distinction — ruled out: the single line is a reverse-charge
construction supply, not an exempt or zero-rated one, so there is nothing to distinguish [reg 14(4)]
```

**Arithmetic.** Single line, £4,200.00, no VAT charged — internally consistent with a reverse-charge treatment. There is no separate VAT amount on the document, so nothing here could be wrongly reclaimed; the missing reference is a wording gap to correct, not a misstatement of the VAT.

```
[pass] Arithmetic — totals recompute [reg 14(1)(h)]
```

**Scope note.** HMRC's construction reverse-charge guidance (VAT Notice 735) recommends fuller wording, but that notice is not shipped in [reference/](reference/CATALOG.md) — so this audit cites only reg 14(1)(o) and says so, rather than citing from memory.

**Verdict: NON-COMPLIANT — defective particulars** — invalid-invoice: 0 · defective-field: 1 · advisory: 0 · passes: 12
