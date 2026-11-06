# Section 11.6 — Outstanding loan balance review

Baseline `3d4624e1a47463e906fb8897fb88babf955a5583`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Twelve answers](ANSWERS.md).

Both documented commands and all twelve existing methods passed on each version. Twelve of 35 additional predicates initially failed; all 35 pass after correction. The runner saves the sole Python fence verbatim as outstanding_loan_balance.py, runs the demonstration and tests, and compiles it in isolation with prepared Linux CPython 3.12.14 and its standard library. The exact example displays 443.21 and 5149.58. No prior module, package, data or network is required.

F54 recurred in unsupported nonzero amounts and nonfinite results. F56 recurred when known endpoints required an unrepresentable intermediate payment or growth. F66 recurred in nearly paid zero-rate subtraction and a long retrospective calculation with finite balance. Prospective factors avoid an intermediate payment; retrospective subtraction is performed separately in local 750-digit Decimal precision, with an explicit cancellation/range limit. F69: an absolute 1e-9 tolerance accepted amounts exceeding the modeled balance, including a nonzero payment at maturity. The comparison now enforces the stated bound against the computed balance. All twelve regression cases are inside an existing method; no historical unique methods were added. The same runner on unchanged source reproduces the initial failures.

Exact Fraction recurrence and direct sums benchmark both methods at opening, intermediate and maturity dates. Extra-payment checks cover a partial payment, exact principal payoff, and overpayments. Zero-rate branches and the worked balance are now explicit in the answers. This is an instantaneous principal adjustment, not a revised schedule or legal payoff quote. Severe retrospective cancellation can remain unsupported; no contract rounding, fees, calendar accrual, installation, notebook or additional platform was tested. F28, F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-11-outstanding-balance-review/review.py
```

Next: 11.7.
