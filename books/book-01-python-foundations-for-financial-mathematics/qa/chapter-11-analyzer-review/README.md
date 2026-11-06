# Section 11.13 — Loan and Mortgage Analyzer review

Baseline `41342a08f9f874a6f87154ffe49c93a8cafc55b1`. [Runner](review.py) · [Baseline results](initial-results.json) · [Corrected results](results.json) · [Worked answers and acceptance mapping](ANSWERS.md).

The runner extracts the sole Python fence verbatim, saves it under the documented name, runs the demonstration and 12 existing tests, and compiles it in a temporary directory. Both commands passed on the baseline and correction in the recorded Linux CPython environment. Sixteen of 48 supplemental predicates failed at baseline; all 48 passed after correction. This is one project workflow, 14 local answers and 12 separate acceptance records. No historical unique test methods were added.

The independent oracle derives installments from direct sums of rational discount factors and advances balances by the payment recurrence. It checks every baseline and accelerated row, reported cash totals, a 60-payment balance, and the cash-fee refinance comparison. The example has 360 versus 265 payments, interest of 278,011.65 versus 192,926.32, and interest savings of 85,085.34 using unrounded totals. The ordinary balance at month 60 is 223,330.46 and the refinance heuristic gives 18 months.

F54, F56, F66, F72 and F73 recurred in numeric range, an opening balance depending on payment representability, cancelled principal, false payoff and refinancing arithmetic. The source now uses exact rational model inputs for installments, recurrence and savings, then reports checked floats. F76: the audit previously overlooked malformed period numbers, inconsistent scheduled/extra composition and false payoff at small scale; the demo also omitted Phase D. The audit now checks these internal conditions and the demo reports a balance after 60 payments.

The standalone project requires Python 3.9+ and the standard library. The oracle is supplemental QA. It does not establish independent acceptance or support for arbitrary terms. Optional CSV, CLI, charts, one-time extras and servicing rounding were not implemented by the source and were not executed. No actual lending agreement, underwriting, APR or payoff quote was verified. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-11-analyzer-review/review.py
```

Next: 11.14 — Exercises and Applied Problems.
