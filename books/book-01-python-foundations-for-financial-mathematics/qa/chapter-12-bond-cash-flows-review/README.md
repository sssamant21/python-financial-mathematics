# Section 12.2 — Bond cash-flow review

Baseline `717b4d03b05b2c0e25555594d7df5cc8a3e6a8cb`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Answers and project](ANSWERS.md).

The runner executes the sole Python fence byte for byte as the named script in isolation and compiles it. Both documented commands and all 12 existing methods passed on both versions in Linux CPython 3.12.14. Twelve of 38 supplemental predicates initially failed; all 38 passed after correction. One workflow, 18 local answer records and one separate applied project were reviewed. No historical unique test methods were added.

An independent rational cash-flow sequence checks all rows of the three project bonds, their redemption and aggregate values, and prices at 4%, 6% and 8% nominal annual yield using each schedule's frequency. The source demo covers only the first bond. It is not an execution of the full project by itself.

F78 recurred in acceptance of fractional counts. F54 recurred in overflowed coupon intermediates, underflowed discount factors and out-of-range outputs. F79: the original pricing function silently discounted semiannual rows with a quarterly frequency and accepted duplicate periods, wrong flow composition or missing redemption. It also propagated a nonfinite total. Timing, fixed coupon, redemption and composition checks now protect the equal-period bullet model. No stub period is implemented; the misleading source docstring was removed.

The listing is standalone Python 3.9+ with no prior script, third-party package or data dependency. It validates reported float rows, uses rational arithmetic for discounting and reports floats. Irregular or stub periods, actual settlement conventions, amortizing principal and credit events remain conceptual. F28, F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-12-bond-cash-flows-review/review.py
```

Next: 12.3 — Coupon Bonds.
