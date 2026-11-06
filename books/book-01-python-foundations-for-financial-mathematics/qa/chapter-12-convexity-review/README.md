# Section 12.11 — Convexity review

Baseline: `b2a8019baf291e06ff95a8a57e22a4ace70b1686`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Answers](ANSWERS.md).

Both documented commands and all 12 existing methods passed on both versions of the exact extracted listing in the recorded Linux CPython runtime. Five of 49 additional predicates failed on the baseline; all 49 passed after correction. Counts: one workflow, 18 local answers, one separate mini-project and no historical unique additions.

The independent benchmark values the bond backward and derives curvature from a centered rational price difference. It checks the zero-coupon formula, every project shock and both absolute approximation errors. Adding convexity improved all eight approximations, and each equal-sized yield decline produced a larger gain than the corresponding increase produced a loss. The exact demo covers only five shocks; the runner calls the listing for all eight.

F88: a nonzero small shock could produce zero exact relative repricing because bumped yields and prices were rounded before subtraction. F54 recurred in extreme derivative and price ranges; the original relative scenario could return a finite exact change beside infinite approximations. Calculating the requested outputs before float reporting preserves representable relative values and rejects unrepresentable results.

The script is standalone Python 3.9+ with standard library only. The runner accepts a manuscript path for baseline replay and overwrites the current result file. Callable and mortgage prepayment behavior, nonparallel curves, other platforms and independent acceptance were not executed. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-12-convexity-review/review.py
```

Next: 12.12 — Interest-Rate Sensitivity.
