# Section 12.10 — Modified Duration review

Baseline: `58ec4f37c0ef1f63dc622f1c4665ddff5aa8564f`. [Runner](review.py) · [Initial](initial-results.json) · [Corrected](results.json) · [Answers](ANSWERS.md).

Both documented commands and all 12 existing test methods passed on the original and corrected exact extracted listing in the recorded Linux CPython runtime. Six of 36 additional predicates initially failed; all 36 passed after correction. Counts: one workflow, 18 local answers, one separate mini-project, and no new historical unique methods.

The independent backward valuation and centered rational difference check price, analytical slope, duration and DV01. All six project shocks and the 250,000 holding are checked using exact-source calls; the demo omits −25 bp. At par the source reports modified duration 2.708596 and DV01 about 0.270860 per 1,000 face, or 67.7149 per 250,000 face. The signed approximation errors are compared independently.

F87: zero frequency caused division before validation, and a sufficiently small shock cancelled in the rounded price subtraction. The code now validates before division and compares model values before reporting. F54 recurred in intermediate range loss and unsupported results.

The script is standalone Python 3.9+ with its standard library. This equal-period, fixed-cash-flow model does not establish callable or nonparallel risk analytics, portability or independent acceptance. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-12-modified-duration-review/review.py
```

Next: 12.11 — Convexity.
