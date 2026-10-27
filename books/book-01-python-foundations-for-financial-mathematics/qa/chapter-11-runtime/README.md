# Book 1 QA — Chapter 11 Reference Runtime

**Status:** Scoped reference runtime passed; independent mathematical, financial, editorial and other-platform review remains pending.  
**Manuscript snapshot:** `f429fb81b8d8f7d228100333c76019d583200d64`. Chapter 11 files were unchanged between that snapshot and repository head `773899d0f0f52b037c5d34095c1f5b3a136dee8b`.  
**Environment:** CPython 3.12.14, Linux 6.18.55 x86_64 with glibc 2.39. Run date: 2026-10-27 UTC.

## Results

All 14 section reference suites passed: **168 unittest methods**, 12 per section, with no failures or skips reported. Each fenced reference block was extracted into a separate module, parsed with Python's AST parser, and run using `python -m unittest -v` in an isolated process. [Per-section results](results.json) and [full output](reference-output.log) are retained.

These checks exercise the manuscript reference suites using synthetic examples; they do not verify every worked problem, lab, contractual rule or lending product. No manuscript correction was required by these test results.

## Reproduction

Retrieve the pinned Book 1 Markdown files under `qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/` in the working directory. Inspect [reference-run.py](reference-run.py), then run in an isolated environment:

```bash
python reference-run.py
```

The script selects each section's fenced Python block containing `unittest` and `__main__`, parses it, saves it under `/tmp/book1_ch11_01_14` and executes it as a unittest module with a 30-second timeout per section. It checks process status and the unittest summary, not independent mathematical correctness. The selected blocks use standard-library imports and synthetic data; no external service was required.

## Remaining work

Independently review payment timing, rate conversion, amortization, rounding, final-payment handling, extra payments, refinancing, fees and borrowing cost. Review numerical extremes, exercises, labs, source attribution and editorial consistency; verify other platforms and artifacts as appropriate. This record does not constitute canonical, lending-policy or production certification.
