# Section 12.3 — Coupon Bonds review

Baseline: `860f6a9dc3fd52a1628374c03b8cf119a484dde3`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Answers and mini-project](ANSWERS.md).

The runner saves the sole Python fence verbatim, executes the documented demonstration and embedded suite, then compiles the extracted file. Both commands and all 12 existing methods passed on both versions in the recorded Linux CPython runtime. Nine of 41 supplemental predicates failed initially; all 41 passed after correction. This is one workflow, 18 local answer records and one separately scoped mini-project. No historical unique methods were added.

An independent backward valuation starts with redemption and discounts one period at a time, adding the coupon before each discount. It checks both source routes at all six project yields. The demo itself prints only 4%, 6% and 8%. The coupon timeline, annual coupon, current yield, zero yield, zero coupon, and quarterly example are checked separately.

F54 and F78 recur in intermediate overflow and underflow, nonrepresentable reports, false par and fractional or zero counts. Exact input-decimal arithmetic resolves these checks. F80: subtracting face from the rounded promised total could erase real coupon income; the source now computes the coupon stream's total directly. The annuity-factor worked answer now includes its zero-yield limit.

Use standalone Python 3.9+ with its standard library. No other listing or data file is needed. This is an equal-period, nonnegative-yield, promised-cash-flow model for teaching-sized terms. Settlement accrual, defaults, market risk and independent acceptance were not executed. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-12-coupon-bonds-review/review.py
```

Next: 12.4 — Zero-Coupon Bonds.
