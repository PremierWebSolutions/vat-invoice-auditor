#!/usr/bin/env python3
"""Recompute the arithmetic in every fixture invoice from its own stated
numbers — the script does the sums, nobody has to trust that a worked
example's "recomputes exactly" claim is actually true.

Runs offline, stdlib only, no API key, no dependency on check_citations.py.

Three invoice shapes appear in fixtures/, each with its own reconciliation:

1. Line-item table (Qty/Extent | Description | Unit price | Net | VAT rate |
   VAT): each line's qty x unit price ~ net and net x rate ~ VAT; the lines'
   nets and VATs sum to the stated "Total net" / "Total VAT"; net + VAT ~ the
   bold "Total payable".
2. Grouped item/amount table with a standard-rated/exempt split in prose
   (broken-exempt-on-simplified.md): the standard-rated group's own line
   items sum to its stated gross-including-VAT figure, and that figure plus
   the stated exempt amount sums to the bold total payable.
3. Single-figure simplified receipt (no table): the "Amount includes VAT..."
   sentence's gross must equal the bold "Total payable" gross.

A fixture matching none of these shapes is a HARD FAILURE, not a skip — an
unrecognised invoice silently excluded from arithmetic checking is exactly
the "not run" that must never read as a pass.

Every fixture is expected to reconcile except the ones in EXPECTED_BROKEN,
which exist to be arithmetically wrong on purpose. A fixture reconciling
when it shouldn't, or failing when it shouldn't, is reported as a defect in
the fixture data itself.

Usage:
    python3 tools/check_arithmetic.py             # check fixtures/
    python3 tools/check_arithmetic.py --self-test  # prove the checker fires
"""
import re
import sys
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

REPO = Path(__file__).resolve().parent.parent
FIXTURES = REPO / "fixtures"
TOLERANCE = Decimal("0.01")

# Fixtures whose arithmetic is deliberately inconsistent — the one class of
# "expected failure" this checker must still report as a named, understood
# mismatch rather than an unexplained red line.
EXPECTED_BROKEN = {"broken-arithmetic-vat-total.md"}

MONEY = r"[£€]\s?[\d,]+\.\d{2}"


def money(text):
    """Parse a single £/€ figure to Decimal, or None if not exactly one."""
    m = re.findall(MONEY, text)
    if len(m) != 1:
        return None
    return Decimal(re.sub(r"[£€,\s]", "", m[0]))


def qty_multiplier(qty_cell, unit_price_cell):
    """Extract a numeric quantity from cells like '6', '2 days', '18 hours'
    paired with a unit price like '£85.00' or '£320.00 per day'."""
    qm = re.match(r"\s*([\d.]+)", qty_cell)
    pm = re.search(MONEY, unit_price_cell)
    if not qm or not pm:
        return None
    return Decimal(qm.group(1)) * Decimal(re.sub(r"[£€,\s]", "", pm.group(0)))


def close(a, b, tol=TOLERANCE):
    return a is not None and b is not None and abs(a - b) <= tol


def parse_line_item_table(text):
    """Shape 1: pipe table with Net / VAT rate / VAT columns (Unit price
    optional — a fixture testing for a missing unit price legitimately has
    no such column, and still gets its rate/sum arithmetic checked)."""
    rows = [r for r in text.splitlines() if r.strip().startswith("|")]
    if len(rows) < 3:
        return None
    header = [c.strip().lower() for c in rows[0].strip("|").split("|")]
    if not ({"net", "vat", "vat rate"} <= set(header)):
        return None
    idx = {name: i for i, name in enumerate(header)}
    errors, net_sum, vat_sum = [], Decimal("0"), Decimal("0")
    for row in rows[2:]:
        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) != len(header):
            continue
        net = money(cells[idx["net"]])
        rate_cell = cells[idx["vat rate"]]
        vat = money(cells[idx["vat"]])
        if net is None or vat is None:
            continue
        if "unit price" in idx:
            qty_col = cells[idx.get("qty", idx.get("extent", 0))]
            unit_price = cells[idx["unit price"]]
            expected_net = qty_multiplier(qty_col, unit_price)
            if expected_net is not None and not close(expected_net, net):
                errors.append(f"line {cells[idx.get('description', 1)]!r}: "
                               f"qty x unit price = {expected_net}, but Net states {net}")
        rate_m = re.search(r"(\d+(?:\.\d+)?)\s*%", rate_cell)
        if rate_m:
            rate = Decimal(rate_m.group(1)) / 100
            expected_vat = (net * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if not close(expected_vat, vat):
                errors.append(f"line {cells[idx.get('description', 1)]!r}: "
                               f"{rate_cell} of net {net} = {expected_vat}, but VAT states {vat}")
        net_sum += net
        vat_sum += vat
    total_net = money(next((l for l in text.splitlines() if l.strip().lower().startswith("total net")), ""))
    total_vat = money(next((l for l in text.splitlines() if l.strip().lower().startswith("total vat")), ""))
    total_payable = money(next((l for l in text.splitlines() if "total payable" in l.lower()), ""))
    if total_net is not None and not close(net_sum, total_net):
        errors.append(f"line nets sum to {net_sum}, but stated Total net is {total_net}")
    if total_vat is not None and not close(vat_sum, total_vat):
        errors.append(f"line VATs sum to {vat_sum}, but stated Total VAT is {total_vat}")
    if total_net is not None and total_vat is not None and total_payable is not None:
        if not close(total_net + total_vat, total_payable):
            errors.append(f"Total net {total_net} + Total VAT {total_vat} = "
                           f"{total_net + total_vat}, but stated Total payable is {total_payable}")
    return errors


def parse_grouped_split(text):
    """Shape 2: item/amount table plus a standard-rated/exempt prose split."""
    rows = [r for r in text.splitlines() if r.strip().startswith("|")]
    header = [c.strip().lower() for c in rows[0].strip("|").split("|")] if rows else []
    if header != ["item", "amount"]:
        return None
    line_amounts = []
    exempt_line_amounts = []
    for row in rows[2:]:
        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) != 2:
            continue
        amt = money(cells[1])
        if amt is None:
            continue
        (exempt_line_amounts if "exempt" in cells[0].lower() else line_amounts).append(amt)
    std_group = money(next((l for l in text.splitlines()
                             if "standard-rated" in l.lower() and "including vat" in l.lower()), ""))
    exempt_group = money(next((l for l in text.splitlines() if "exempt from vat" in l.lower()), ""))
    total_payable = money(next((l for l in text.splitlines() if "total payable" in l.lower()), ""))
    errors = []
    std_sum = sum(line_amounts, Decimal("0"))
    if std_group is not None and not close(std_sum, std_group):
        errors.append(f"standard-rated line items sum to {std_sum}, but the stated group total is {std_group}")
    exempt_sum = sum(exempt_line_amounts, Decimal("0"))
    if exempt_group is not None and not close(exempt_sum, exempt_group):
        errors.append(f"exempt line items sum to {exempt_sum}, but the stated exempt total is {exempt_group}")
    if std_group is not None and exempt_group is not None and total_payable is not None:
        if not close(std_group + exempt_group, total_payable):
            errors.append(f"standard-rated {std_group} + exempt {exempt_group} = "
                           f"{std_group + exempt_group}, but stated Total payable is {total_payable}")
    return errors


