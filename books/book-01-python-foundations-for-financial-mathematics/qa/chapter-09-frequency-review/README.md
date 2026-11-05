# Section 9.11 — Compounding frequency lab and answer review

Baseline `1ec37d370f684966291d86fb9bd4a6177ec29176`. [Runner](review.py) · [Initial failures](initial-results.json) · [Corrected results](results.json) · [Six answers](ANSWERS.md).

One workflow and six local answers reviewed. Two documented commands, twenty-nine additional checks and eight existing embedded methods passed after F46/F47 corrections. The listing was reconstructed verbatim as compounding_frequency.py, executed and compiled in isolation. Console expectations are independently derived using 90-digit Decimal powers and formatted to the documented source precision. Prepared Linux CPython 3.12.14; standard library only. No prior imports, real product data or network. Fresh installation and other platforms were not run.

**F46 follow-up:** Nonzero Fraction rates below float range became zero in both conversion directions. The scalar helper now retains the original value until conversion checks finish and rejects the loss.

**F47:** nominal_for_effective(5e-324,12) returned zero for a nonzero float input. log1p(e)/12 rounds to zero before expm1, although the exact conversion requires a positive nominal rate. The reverse function now rejects nonzero-to-zero conversion rather than returning an ordinary zero rate. It does not promise support for that rearranged numerical range. Three initial failing checks are retained; three assertions were added within the existing invalid/zero method, so historical unique method count remains unchanged. Reproduce the initial failures by running this runner at the same relative path in a worktree of the baseline.

Independent Decimal and rational references verify the entire frequency table, fixed-effective nominal quotes/balances, quarterly exercises, thirty-six monthly periods and the finite-frequency comparison against the exponential limit. This is equal-period mathematics, not an actual bank day-count or a forecast. Partial periods, posting rules, fees, legal disclosure meanings, exact settlement and arbitrary-range accuracy remain outside scope. No chart workflow. F28/F32, platform/notebook and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-09-frequency-review/review.py
```

Next: Section 9.12 formal lab and local answers.
