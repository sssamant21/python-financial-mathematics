# Section 12.12 — Interest-Rate Sensitivity review

Baseline: `46cd1908926849aa6405bb3800e013a9c5ca12b2`. [Runner](review.py) · [Initial](initial-results.json) · [Corrected](results.json) · [Answers](ANSWERS.md) · [Initial QA error](initial-qa-error.txt).

Both documented commands and all 12 existing methods passed on the baseline and corrected exact extracted listing in the recorded Linux CPython runtime. Eleven of 41 supplemental predicates failed initially; all 41 passed after correction. Counts: one workflow, 18 local answers, one separate mini-project and no additions to historical unique methods. An initial QA run failed when a local list shadowed the manuscript path; the traceback is retained, and the observer was corrected before rerunning the unchanged source.

The independent benchmark uses backward rational prices and centered differences, then sums three independently derived position risks and changes. All six project shocks reconcile to their component P&Ls, and the second-order estimate improves each checked case. The demo covers Bond A only. The runner also calls the exact portfolio functions for all three bonds and a mixed-frequency case. At base, the portfolio is worth 4,167.89, modified duration is about 3.873825, convexity is 17.982728 and DV01 is 1.614567 currency units per bp.

F89: supplying the optional frequency shifted the original shock argument into the frequency slot. The corrected lab defines and unpacks the position shape explicitly, supplies portfolio base analytics and preserves tiny price changes. F54 recurred in unrepresentable individual results and overflow in an intermediate that should not prevent a finite shock output. Exact model operations precede float reporting.

The standalone lab requires Python 3.9+ and standard library only. Positions are positive face amounts in one common currency. Each bond's nominal yield is shocked by the same decimal amount under its own frequency; no nonparallel curve, spreads, short hedge, funding convention, other platform or independent acceptance was tested. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-12-interest-rate-sensitivity-review/review.py
```

Next: 12.13 — Yield Curves.