def parse_single_figure_receipt(text):
    """Shape 3: no table, one gross figure stated twice."""
    if re.search(r"\|.*\|", text):
        return None
    incl_line = next((l for l in text.splitlines() if "amount includes vat" in l.lower()), None)
    total_line = next((l for l in text.splitlines() if "total payable" in l.lower()), None)
    if incl_line is None or total_line is None:
        return None
    amounts_incl = re.findall(MONEY, incl_line)
    gross_total = money(total_line)
    errors = []
    if not amounts_incl or gross_total is None:
        errors.append("expected a gross figure in both the 'Amount includes VAT' line and the Total payable line")
    elif not close(Decimal(re.sub(r"[£€,\s]", "", amounts_incl[-1])), gross_total):
        errors.append(f"'Amount includes VAT' line states {amounts_incl[-1]}, "
                       f"but Total payable states {gross_total}")
    return errors


SHAPES = [parse_line_item_table, parse_grouped_split, parse_single_figure_receipt]


def check_fixture(path):
    text = path.read_text(encoding="utf-8")
    for shape in SHAPES:
        errors = shape(text)
        if errors is not None:
            return errors
    return None  # no shape matched — hard failure, not a skip


def run(fixture_dir):
    results = {}
    for path in sorted(fixture_dir.glob("*.md")):
        errors = check_fixture(path)
        results[path.name] = errors
    return results


def report(results, expected_broken):
    problems = []
    for name, errors in results.items():
        if errors is None:
            problems.append((name, ["UNRECOGNISED INVOICE SHAPE — no arithmetic parser matched this "
                                     "file; add one rather than letting it pass unchecked"]))
        elif name in expected_broken:
            if not errors:
                problems.append((name, ["expected to be arithmetically broken (in EXPECTED_BROKEN) "
                                         "but reconciled cleanly — the fixture no longer tests what it claims to"]))
        elif errors:
            problems.append((name, errors))
    return problems


def self_test():
    testdata = REPO / "tools" / "testdata"
    clean = testdata / "clean-arithmetic.md"
    broken = testdata / "broken-arithmetic.md"
    failures = []

    clean_errors = check_fixture(clean)
    if clean_errors is None:
        failures.append("clean testdata matched no shape parser")
    elif clean_errors:
        failures.append(f"clean testdata raised errors it shouldn't have: {clean_errors}")

    broken_errors = check_fixture(broken)
    if broken_errors is None:
        failures.append("broken testdata matched no shape parser")
    elif not broken_errors:
        failures.append("broken testdata (planted defect) reconciled cleanly — checker did not fire")

    if failures:
        print("SELF-TEST FAILED — the arithmetic checker can no longer be trusted:")
        for f in failures:
            print(f"  ✗ {f}")
        return 1
    print(f"SELF-TEST PASSED — clean testdata reconciles with 0 errors; "
          f"broken testdata's planted defect caught: {broken_errors[0]}")
    return 0


def main(argv):
    if argv and argv[0] == "--self-test":
        return self_test()
    results = run(FIXTURES)
    problems = report(results, EXPECTED_BROKEN)
    checked = len(results)
    if problems:
        print(f"ARITHMETIC CHECK FAILED — {len(problems)} of {checked} fixture(s) have a problem:")
        for name, errors in problems:
            for e in errors:
                print(f"  ✗ {name}: {e}")
        return 1
    print(f"ARITHMETIC CHECK PASSED — {checked} fixtures recomputed from their own stated figures; "
          f"{len(EXPECTED_BROKEN)} confirmed broken exactly as designed, the rest reconcile.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
