# Section 9.10 — Effective versus nominal rate review

Baseline `a3f1269fd8fff56114f3db54ab98505b9325f977`. [Runner](review.py) · [Initial failures](initial-results.json) · [Corrected results](results.json) · [Five answers](ANSWERS.md).

One workflow and five local answers reviewed. Two documented commands, fifteen additional checks and eight existing embedded methods passed after F46 follow-up. The full listing was reconstructed verbatim as rate_conventions.py, executed and compiled in isolation. Prepared Linux CPython 3.12.14; standard library only. No prior module, external quote data or network. Fresh installation and Windows substitution were not executed.

F46 was reproduced in both conversion directions with a nonzero Fraction rate below float range. The validator now preserves the original scalar during conversion and rejects a lost nonzero input. Both assertions are within the existing small-rate method; no historical method is added. Initial failures and corrected results retained. Reproduce the initial run using this runner at the same relative path in a worktree of the baseline.

Independent 90-digit Decimal calculations verify forward/reverse conversions, quarterly exercises, negative rates and 1e-16 preservation. A rational 36-month factor checks the equivalent three-year balance. The small-rate comparisons use absolute tolerance 1e-30; ordinary rates use 1e-14, and balances 1e-9. Common-basis ranking holds synthetic fees/risk/terms fixed; fee and disclosure implications remain conceptual. No APR/APY legal interpretation, real rate recommendation, contractual rounding or arbitrary-range guarantee. No image workflow. F28/F32, platform/notebook and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-09-rate-conventions-review/review.py
```

Next: Section 9.11 formal lab and local answers.
