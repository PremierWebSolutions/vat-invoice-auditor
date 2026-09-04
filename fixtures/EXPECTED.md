# Fixture answer sheet — for judges and testing only

Do **not** feed this file to the auditor alongside an invoice: it contains the answers. Every business, person, address, VAT number and bank detail in these fixtures is synthetic.

| Fixture | Designed outcome | Key finding(s) it must surface |
|---|---|---|
| [compliant-full-invoice.md](compliant-full-invoice.md) | COMPLIANT | All reg 14(1) particulars present; arithmetic exact [reg 14(1)] |
| [compliant-simplified-invoice.md](compliant-simplified-invoice.md) | COMPLIANT | £186.00 gross ≤ £250; all reg 16A(a)–(e) particulars present [reg 16A] |
| [broken-missing-sequential-number.md](broken-missing-sequential-number.md) | NON-COMPLIANT — defective particulars | No invoice number anywhere [reg 14(1)(a)] |
| [broken-missing-vat-number.md](broken-missing-vat-number.md) | NON-COMPLIANT — invalid invoice | Supplier VAT registration number absent [reg 14(1)(d)] |
| [broken-reverse-charge-wording.md](broken-reverse-charge-wording.md) | NON-COMPLIANT — invalid invoice | Construction supply where the customer accounts for the VAT, but no "reverse charge" reference — "VAT not charged" is not the required wording [reg 14(1)(o)] |
| [broken-missing-unit-price.md](broken-missing-unit-price.md) | NON-COMPLIANT — defective particulars | Extent shown (18 hours) but no unit price [reg 14(1)(m)] |
| [broken-vat-total-in-euros.md](broken-vat-total-in-euros.md) | NON-COMPLIANT — invalid invoice | Net amounts in euros are permitted [reg 14(1)(h)], but the VAT total appears only in euros, not sterling [reg 14(1)(l)] |
| [broken-simplified-over-limit.md](broken-simplified-over-limit.md) | NON-COMPLIANT — invalid invoice | Simplified format used at £474.00 gross — over the £250 limit, full particulars required [reg 16A; 700/21 §4.5] |
| [broken-exempt-on-simplified.md](broken-exempt-on-simplified.md) | NON-COMPLIANT — invalid invoice | Exempt postage stamps included on a retailer's simplified invoice [reg 16(2); 700/21 §4.4] |
| [broken-arithmetic-vat-total.md](broken-arithmetic-vat-total.md) | NON-COMPLIANT — invalid invoice | Line VAT sums to £230.00 but the invoice states £276.00 [reg 14(1)(h); reg 14(1)(l)] |

Each broken fixture plants exactly one class of defect, so a correct audit reports that finding plus passes for everything else.
