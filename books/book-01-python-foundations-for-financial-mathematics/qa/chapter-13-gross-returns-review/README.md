# Section 13.3 — Gross Returns review

Baseline: `135db4e1f6d5dfcc38b8972baa71777add885790`. [Runner](review.py) · [Initial](initial-results.json) · [Corrected](results.json) · [Answers](ANSWERS.md).

The runner executes the named standalone script from the sole verbatim Python fence, checks isolated import and compiles it. All three commands and 12 existing methods passed on both versions in the recorded Linux CPython runtime. Nine of 54 supplemental predicates initially failed; all 54 passed after correction. One workflow, 18 local answers, one separate project and no historical unique additions are recorded.

Independent rational products and Decimal powers check every daily factor, the linked return, final wealth, geometric mean, 252-day annualization and zero-factor path. The mini-project is separate from the four-return demo. Its final wealth is 26,501.60; annualized 1,791.18% is a constant-equivalent value from five days, not a forecast. The arithmetic average and beginning-weight portfolio example are supplemental calculations.

F97: a tiny geometric gain disappeared when its gross factor rounded to one; annualization could silently report a total loss despite positive gross. F95 and F54 recurred in linked returns and intermediate or result range. The corrected lab separates linked factor and linked return reporting and checks representability.

Python 3.9+ and the standard library suffice. No external prices, trading calendar, realized reinvestment, other platform or independent acceptance was tested. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-13-gross-returns-review/review.py
```

Next: 13.4 — Log Returns.
