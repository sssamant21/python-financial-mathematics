# Section 12.8 — Accrued Interest and Clean vs. Dirty Price review

Baseline: `3720d1f59bd0a085595e57ec23ab97d8ba1a568a`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Answers](ANSWERS.md).

Both documented commands and the 12 existing methods passed on both versions of the exact extracted listing in the recorded Linux CPython runtime. Six of 39 additional predicates failed on the baseline; all 39 passed after correction. Counts: one workflow, 18 local answer records, one separate mini-project and no additions to historical unique methods.

The independent benchmark counts days by explicit Gregorian month lengths, then applies a rational fraction. It checks five settlements from period start to the day before the next coupon, a leap-year example, the next-period reset, and the reverse clean-price reconciliation. The demo prints only the April settlement; the runner calls the source for the full set. The per-100 quote conversion is supplemental arithmetic; the source dirty-price function consumes the converted full amount.

F85: datetime values passed the date check and silently lost hours when the lab took integer days. The API now accepts calendar dates only. F54 recurred in coupon/dirty overflow, coupon underflow and loss of an otherwise finite accrued amount. Rational model arithmetic defers reporting until the requested result is calculated.

Python 3.9+ and the standard library suffice; no earlier file or settlement calendar is required. This is a regular coupon-period day fraction. It does not certify Actual/Actual variants, alternative day-count or ex-coupon rules, settlement-date yield, platform portability or independent acceptance. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-12-accrued-interest-review/review.py
```

Next: 12.9 — Duration.
