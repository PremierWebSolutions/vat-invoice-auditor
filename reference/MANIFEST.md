# Reference integrity manifest

SHA-256 of every file in reference/ (except this one and CATALOG.md), recorded
at the access dates stated in each file's own header. Verify with:

```bash
python3 tools/check_reference_integrity.py
```

A mismatch means the text changed without the manifest being regenerated on
purpose. Regenerating with `--write` after a deliberate re-fetch is correct;
regenerating to silence an unexplained mismatch defeats the entire point.

```
067372cdf28fb851b9734cc3b5203cef6d824b565ec1d081183b82b17e2fd037  vat-notice-700-21-invoicing.md
8118c8982f529eca1fb20e69cc85d7be15f95a7725022482ee90b9e2317faa8f  vat-regulations-1995-reg-13.md
64fb8ab95de8abcf650216e37b7c662e054b922847ddde79b2204c4966e66917  vat-regulations-1995-reg-14.md
2492bb60432cd1fc6d4b822ddeb4769ef4f91c09e08498c1d3913ff9afc35ecc  vat-regulations-1995-reg-16.md
0a7e3f9b24889b7d7d96c9d2943f991837f41b68d701f013bac765b6bbba8d29  vat-regulations-1995-reg-16A.md
```
