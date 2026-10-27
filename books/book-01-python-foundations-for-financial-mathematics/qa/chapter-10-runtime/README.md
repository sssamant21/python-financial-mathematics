# Book 1 QA — Chapter 10 Reference Runtime

**Status:** Scoped reference runtime passed after two corrections; independent mathematical, financial, editorial and other-platform review remains pending.  
**Manuscript snapshot:** `f429fb81b8d8f7d228100333c76019d583200d64`. Chapter 10 files were unchanged between that snapshot and repository head `96bebc11db9ea6bfa28097d4c33cd410a3314a98`. The post-fix run includes the Section 10.1 and 10.7 changes published with this record.  
**Environment:** CPython 3.12.14, Linux 6.18.55 x86_64 with glibc 2.39. Run date: 2026-10-27 UTC.

## Results

After correction, 15 extracted section reference suites passed: **174 unittest methods**, with no failures or skips reported. Section 10.1 has 8 tests, Sections 10.2 and 10.3 have 10 each, Section 10.7 has 14 including two added regressions, and the remaining 11 sections have 12 each. Each fenced reference block was extracted into a separate module, parsed and run using `python -m unittest -v` in an isolated process. [Per-section results](results.json) and [post-fix output](reference-output.log) are retained.

## Findings and corrections

- **Section 10.1 — escaped Markdown:** Backticks in the source were escaped, causing code fences and inline code to render as literal text rather than intended Markdown. The escapes were removed, making the reference block extractable. Its 8 tests passed in this scoped run.
- **Section 10.7 — near-equal rates:** The original near-equal test failed: for first payment 100, discount `0.05`, growth `0.05 + 1e-10`, and 12 periods, the original closed form returned `1142.8571276498753` versus timeline value approximately `1142.8571434557823`. The original [failure log](section-07-before.log) is retained. Subtracting near-equal `log1p` values lost precision.
- The implementation now uses `log1p((growth-discount)/(1+discount))` where that ratio is finite and greater than −1, and falls back to a difference of logarithms otherwise. A separate 70-digit Decimal timeline calculated from the exact binary float inputs gave approximately `1142.8571434557823180868932711208984`; the revised result was approximately `1142.857143455782`. Two regression tests cover that benchmark and an extreme-ratio fallback.

All 15 suites were rerun after correction. The fallback and extreme-domain behavior still require numerical analysis; passing these examples does not prove accuracy for every input or certify the valuation model.

## Reproduction

Retrieve the pinned Book 1 Markdown files under `qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/` in the working directory and replace Sections 10.1 and 10.7 with the corrected files in the commit containing this record. Inspect [reference-run.py](reference-run.py), then run in an isolated environment:

```bash
python reference-run.py
```

The script selects each section's fenced Python block containing `unittest` and `__main__`, parses it, saves it under `/tmp/book1_ch10_01_15` and executes it as a unittest module with a 30-second timeout per section. The selected blocks use standard-library imports and synthetic data; no external service was required. The run checks the reference suites, not every lab, exercise or illustrative snippet.

## Remaining work

Independently review annuity and perpetuity domains, equal/near-equal rates and extreme values, payment timing, discounting, IRR roots, cash-flow calendars, exercises, source attribution and editorial consistency. Verify other platforms and artifact packaging where appropriate. This record is scoped runtime evidence, not canonical or production certification.
