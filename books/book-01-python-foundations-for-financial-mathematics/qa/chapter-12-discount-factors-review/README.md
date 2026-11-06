# Section 12.14 — Discount Factors and Spot Rates review

Baseline: `dd7d34774d9996d01aa75ed3a932d5212996c643`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Answers](ANSWERS.md).

The runner extracts the single Python fence verbatim, executes the named demo and 12 existing methods, then compiles the same file. Both commands passed on both versions in the recorded Linux CPython runtime. Seven of 45 additional predicates failed initially; all 45 passed after correction. Counts: one workflow, 18 local answers, one separately scoped mini-project, no historical unique methods added.

The independent benchmark uses rational growth factors for annual and periodic quotes and a separate Decimal exponential for continuous compounding. It checks all five project nodes, four forwards, $1,000 zero prices, the worked two-flow price and the five-year coupon bond. Supplemental conversion of the project spot rates to continuous quotes gives equivalent factors and the same 1,024.574345005014 model PV. The exact demo covers three nodes and the two-flow example only.

F91: periodic multi-flow PV could not accept an explicit frequency and inverse quotes could round to the excluded rate boundary. F54 recurred in underflowed factors, overflowed ratios, nonfinite outputs and premature rounding or overflow of scaled contributions. The lab validates the compounding basis, nets signed flows at each tenor and computes in a local Decimal context before reporting floats.

Standalone Python 3.9+ with standard library only. This is a supplied-rate valuation workflow, not a bootstrap or market quote feed. Cancellation at arbitrary scales, irregular dates, contract conventions, platform portability and independent acceptance were not established. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-12-discount-factors-review/review.py
```

Next: 12.15 — Forward Rates.
