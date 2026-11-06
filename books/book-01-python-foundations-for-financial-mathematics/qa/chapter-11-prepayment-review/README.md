# Section 11.9 — Extra payments and prepayment review

Baseline `43ccada6e1ea5a10e2e571fc72357b20d46978b4`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Worked-answer review](ANSWERS.md).

The runner saves the sole Python fence verbatim to the documented filename in a temporary directory. Both documented commands and the 12 existing test methods passed on the baseline and corrected source (Linux CPython 3.12). Seven of 31 supplemental predicates initially failed; all 31 passed after correction. The batch records one workflow and 14 local prompts. No historical unique methods were added.

The independent benchmark derives the installment from an explicit sum of discount factors and values the balance prospectively as the remaining scheduled cash flows less accumulated prior extras. It checks every row for the baseline, both recurring extras, delayed extras, start after maturity, zero rate, payoff caps and numeric boundaries. The 0/50/100 extras give 24/22/20 installments and interest of 636.95/570.62/517.09 when rounded for display. Interest savings for 100 extra is 119.85 from the unrounded amounts.

F72: the absolute payoff cutoff erased positive balances, including a residual after an almost full first payment. The recurrence now carries exact rational balances, caps payments against the exact amount due, and stops only at zero. F54 recurred in payment, interest, amount due and aggregate totals; unsupported report ranges now raise ValueError. The exact recurrence accepts decimal input text and returns floats. It is not a currency rounding policy or a performance claim for large terms.

No dependencies beyond Python 3.9+ and its standard library are specified; only the recorded runtime was tested. The supplemental oracle is not another learner lab. Recasting, lender processing, one-off prepayment schedules, irregular accrual, penalties and real contracts are outside the executed workflow. F28, F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-11-prepayment-review/review.py
```

Next: 11.10 — Refinancing Analysis.
