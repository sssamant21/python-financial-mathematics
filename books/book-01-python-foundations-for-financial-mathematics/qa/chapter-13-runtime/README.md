# Book 1 QA — Chapter 13 Reference Runtime

**Status:** Scoped reference runs passed after one test correction; independent mathematical, model, editorial and other-platform review remains pending.  
**Manuscript snapshot:** `f429fb81b8d8f7d228100333c76019d583200d64`. Chapter 13 files were unchanged between that snapshot and repository head `76b6e049be0447647c6986a1a56d028e974aeafa`. The post-fix run additionally includes the Section 13.14 change published with this record.  
**Environment:** CPython 3.12.14, Linux 6.18.55 x86_64 with glibc 2.39. Run date: 2026-10-27 UTC.

## Results

Fifteen extracted reference suites passed after correction: **180 unittest methods**, 12 per section, with no failures or skips reported. Each was parsed and run in a separate process using synthetic examples. [Per-section results](results.json) and [post-fix output](reference-output.log) are retained. These checks do not execute every illustrative block, lab or exercise and do not certify an investment-performance methodology.

## Finding and correction

Section 13.14's original test required exact list equality between computed returns and `[0.1, -0.1]`. For prices `[100, 110, 99]`, the computed floats were `[0.10000000000000009, -0.09999999999999998]`, so that assertion failed despite agreement with the mathematical values within normal floating-point rounding. The test now checks the result length and compares each value with an absolute tolerance of `1e-12` in decimal return units. This illustrative test tolerance is not a universal financial materiality threshold. The [original failure](section-14-before.log) is retained, and all 15 suites were rerun.

## Reproduction

Retrieve the pinned Book 1 Markdown files under `qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/` in the working directory and replace Section 13.14 with the corrected version in the commit containing this record. Inspect [reference-run.py](reference-run.py) and run it in an isolated environment:

```bash
python reference-run.py
```

The script extracts each section's fenced Python block containing `unittest` and `__main__`, parses it, writes separate modules and logs under `/tmp/book1_ch13_01_15`, and runs each using the invoking interpreter's `unittest` module with a 30-second timeout. The reference suites use standard-library imports and synthetic data. No external service was required.

## Remaining work

Independently review return conventions, distributions, time- and money-weighted return, multiple or absent IRR roots, volatility, drawdowns, risk-adjusted metrics, numerical extremes, exercises, labs, source data and editorial attribution. Verify supported platforms and artifact packaging as appropriate. This is scoped runtime evidence, not canonical or production certification.
