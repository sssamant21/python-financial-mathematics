# Section 11.2 — Principal, rate, term, and payment review

Baseline `4c9d4825d2debbc4f3bebf74232d901f5486471b`. [Runner](review.py) · [Initial run](initial-results.json) · [Expanded baseline](expanded-baseline-results.json) · [Corrected run](results.json) · [Twelve answers](ANSWERS.md).

Both documented commands and all twelve existing methods passed on both source versions. Nine of 33 additional predicates failed first; adding the smallest-rate positive-interest check gave ten failures of 34 on unchanged source. All 34 pass after correction. The runner saves the sole Python listing verbatim as loan_variables.py, runs the example and tests, and compiles it in isolation with prepared Linux CPython 3.12.14 and its standard library. No earlier module, package, network, or data is required. Existing-method regressions add no historical unique methods.

F54 recurred in payment, conversion, inverse principal and total-interest range checks. Unit factors avoid the reproduced intermediate payment loss, and unsupported nonzero results are rejected. F56 recurred when finite interest depended on an overflowing payment. F66 recurred when small positive interest disappeared in total-payment subtraction. A local 750-digit Decimal evaluation retains the subtraction before the final bounded float conversion; the benchmark independently sums exact unit discounts with Fraction. Positive tiny rates, zero rate and extreme-principal cases are distinct predicates. The same runner on baseline reproduces the expanded failures.

Independent rational sums and a 100-digit Decimal monthly conversion benchmark payment, total interest and inverse principal. The nominal conversion is for a stated nominal annual rate compounded monthly, not an assertion about regulated APR. The twelve answers include supplemental purchase/count arithmetic and conceptual mortgage exclusions; no credit decision, contract, tax/insurance amount, cent-rounded servicing schedule, fresh installation, notebook or platform acceptance was tested. Float/Decimal factor ranges and independently certified results remain out of scope. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-11-loan-variables-review/review.py
```

Next: Section 11.3.
