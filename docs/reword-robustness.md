# Reword robustness receipt

**Date:** 10 September 2026
**Prompted by:** a comment from a community member (Leo Saraiva) on this competition's own thread, reproduced here in full because the test is his:

> everyone will check the gate fires on a fixture broken on purpose. that only proves it can say no once. the harder version: keep one real violation intact and reword the surrounding text three ways. if the finding fires on only one of the three, the auditor is reading phrasing, not the provision. that is the failure nobody catches, because it looks exactly like a clean pass on the other two.

**Setup:** the same underlying defect — Bluewharf Joinery Ltd's invoice INV-2044 to Harrold & Vane Ltd, £912.00 gross, missing the supplier's VAT registration number — presented three different ways to three independent, freshly-started agent sessions, each with no memory of the others and no knowledge this was a reword test. Each was simply asked to audit the text pasted to it. The defect this tests is an *absence*, not a phrase, so the three variants don't reword a violating sentence (there is no sentence to reword) — they instead vary how the rest of the document is written and add one adversarial decoy, to test whether the finding survives changes that have nothing to do with the defect itself, and correctly rejects a look-alike that has everything to do with it.

- **Variant A — casual reformat.** The same facts as plain running prose with light structure, no bold headers, a different field order from any shipped fixture.
- **Variant B — decoy field.** The usual tabular layout, but with a **Companies House company registration number** (`08234567`) placed exactly where a VAT registration number would sit — a real, common confusion: two different registration schemes, formatted almost identically, one of them legally irrelevant to reg 14(1)(d).
- **Variant C — full prose.** No table, no headers, no bold — a single paragraph of formal prose carrying every fact, including the assertion that the supplier is *registered for VAT purposes* — true, but not a number, and not what the regulation requires.

## Result: fired correctly on all three

| Variant | VAT-number finding raised? | Cited reg 14(1)(d)? | Notable reasoning |
|---|---|---|---|
| A — casual reformat | Yes, invalid-invoice | Yes | Unaffected by the looser layout |
| B — decoy company number | Yes, invalid-invoice | Yes | Named the decoy explicitly as a different identifier that does not stand in for the required VAT registration number |
| C — full prose, registered for VAT purposes | Yes, invalid-invoice | Yes | Declined to treat the assertion as a substitute, since it supplies no actual number |

All three sessions reached the same verdict (NON-COMPLIANT — invalid invoice, invalid-invoice: 1 · defective-field: 0 · advisory: 0 · passes: 15) with the same arithmetic and the same fourteen other particulars passing. Nothing about the surface presentation moved the finding, and nothing about a plausible-looking decoy or a true-but-insufficient assertion satisfied it.

## Why it matters

A keyword or fixed-format matcher would have been vulnerable in at least two of these three variants: Variant B rewards anything that looks like a registration number sitting in the right visual position, and Variant C rewards any sentence containing "VAT" and "registered." Both would be a false pass. What held instead was reg 14(1)(d)'s actual requirement — a registration number stated *on the document* — checked against what the text actually contains, not against its shape. That is the specific failure mode this test exists to expose, run the way the comment asked: independently, cold, three ways, on the one kind of defect (an absence) that a real invoice audit most needs to get right regardless of how the invoice happens to be laid out.
