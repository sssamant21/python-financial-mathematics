# Section 13.8 — Arithmetic vs. Geometric Mean Return review

Baseline: `b01aec141de6edefee609d5ab58efcc5b8c066e2`. [Runner](review.py) · [Initial](initial-results.json) · [Corrected](results.json) · [Answers](ANSWERS.md).

The observer executes the exact standalone listing, verifies isolated import and compiles it. All three commands and all 12 existing methods passed on both versions in the recorded Linux CPython runtime. Eight of 37 supplemental predicates initially failed; all 37 passed after correction. Counts: one workflow, 18 local answers, one separate mini-project, no historical unique additions. One exact contextual expression is additionally evaluated with its required `math` and `returns` bindings; it is not a separate workflow.

The independent benchmark uses a rational product, a separate high-precision power, and the pairwise-difference identity for population variance. It checks the six-month report, the reconstructed terminal wealth, the approximation error, annualization and total-loss stress. The demo itself uses two returns. The six-month fixture gives 21,242.11 wealth and 12.806807% annual equivalent under the stated assumption.

F102: rounding a positive gross result to −100% could also erase a finite terminal wealth amount; the project lacked final numerical reconciliation. F54 recurred in scaled wealth, mean and variance. Source helpers calculate each requested output before checking float reporting.

Standalone Python 3.9+ and standard library only. These are descriptive sample calculations; the variance-drag approximation is not an expectation model. No fund feed, independent reviewer or additional platform was used. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-13-mean-returns-review/review.py
```

Next: 13.9 — Time-Weighted Return.
