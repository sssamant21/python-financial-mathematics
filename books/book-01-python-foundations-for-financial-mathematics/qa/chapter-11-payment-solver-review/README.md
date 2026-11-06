# Section 11.4 — Solving for payment review

Baseline `1d9ccd2b77cf3a3470217743fbca9ec88630666d`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Twelve answers](ANSWERS.md).

Both documented commands and all twelve existing methods passed on both versions. Twelve of 35 additional predicates initially failed; all 35 pass on corrected source. The runner saves the sole Python fence verbatim as solving_for_payment.py, runs the example and tests, and compiles it in isolation using prepared Linux CPython 3.12.14 and the standard library. No earlier module, packages, data or network is needed. The console prints monthly payment 1498.88. Regression assertions are in an existing method; no historical unique methods were added.

F54 recurred in the payment, inverse-principal and first-interest range checks. F56 recurred when the balloon solver first computed an overflowing ordinary payment or positive exponential. F66 recurred when near-equal monetary subtraction erased a small positive scheduled installment. Discounting the balloon in a local 750-digit Decimal context and evaluating the remaining unit-factor equation before float conversion corrects these cases. F67: the first-interest helper accepted a negative rate, invalid term and boolean principal because it skipped validation. Shared loan validation now applies. The same runner on baseline reproduces all initial failures.

Independent Fraction sums value all regular payments, then add the balloon at the final date separately. A separate exact recurrence checks the total-interest identity; no source total-interest API is supplied in this section. The inverse-principal checks use ordinary and zero rates, and the zero/negative regular-payment rejection is tested. The revised formula answers explicitly include zero rates. Monthly-rate and count arithmetic are supplemental, not a lender disclosure or underwriting calculation. Loan contract/APR, exact servicing rounding, fresh installation, notebook and alternate platform acceptance were not tested. Extreme factors and precision boundaries remain bounded; F28, F32 and independent acceptance stay open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-11-payment-solver-review/review.py
```

Next: Section 11.5.
