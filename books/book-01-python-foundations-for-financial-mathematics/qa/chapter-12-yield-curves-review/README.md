# Section 12.13 — Yield Curves review

Baseline: `e6c9d0926447e5521b62b02c04423bf521146a6e`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Answers](ANSWERS.md).

The runner extracts the sole Python fence verbatim, runs the named demo and embedded suite, and compiles the file in isolation. Both commands and all 12 existing methods passed on the baseline and corrected listing in the recorded Linux CPython runtime. Nine of 37 supplemental predicates failed initially; all 37 passed after correction. Counts: one workflow, 18 local answers, one separate mini-project and no additions to historical unique methods.

Independent high-precision powers check all six spots, factors and prices. Exact rational growth ratios benchmark the two forwards. The stress-node construction is supplemental: add 50 bp at every node, or interpolate each endpoint shock linearly across tenors for steepening and flattening. The runner passes those stressed nodes to the exact source and checks all 18 shocked prices.

F90: the 2-year factor and price displayed incorrectly rounded values, invalid annual-effective nodes could enter the curve, and tiny forwards cancelled when derived from rounded factors. F54 recurred in intermediate interpolation range, discount underflow, finite scaled PV and finite forward despite unreportable standalone factors. Exact interpolation and log discount arithmetic precede float reporting.

The standalone script requires Python 3.9+ and standard library only. No extrapolation, curve calibration, arbitrage test, market day-count convention, data download, other platform or independent acceptance was executed. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-12-yield-curves-review/review.py
```

Next: 12.14 — Discount Factors and Spot Rates.
