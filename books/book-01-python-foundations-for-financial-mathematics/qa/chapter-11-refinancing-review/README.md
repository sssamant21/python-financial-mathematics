# Section 11.10 — Refinancing review

Baseline `62e3433cbf27e606cd84e782e414a98d2d0c7943`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Worked-answer review](ANSWERS.md).

The runner extracts the sole Python fence verbatim and runs both documented commands on Linux CPython 3.12.14. Both commands and all 12 existing methods passed on the baseline and correction. Ten of 41 supplemental predicates initially failed; all 41 passed after correction. This is one workflow and 14 local records; no historical unique methods were added.

The independent benchmark sums individual discount factors, advances the principal by the retrospective recurrence, and discounts each installment and terminal balance separately. The source uses closed-form annuity factors and a prospective residual. The example gives payments of 1,432.86 and 1,265.30, savings of 167.56 per month, and a simple break-even threshold of 18 installments. At discount rate 0.003 per month, keep-minus-refinance PV is −89.13, +5,218.60 and +9,863.84 at 12, 36 and 60 months respectively. It is not the same comparison as the payment-only threshold.

F54 recurred in positive payment underflow and nonfinite reports. F56 recurred where an unnecessary payment or discount denominator exceeded float range despite a finite requested balance or PV. F73 covered a truthy nonboolean flag, cancellation of a nonzero payment difference, and a rounding error before the whole-period ceiling. The corrected lab uses rational decimal inputs and computes the ceiling before converting reported amounts. A zero upfront threshold does not prove economic savings. A threshold beyond the period of overlap extrapolates the payment difference.

Python 3.9+ and the standard library are specified; no earlier lab or file is needed. Only the recorded runtime was executed. The runner's oracle is supplemental validation, not a second learner lab. This model does not cover real loan offers, regulatory APR, taxes, escrow, irregular dates, penalties, or horizons after one alternative matures. Exact powers are intended for teaching-sized terms. F28, F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-11-refinancing-review/review.py
```

Next: 11.11 — Effective Borrowing Cost.
