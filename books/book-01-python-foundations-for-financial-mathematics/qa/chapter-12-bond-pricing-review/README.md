# Section 12.5 — Bond Pricing review

Baseline: `3f234f122e06f4e1a7eb05d8fa5d8b49c87b85cb`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Answer and project mapping](ANSWERS.md).

Both documented commands and all 12 existing methods passed on the original and corrected extracted listing on the recorded Linux CPython runtime. Twelve of 40 supplemental predicates failed initially; all 40 passed after correction. Counts: one workflow, 18 local answers, one separate mini-project, no additions to historical unique methods.

The independent backward recurrence checks direct, annuity and bumped prices for all six project yields. A direct dot product checks the new nonflat fixture (1,057.90) and a flat curve reproduces par. The original demo prints three yields and one shock; the runner calls the exact listing for the remainder.

F82: flat pricing accepted inconsistent dates and frequency, curve pricing accepted malformed rows, annuity pricing and the shock accepted booleans, tiny shocks cancelled, and the project never supplied its factor array. The corrected source validates the rows, prices and compares exact model amounts before float reporting, and includes a six-factor example. F54 recurred in numeric range checks.

The lab is standalone Python 3.9+ and standard library only. Pricing is for the specified nonnegative promised cash flows and valid periodic yield above −100%; curve factors are positional and must be ordered by the caller to match the dates. No curve calibration, accrued-interest settlement, credit event or other platform was tested. F28, F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-12-bond-pricing-review/review.py
```

Next: 12.6 — Yield to Maturity.
