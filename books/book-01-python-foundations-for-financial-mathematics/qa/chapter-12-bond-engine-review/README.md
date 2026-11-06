# Section 12.16 — Bond Analytics Engine review

Baseline: `c48141fa3800334d78190b8438ba0e65edddd803`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Answers and deliverables](ANSWERS.md).

Both documented commands, an isolated import probe and all 12 existing methods passed on both versions of the exact extracted listing in the recorded Linux CPython runtime. Six of 58 supplemental predicates failed initially; all 58 passed after correction. Counts: one workflow, 18 local answers, six separate project deliverable records and no historical unique methods added.

Independent backward rational prices and centered differences verify the base analytics for all three positions, three yield inversions from independent prices, 18 position-level stress rows, six aggregate shocks and all demo outputs. A separate Decimal direct-power calculation checks a nonflat spot schedule; the flat 6.09% spot curve reproduces 6% semiannual nominal par. The aggregate quadratic approximation improves each tested shock.

F93: the absolute residual could accept a wrong yield at small notionals, invalid tolerances went unchecked, and tiny repricing changes cancelled after float rounding. The corrected project resolves the supplied bracket and checks the relative residual at the reported yield, and performs scenario subtraction before reporting. F54 recurred in spot underflow and unsupported analytics ranges.

Use standalone Python 3.9+ with its standard library; no earlier listing or external curve file is required. Spot maps need one explicit key at every source payment time. Cash flows are fixed and equally spaced. No accrued interest, embedded options, quote calibration, other platform or independent acceptance was executed. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-12-bond-engine-review/review.py
```

Next: 12.17 — Exercises and Applied Problems.
