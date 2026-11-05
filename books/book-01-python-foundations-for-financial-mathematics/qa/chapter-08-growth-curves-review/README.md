# Section 8.10 — Interest and investment growth curves review

Baseline `5bfa039fe841658f7cab45939e899670ffa15dcf`. [Runner](review.py) · [Initial failure](initial-results.json) · [Corrected results](results.json) · [Worked answers](ANSWERS.md).

One formal workflow and eight local answers reviewed. Three documented commands, eleven additional predicates and eight existing methods passed after correction. Both complete source listings were saved verbatim as siblings and discovery, demonstration and compilation ran from the lab directory. The grids and conventions are embedded; no earlier lab, external investment data, pandas or desktop is required. Prepared Linux CPython 3.12.14, NumPy 2.3.5 and Matplotlib 3.10.8 were used. Fresh installations and other platforms were not run.

**F42:** The helper declared Real scalar inputs but NumPy finiteness checks raised TypeError for Fraction principal/rate. Original failure retained; scalar bounds now precede and follow float conversion. The existing endpoint method gains regression assertions; no new historical methods. To replay the initial failure, run this runner from the same relative directory in a worktree at the baseline.

Independent 60-digit Decimal calculations verify all four terminal balances and the equivalent monthly nominal rate. Rational annual balances verify every common year-end. Domain and credit-period rejections use the exact source. PNG was inspected for scale labels, post-step annual states, distinct conventions and the absence of any uncertainty claim. The runner regenerates it and records its hash. Log and linear artists retain identical money arrays. The plot is not a forecast or validated real product; uncertainty remains conceptual. F28/F32, platform coverage and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-08-growth-curves-review/review.py
```

Next: Section 8.11 formal lab and local answers.
