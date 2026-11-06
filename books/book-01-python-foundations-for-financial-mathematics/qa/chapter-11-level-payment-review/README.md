# Section 11.3 — Level-payment loans review

Baseline `c36f690297bd3d134cd94b5bf35737a94cda7a09`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Twelve answers](ANSWERS.md).

Both documented commands and all twelve existing methods passed on both versions. Ten of 33 additional predicates failed initially; all 33 pass after correction. The runner saves the sole Python listing verbatim as level_payment_loans.py, runs the example and tests, then compiles it in isolation using prepared Linux CPython 3.12.14 and the standard library. The file needs no earlier module, external package, data or network. Regressions are inside an existing method; no historical unique methods were added.

F54 recurred in payment, interest and schedule range checks. Nonzero components rounded to zero and nonfinite results are rejected. F56 recurred when opening balance or finite total interest depended on an overflowing payment. F66 recurred when the principal split and total interest were computed by subtracting nearly equal floats. The schedule uses prospective balances and equivalent direct principal reductions; final principal is the prospective opening balance of the last period, not a write-off of a separately calculated residual. Total interest uses a local 750-digit Decimal computation before float conversion. Baseline failures are reproducible by using this runner on unchanged baseline source.

An independent exact Fraction recurrence checks all 24 rows, the first split, intermediate balances, the sum of principal and total interest; ordinary loan payment is derived from a direct unit discount sum. The two displayed numbers are compared after rounding only at output. The revised answers include the zero-rate branch and explicitly name the opening balance for the first-period question. Contractual rounding, fees, prepayments, huge schedule resource limits, alternate platforms and notebooks were not tested. Bounded factors can reject otherwise representable values. F28, F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-11-level-payment-review/review.py
```

Next: Section 11.4.
