# Section 9.12 — Continuous compounding lab and answer review

Baseline `4a7b02785d8453173a403efd1bda2bae10008eb0`. [Runner](review.py) · [Initial failures](initial-results.json) · [Corrected results](results.json) · [Six answers](ANSWERS.md).

One workflow and six local answers reviewed. Two documented commands, twenty-two additional checks and eight existing embedded methods passed after F46 follow-up. The complete listing was reconstructed verbatim as continuous_compounding.py, executed and compiled in isolation. Prepared Linux CPython 3.12.14; standard library only. No prior module imports, market data or network. Fresh installation and other platforms were not executed.

Five initial F46 probes failed: nonzero Fraction inputs below float range were silently treated as zero in future/present amounts and continuous/effective/nominal rate conversion. The scalar helper now rejects a nonzero input lost during conversion. The existing validation method includes regression assertions; no historical unique method was added. Place the runner at this same relative path in a worktree of the baseline to reproduce the initial failures.

Independent 90-digit Decimal exponentials/logarithms verify worked future/present amounts, every numerical practice answer, nominal-to-continuous conversions, negative rates and interval composition. Signed zero-time identity and unrounded inversion are checked separately. This is a constant-rate model, not infinite transaction posting, a forecast or a real rate recommendation. Calendar year fractions, variable rate paths, settlement rounding, subnormal relative accuracy and arbitrary-range support remain outside scope. The lab produces tables/console output, not an image. F28/F32, platform/notebook and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-09-continuous-review/review.py
```

Next: Section 9.13 formal lab and local answers.
