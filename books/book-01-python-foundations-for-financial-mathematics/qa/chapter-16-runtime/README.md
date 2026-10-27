# Book 1 QA — Chapter 16 Reference Runtime

**Status:** Scoped reference runs passed after two corrections; independent mathematical, model, editorial and other-platform review remains pending.  
**Manuscript snapshot:** `f429fb81b8d8f7d228100333c76019d583200d64`. Chapter 16 files were unchanged between that snapshot and repository head `a54a21d92b921267447a80ed1776159a918e8727`. The post-fix run includes the Section 16.6 and 16.9 changes published with this record.  
**Environment:** CPython 3.12.14, Linux 6.18.55 x86_64 with glibc 2.39. Run date: 2026-10-27 UTC.

## Results

Sixteen reference suites, each containing 12 unittest methods, passed after correction: **192 tests**, no failures or skips. Each was extracted and run in a separate process using synthetic examples. [Per-section results](results.json) and [full post-fix output](reference-output.log) are retained. These tests do not execute every illustrative block, lab step or exercise, and do not establish the correctness or suitability of all portfolio models.

## Findings and corrections

- **Section 16.6 — short-position variance:** The original test and Exercise 20 worked answer expected `0.0576` for weights `[1.2, -0.2]` and covariance `[[0.04, 0.01], [0.01, 0.09]]`. Direct expansion gives `1.2² × 0.04 + (−0.2)² × 0.09 + 2 × 1.2 × (−0.2) × 0.01 = 0.0564`. The expected test value and worked answer were corrected. The [original failure](section-06-before.log) is preserved.
- **Section 16.9 — degenerate minimum-variance case:** The original invalid-input test expected an exception for equal volatilities and correlation +1, while the implementation returns a documented result indicating that all fully invested weights have identical variance. The test now checks the returned `None` weight and explanatory note instead. The [original failure](section-09-before.log) is preserved.

All 16 suites were rerun after the changes. Further review of positive-semidefinite covariance validation, numerical tolerances, degeneracy and portfolio assumptions is still required; these corrections do not certify the models.

## Reproduction

Retrieve the pinned Book 1 Markdown files under `qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/` in the working directory and replace Sections 16.6 and 16.9 with the corrected files in the commit containing this record. Inspect [reference-run.py](reference-run.py) and execute it in an isolated environment:

```bash
python reference-run.py
```

The script extracts each section's fenced Python block containing `unittest` and `__main__`, writes separate scripts and logs under `/tmp/book1_ch16_01_16`, and uses the invoking interpreter and a 30-second timeout per section. The reported run used standard-library reference blocks; no external service or real financial data was required.

## Remaining work

Independently review all formulas and worked exercises, covariance matrix validity and positive-semidefinite handling, portfolio constraints, data alignment, estimation risk, numerical extremes, labs, source attribution, accessibility and editorial consistency. Verify supported platforms and installed artifacts where relevant. This record is scoped runtime evidence, not a canonical or production certification.
