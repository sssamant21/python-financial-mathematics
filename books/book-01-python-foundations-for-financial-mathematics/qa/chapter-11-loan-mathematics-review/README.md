# Section 11.1 — Loan mathematics review

Baseline `4846e5932a843c6f67b1611e1842d0d98268f920`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Twelve local answers](ANSWERS.md).

Two documented commands and twelve existing methods passed on both versions. Nine of 32 additional predicates initially failed; all 32 pass after correction. The sole Python fence is extracted verbatim as loan_mathematics.py, run and compiled in isolation with prepared Linux CPython 3.12.14 and the standard library. The filename and save/run/compile sequence were checked. No earlier module, data, package installation or network is required. The exact console displays payment 443.21 and balance after 12 of 5149.58.

F54: tiny rates lost the payment or balance in intermediate arithmetic, and unsupported nonzero payment, interest and balance amounts silently rounded to zero or produced a wrong retained balance. The lab evaluates bounded unit factors and rejects unrepresentable positive results. F56: obtaining the known opening balance incorrectly required a representable payment. Opening and closing balances now return directly after validation. F66: near-payoff subtraction lost a positive zero-rate balance; subtraction of almost equal payment and interest lost the one-period principal and left a false closing balance. Remaining/original factor ratios and direct principal evaluation remove the demonstrated cancellation. Nine regression assertions are inside an existing method; no historical unique methods were added. Reproduce initial failures with the same runner on baseline source.

The independent benchmark discounts 24 unit payments using exact Fraction powers, then derives payment and advances the balance with an exact retrospective recurrence. It checks components, midterm/near-final balances and total principal reconciliation. The source uses a prospective formula, so this is a distinct numerical derivation. Signs, rate conventions and contractual caveats are conceptual; no lender, contract, payment calendar, cent-rounded schedule, fee/APR, prepayment, fresh installation, notebook or additional platform was tested. Some finite outcomes remain unsupported by the bounded factor calculation. F28, F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-11-loan-mathematics-review/review.py
```

Next: 11.2 — Principal, Rate, Term, and Payment.
