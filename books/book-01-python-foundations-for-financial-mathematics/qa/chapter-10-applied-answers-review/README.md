# Section 10.15 — Chapter-wide applied answers and acceptance lab

Baseline `2f860f73540630ea58b1bd75616ebfa38e003980`. [Runner](review.py) · [First run](initial-results.json) · [Corrected benchmark on original source](baseline-results.json) · [Final run](results.json) · [Twenty answer records](ANSWERS.md).

Two documented commands and all twelve existing methods passed on both source versions. All 55 additional predicates pass on the final source. The first run had 23 failures, one from the QA predicate requiring both equipment NPVs to be positive. The rational sums showed A is negative and B is positive; changing the predicate from B>A>0 to B>0>A left 22 failures on unchanged source. Both runs are retained. Eight failed answer-completeness predicates and fourteen failed runtime predicates were resolved.

The runner extracts the sole Python fence as chapter10_acceptance.py, runs it and compiles it in isolation on prepared Linux CPython 3.12.14. No external package, data, network or preceding module is required for those commands. Supplemental review invokes exact source functions from 10.8, 10.9 and 10.11 for perpetuity and dated examples, with listing hashes retained. Their embedded tests are not rerun or counted here. Fraction and 100-digit Decimal calculations independently benchmark timelines, geometric valuations, roots and residuals. No external spreadsheet or independent reviewer was used.

F64 adds rounded values and decisions to eight formula-only answers and clarifies signed rather than absolute-magnitude NPV comparison. F65 materializes one-shot IRR input before repeated valuation. F54/F56, F60/F61, F62 and F63 recur in discounted/generated range loss, unsafe bisection, indeterminate roots and skipped input checks. The lab now guards those paths; regressions are inside an existing method. The first payment/date and rate/horizon/count contracts were reviewed. No new historical unique methods were added.

Chapter 10 now has fourteen core workflows, 160 local prompts, six project acceptance records, and this assessment workflow with twenty distinct chapter-wide answers. The rubric remains a suggested educational grading scheme; no external assessment score, production review, cross-version, notebook or platform acceptance was performed. F28 and F32 remain open. Float scaling and order-dependent extreme cancellation remain limitations.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-10-applied-answers-review/review.py
```

Next: Chapter 11, Section 11.1 — Loan Mathematics (confirmed against Master TOC).
