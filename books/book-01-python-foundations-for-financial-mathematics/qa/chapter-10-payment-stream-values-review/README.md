# Section 10.10 — Payment-stream valuations review

Baseline `c68f73dfd6406ab492514a2f1781821d62b2d000`. [Runnable review](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Twelve prompt records](ANSWERS.md).

Both documented commands and all twelve existing methods passed on both versions. Four of 32 additional predicates initially failed; all 32 pass on the corrected source. The runner extracts the sole Python listing verbatim, saves it as payment_stream_values.py, runs its demonstration and tests, and compiles it in isolation. The console prints PV = −17.66 (ASCII minus in the recorded output). Prepared Linux CPython 3.12.14, standard library only; save/run/compile and filename requirements verified. No earlier module, file data, network or package installation is needed.

F54 recurred when either the discount factor or a nonzero valued payment rounded to zero; both paths now reject silent loss. F56 recurred in two exact special cases: a zero amount did not need an overflowing factor, and a zero rate did not need to convert a very large integer period difference to float. Dates, rate and amounts are still validated before the shortcuts. Four regression cases were added inside an existing method, with no new historical unique methods. Initial failures can be reproduced with this runner against baseline source. The supported-range policy can reject a factor even where another scaling method could represent the monetary value.

Independent rational sums verify signed, repeated, unsorted, ordinary, due and deferred streams, and horizons before, at and after a payment. The mixed fixture has PV −23500/1331 and period-3 value −23.50. A generator and cancellation case also pass. The audit answer describes a comparison with a closed-form formula; this batch benchmarks the exact timeline source against independent rational sums, not an added closed-form implementation. No contractual day-count, rounding, variable rates, fresh installation, notebook or other platform execution is claimed. F28, F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-10-payment-stream-values-review/review.py
```

Next: Section 10.11.
