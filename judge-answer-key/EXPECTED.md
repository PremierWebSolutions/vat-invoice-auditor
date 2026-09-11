# Fixture answer sheet — for judges and testing only

This file lives outside [fixtures/](../fixtures/) on purpose, not just by instruction: a stranger who clones the repo and drops [identity.md](../identity.md), [rules.md](../rules.md), [examples.md](../examples.md) and [reference/](../reference/CATALOG.md) into a Claude project never has this folder in front of them at all. Its separateness is a folder position, not a request the auditor is trusted to honour — see [docs/decisions.md](../docs/decisions.md) for why that distinction matters. It contains the answers, so it never belongs beside the fixtures it grades. Every business, person, address, VAT number and bank detail in these fixtures is synthetic.

| Fixture | Designed outcome | Key finding(s) it must surface |
|---|---|---|
| [compliant-full-invoice.md](../fixtures/compliant-full-invoice.md) | COMPLIANT | All reg 14(1) particulars present; arithmetic exact [reg 14(1)] |
| [compliant-simplified-invoice.md](../fixtures/compliant-simplified-invoice.md) | COMPLIANT | £186.00 gross ≤ £250; all reg 16A(a)–(e) particulars present [reg 16A] |
| [broken-missing-sequential-number.md](../fixtures/broken-missing-sequential-number.md) | NON-COMPLIANT — defective particulars | No invoice number anywhere [reg 14(1)(a)] |
| [broken-missing-vat-number.md](../fixtures/broken-missing-vat-number.md) | NON-COMPLIANT — invalid invoice | Supplier VAT registration number absent [reg 14(1)(d)] |
| [broken-reverse-charge-wording.md](../fixtures/broken-reverse-charge-wording.md) | NON-COMPLIANT — defective particulars | Construction supply where the customer accounts for the VAT, but no "reverse charge" reference — "VAT not charged" is not the required wording. Defective, not invalid: the invoice shows no separate VAT amount (gross only), so nothing could be wrongly reclaimed [reg 14(1)(o)] |
| [broken-missing-unit-price.md](../fixtures/broken-missing-unit-price.md) | NON-COMPLIANT — defective particulars | Extent shown (18 hours) but no unit price [reg 14(1)(m)] |
| [broken-vat-total-in-euros.md](../fixtures/broken-vat-total-in-euros.md) | NON-COMPLIANT — invalid invoice | Net amounts in euros are permitted [reg 14(1)(h)], but the VAT total appears only in euros, not sterling [reg 14(1)(l)] |
| [broken-simplified-over-limit.md](../fixtures/broken-simplified-over-limit.md) | NON-COMPLIANT — invalid invoice | Simplified format used at £474.00 gross — over the £250 limit, full particulars required [reg 16A; 700/21 §4.5] — plus the knock-on full-checklist failures a simplified-format document necessarily has at that value (no customer particulars, no VAT amount, no net figures, no unit price) |
| [broken-exempt-on-simplified.md](../fixtures/broken-exempt-on-simplified.md) | NON-COMPLIANT — invalid invoice | Exempt postage stamps included on a retailer's simplified invoice [reg 16(2); 700/21 §4.4] |
| [broken-arithmetic-vat-total.md](../fixtures/broken-arithmetic-vat-total.md) | NON-COMPLIANT — invalid invoice | Line VAT sums to £230.00 but the invoice states £276.00 [reg 14(1)(h); reg 14(1)(l)] |

Each broken fixture plants one class of defect. For most, a correct audit reports that finding plus passes for everything else; the over-limit fixture is the exception — once the £250 relaxation falls away, the full checklist applies and the simplified-format document genuinely fails several of its particulars, all of which a correct audit reports (see [docs/cold-walk.md](../docs/cold-walk.md), which is how this note got corrected).
