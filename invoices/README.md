# Put the invoices you want to audit here

Drop the invoices you want checked into this folder — one per file. **PDFs are fine** (most supplier invoices are), and so are plain text files (`.md` or `.txt`). Then audit the whole folder at once from the repo root:

```bash
./tools/audit.sh invoices/*.pdf
```

or, in a chat: **Audit every invoice in invoices/**

To check a single one: **Audit invoices/that-invoice.pdf**

Four sample invoices (`SAMPLE-1` to `SAMPLE-4`) already sit here as PDFs so you can try the tool straight away. They're made up, but modelled on the kind of software and subscription invoices a practice actually receives, and they show the range of outcomes: `SAMPLE-1` is a clean full invoice (COMPLIANT), `SAMPLE-2` is a US supplier with no VAT number (fails), `SAMPLE-3` is a statement of account rather than a VAT invoice (the tool explains it can't stand as your invoice and tells you to request the real one), and `SAMPLE-4` is a small subscription receipt under £250 (a valid simplified invoice). Delete them once you've added your own, or they'll be audited alongside them.

## Two things worth knowing

**Your invoices stay private.** Everything you put in this folder is git-ignored — only this README and the `SAMPLE-` invoice are tracked — so a real supplier's invoice can never be committed or pushed to the public repo by accident. It stays on your machine.

**One limit on PDFs.** The auditor reads the text inside a PDF, which works for any PDF produced by software (accounting systems, invoicing tools, "print to PDF"). A PDF that is just a *photo or scan* of a paper invoice has no text to read — for those, type the details into a `.txt` file first, or run the scan through OCR.

**This is not the `fixtures/` folder.** `fixtures/` holds the tool's own synthetic test invoices; leave those alone. Your real invoices go here, in `invoices/`.
