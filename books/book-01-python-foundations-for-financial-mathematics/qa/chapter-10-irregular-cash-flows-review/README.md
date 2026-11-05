# Section 10.11 — Irregular cash flows review

Baseline `8a7200f1d552f3f36281b88dd2a2a974bd278bc1`. [Runnable review](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Twelve prompt records](ANSWERS.md).

Both documented commands and all twelve existing methods passed on both source versions. Five of 27 additional predicates initially failed; all 27 pass on the corrected source. The runner extracts the sole Python fence verbatim as irregular_cash_flows.py, runs the tests, and compiles it in isolation. Prepared Linux CPython 3.12.14 and its standard library were used. Save/run/compile and exact filename hold. The worked example was evaluated by calling the extracted source, not as an additional documented demonstration command. No data files, dependency installation or network are required.

F53 recurred in two empty-stream calls: string and datetime anchors bypassed validation. Any supplied anchor is now checked before returning empty value, with valid empty streams still supported. F54 recurred in discount-factor and nonzero-term underflow, now explicitly rejected. F56 recurred when an exact zero payment with a distant anchor tried to evaluate an overflowing factor. Zero terms skip factor calculation after input validation. All five regressions are inside an existing method; no historical unique methods were added. Reproduce initial failures by using the same runner against baseline source.

Calendar arithmetic gives day offsets 0, 104, 333 and 424. Independent Decimal sums at precision 100 produce 59.738677540615295… at the worked anchor. Source default and explicit anchors, unsorted generators, repeated dates, signed flows and leap-year Actual/365 Fixed values agree with Decimal or rational benchmarks. The P9 answer now describes mathematical invariance without implying every floating-point difference is insignificant. Tested reorderings agree; arbitrary extreme cancellation/order combinations are outside scope.

Conceptual audit covers rate, currency and completeness, which are not all enforced by this simple numeric/date API. Other day counts, timestamps, multiple currencies, market-data completeness, spreadsheet compatibility, fresh installation, notebooks and other platforms were not tested. Bounded discount-factor evaluation may reject cases another order could represent. F28, F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-10-irregular-cash-flows-review/review.py
```

Next: Section 10.12.
