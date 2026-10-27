# Book 1 QA — Chapter 9 Reference Runtime

**Status:** Scoped reference runtime passed after Markdown corrections; independent mathematical, financial, editorial and other-platform review remains pending.  
**Manuscript snapshot:** `f429fb81b8d8f7d228100333c76019d583200d64`. Chapter 9 files were unchanged between that snapshot and repository head `169bd5ea85c96c6417c14fb8a6c354502363b31a`. The run additionally includes the Markdown formatting corrections to Sections 9.11–9.17 published with this record.  
**Environment:** CPython 3.12.14, Linux 6.18.55 x86_64 with glibc 2.39. Run date: 2026-10-27 UTC.

## Results

All 17 extracted reference suites passed: **152 unittest methods**, with no failures or skips reported. Sections 9.1–9.15 contain eight tests each, Section 9.16 contains 12, and Section 9.17 contains 20. Each fenced reference block was extracted into a separate module, parsed with Python's AST parser, and run using `python -m unittest -v` in an isolated process. [Per-section results](results.json) and [full output](reference-output.log) are retained.

These checks execute the selected reference suites on synthetic examples; they do not establish that all exercises, labs, numerical ranges or financial conventions are correct. Earlier Chapter 9 execution claims were not independently reconciled with their historical evidence in this run.

## Finding and correction

Sections 9.11–9.17 contained escaped backticks in Markdown, including the code fences. Consequently the reference blocks were rendered as literal text and not recognized by the initial fenced-code extractor. The escapes were removed from fences and inline code; the underlying Python code was not intentionally changed. The corrected blocks were then extracted and included in the 152-test run. Broader Markdown and links still require review.

## Reproduction

Retrieve the pinned Book 1 Markdown files under `qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/` in the working directory and replace Sections 9.11–9.17 with the corrected versions in the commit containing this record. Inspect [reference-run.py](reference-run.py) and run in an isolated environment:

```bash
python reference-run.py
```

The script selects each section's fenced Python block containing `unittest` and `__main__`, parses it, saves it under `/tmp/book1_ch09_01_17` and executes it as a unittest module with a 30-second timeout per section. It checks process status and the unittest summary, not independent mathematical correctness. The selected blocks use standard-library imports and synthetic data; no external service was required.

## Remaining work

Independently verify time-value formulas, rates and compounding conventions, boundaries, numerical extremes, cash-flow timing, exercise answers, remaining lab steps, source attribution and editorial consistency. Reconcile historical evidence and check other platforms and artifact packaging where appropriate. This is scoped runtime evidence, not canonical or production certification.
