# Section 11.11 — Effective borrowing cost review

Baseline `eaed8250b3400bedc612aa415c3cecb8f23b2af5`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Worked answers and steps](ANSWERS.md).

The runner saves the sole Python fence verbatim as the documented script. Both commands and all 12 existing methods passed on both versions on Linux CPython 3.12.14. Fourteen of 27 supplemental predicates initially failed; all 27 pass after correction. This is one workflow and 14 local records; no historical unique methods were added. The runner accepts an optional manuscript path for baseline replay and overwrites its current results file.

The independent benchmark derives the contractual installment by summing individual discount factors and uses high-precision Newton iteration with a directly differentiated sum. The one-period cases use algebra; the tiny two-period case uses a stable quadratic root. These checks do not copy the source's normalized PV bisection. The example reconciles to 9,800 net proceeds and displays 0.00666269 monthly, 0.079952 nominal annualized and 0.082948 effective annual.

F54 recurred in payment and PV underflow or overflow and annualization overflow. F74 covered tiny positive roots, a large representable root rejected by the old bracketing arithmetic, and invalid PV and annualization inputs. The corrected implementation normalizes PV by the contractual payment, uses an upper bound from the perpetuity, and refines the interval in a local Decimal context. The one-payment equation is solved directly. Reporting remains limited to floats and can round nearby results to the same value. Precision and runtime are scoped to teaching-sized schedules.

Use Python 3.9+ with its standard library; no prior lab or fixture is required. Only the recorded runtime was tested. The supplemental oracle is a verification aid. The model is level and equally spaced with fees withheld upfront; financed fees, official APR rules, irregular dates and real borrower offers were not executed. F28, F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-11-borrowing-cost-review/review.py
```

Next: 11.12 — Numerical and Rounding Considerations.
