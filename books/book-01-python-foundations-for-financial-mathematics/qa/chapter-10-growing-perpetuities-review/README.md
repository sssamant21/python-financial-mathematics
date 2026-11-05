# Section 10.9 — Growing perpetuities review

Baseline `5813a24f9a5356dd2ed8cb8f38e26fbebf680a95`. [Runnable review](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Twelve prompt records](ANSWERS.md).

Both documented commands and all twelve existing methods passed on both versions. Eleven of 35 additional predicates initially failed; all 35 pass after correction. The runner extracts the only Python fence verbatim as growing_perpetuities.py, executes it and compiles it in isolation on prepared Linux CPython 3.12.14. Filename, save/run/compile steps and standalone standard-library imports were checked. There is no separate demonstration command, data, dependency installation or network requirement.

F11 recurred when subtracting logarithms for adjacent represented rates. The finite helper now uses the stable relative change before log1p. F54 recurred in five cases: tiny-rate finite valuation, ordinary underflow, due total overflow and deferral factor/result underflow. Factor ordering and explicit finite/nonzero result checks address these cases. F56 recurred in four cases: a finite first payment and an empty stream both required representable infinite PV, a due valuation formed an overflowing next payment, and deferred PV formed an overflowing ordinary value. Validation is now separate from valuation; due and deferred paths combine unit factors when representable. The finite helper retains the convergent-rate input contract. F57 rejected a boolean due payment before arithmetic could convert it into a numeric next payment. F58 clarified the sensitivity answer for signed and zero payments; its original unqualified wording is recorded in ANSWERS.md.

Independent Fraction sums benchmark finite values at 1, 20, 100 and 1000 payments. A first-term/ratio derivation benchmarks the infinite, due and deferred amounts and bounds the omitted tail at 1000. Next-payment and inverse-payment arithmetic are supplemental: the lab has no corresponding conversion APIs. Timing, convergence and sensitivity explanations are conceptual, with selected numerical examples and invalid-rate calls executed against the source. Regressions are inside an existing method; no historical unique methods were added. Reproduce initial failures using the same runner against the baseline source.

The bounded float implementation may reject factors even where another evaluation order could support the final value. No market suitability, contract rounding, calendar, notebook or fresh installation was tested. F28, F32, platform coverage and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-10-growing-perpetuities-review/review.py
```

Next: Section 10.10.
