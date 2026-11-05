# Section 9.7 — Discount factor lab and answer review

Baseline `4d803a09669ae4734a8970aabad623b346ea418f`. [Runner](review.py) · [Initial failure](initial-results.json) · [Corrected results](results.json) · [Five answers](ANSWERS.md).

One workflow and five local answers reviewed. Two documented commands, twenty additional checks and eight existing embedded methods passed after the F46 follow-up. The complete listing was saved verbatim as discount_factors.py and executed/compiled in isolation. Prepared Linux CPython 3.12.14; standard library only. No earlier local lab, external market data or network. Windows substitution and fresh installation were not executed.

F46 was reproduced with a nonzero Fraction payment below float range. The scalar validator formerly replaced the original value with zero before the monetary loss check. It now retains the original input during conversion and rejects that loss. The assertion is inside the existing payment-scaling method; no new historical method. Initial failure and corrected rerun are retained. Place the runner at this evidence path in a worktree of the baseline to replay the initial case.

Independent fractions verify all factor-grid rows, signed payment equivalents, reciprocal/interval composition and the numerical practice answers. Practice 5 supplies a factor directly, so its signed multiplication is supplemental arithmetic. Probability interpretation and rate/calendar metadata remain conceptual. Source range tests ran, without a claim of arbitrary-range accuracy, exact settlement or a calibrated yield curve. No chart is generated. F28/F32, platform/notebook and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-09-discount-factors-review/review.py
```

Next: Section 9.8 formal lab and local answers.
