# Section 13.6 — Annualization review

Baseline: `d437ea6689d86ed8967e3a08981b3f2f4b2f3c82`. [Runner](review.py) · [Initial](initial-results.json) · [Corrected](results.json) · [Answers](ANSWERS.md) · [Supplemental project CSV](project.csv).

The observer executes the exact Python fence, checks isolated import and compiles the standalone file. All three commands and 12 existing methods passed on both versions in the recorded Linux CPython runtime. Seven of 42 additional predicates failed on the baseline; all 42 passed after correction. Counts: one workflow, 18 local answers, one separately scoped mini-project and no historical unique additions.

Independent rational powers and Decimal calculations check gains, losses, conversions, actual elapsed periods and all four strategy round trips. The 90-day Actual/365 Fixed rate is 8.3623648654%, not 8.365%. The observer generates the supplemental CSV by calling the source, computing annual logs, and recording residuals; the source demo is a separate three-example workflow.

F100: an early total-loss return hid later invalid data, timestamp inputs lost partial days, and the published 90-day approximation was wrong. F54 recurred in overflow, near-zero rate conversion and positive factors rounding to total loss. The corrected listing validates the entire series and uses exact calendar-day fractions before reporting.

Standalone Python 3.9+ with standard library only. Annual-effective rates are constant-equivalent, not forecasts or regulatory APR. No market data, production calendar, other platform or independent acceptance was validated. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-13-annualization-review/review.py
```

Next: 13.7.
