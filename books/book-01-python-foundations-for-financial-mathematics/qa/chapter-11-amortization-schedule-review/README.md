# Section 11.7 — Amortization schedules review

Baseline `151afae0364cbdd3b468d2f8da66a0a948ba7319`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Fourteen worked answers](ANSWERS.md).

The runner extracts the single Python fence byte for byte, saves it as `amortization_schedules.py` in a temporary directory, and runs the two documented commands. The demo and all 12 existing test methods passed on each version; so did compilation. Eleven of 31 additional predicates failed against the baseline; all 31 passed after correction on Linux CPython 3.12.14. The commands, source and listing hashes, demo output and individual outcomes are retained. This is one workflow and 14 local answer records. No historical unique methods were added.

The exact-model benchmark sums rational discount factors and walks the balance recurrence for all 24 periods. It checks the published table and the component, balance and total identities. The source instead uses prospective balances and discounted principal components to avoid cancellation. F54 recurred for payment and interest outside the supported float range; F66 recurred when principal disappeared or the final row carried a residual. F68 recurred in four cells across rows 2 and 3 of the unrounded worked table.

The independent cent benchmark uses a direct discount sum and integer-cent recurrence, with exact half-up tie decisions. It matches all 24 rows and the demonstration, including the regular 443.21 payment and final 443.11 payment. The cent-rounded rows need not match the independently displayed cents of the unrounded model. F70 covered the 0.15 / 6 half-cent tie, a regular installment calculated before booking the opening to cents, zero booked principal, and a finite large balance failing at default Decimal precision. The corrected source computes exact rounding decisions from the booked opening and decimal input text, keeps the ledger in integer cents, and emits Decimal amounts.

Python 3 and its standard library are the only prerequisites. There is no input file, install step or CSV export. Scope is fixed-rate, equal-period educational schedules, with no real contract, fees, day-count accrual or prepayment workflow tested. Exact rational powers can be costly for large terms; no performance limit or universal numeric range is established. The runner's oracles are supplemental checks against the exact listing, not separately published lab implementations. F28, F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-11-amortization-schedule-review/review.py
```

Next: 11.8 — Mortgages.
