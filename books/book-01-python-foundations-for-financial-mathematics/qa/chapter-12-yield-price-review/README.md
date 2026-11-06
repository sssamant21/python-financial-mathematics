# Section 12.7 — Yield and Price Relationships review

Baseline: `d91c378d5ce5fcfe0ff37705622fc3502089fd7d`. [Runner](review.py) · [Baseline](initial-results.json) · [Corrected results](results.json) · [Answers](ANSWERS.md).

Both documented commands and all 12 existing methods passed on the original and corrected exact extracted listing in the recorded Linux CPython runtime. Six of 36 additional predicates failed at baseline; all 36 passed after correction. Counts: one workflow, 18 local answers, one separately reviewed mini-project, and no new historical unique methods.

The independent price benchmark starts at redemption and steps backward one coupon date at a time. High-precision symmetric differences benchmark the analytical sensitivities. Seven price scenarios and six two-sided shocks were run through the source functions; the runner supplies the supplemental duration-only and duration-plus-convexity calculations. Adding convexity improves the approximation in each checked shock. The exact demo prints only five scenarios.

F84: float rounding erased slopes and curvature at tiny steps, and boolean steps passed validation. The corrected source applies finite differences before float reporting and validates both the step and bumped yields. F54 recurred in derivative intermediate range and unsupported output values.

Python 3.9+ and its standard library are sufficient. No prior files, day-count convention, optional cash flows, market observations, other platforms or independent acceptance were used. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-12-yield-price-review/review.py
```

Next: 12.8 — Accrued Interest and Clean vs. Dirty Price.
