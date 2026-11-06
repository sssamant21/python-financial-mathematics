# Section 11.12 — Numerical and rounding review

Baseline `1b07ead422f850396300dea90c9c9e600b7e4205`. [Runner](review.py) · [Baseline](initial-results.json) · [Corrected results](results.json) · [Worked answers](ANSWERS.md) · [Initial QA error](initial-qa-error.txt).

The runner executes both exact short Python fences, the standalone demo and its 12 existing methods, and compilation, on Linux CPython 3.12.14. A fifth command is a supplemental probe that imports the exact listing under Python optimization and mutates a row. The four exact-source commands passed both times. The optimized probe and nine of 22 supplemental predicates initially failed; all five command expectations and 22 predicates passed after correction. One workflow and 14 local records were reviewed; no historical unique methods were added.

A direct rational discount sum checks the ordinary and small-rate formulas. The naive formula's loss of precision is an intentional teaching comparison. The independent cent benchmark derives the installment by summing discount factors and walks an integer-cent recurrence. It confirms all 24 ordinary rows, a 443.21 regular payment, a 443.11 final payment and exact principal reconciliation. F70 and F54 recurred in cent ties, booked principal, Decimal precision and float range. The lab separates float formula comparison from the exact cent ledger. F75: assertions let corrupted rows pass with Python optimization. Explicit errors now enforce the reconciliation contract independently of optimization.

The first QA run reached Python's integer-to-string limit when serializing a large exact Fraction. The runner still derives the exact rational value and records its float projection; the corrected observer then captured the unchanged source baseline. Supply an optional manuscript path to replay; the runner overwrites its current results file.

The standard-library lab is standalone, with no external data or prior imports. This is an illustrative half-up policy, not a lender's servicing implementation. Other rate conventions, irregular dates, extra payments, contract terms and other runtimes were not exercised. F28, F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-11-rounding-review/review.py
```

Next: 11.13 — Chapter Project — Loan and Mortgage Analyzer.
