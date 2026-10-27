# Book 1 QA — Chapter 14 Reference Runtime

**Status:** Scoped reference runtime passed after one standalone-runner correction; independent mathematical, model, editorial and other-platform review remains pending.  
**Manuscript snapshot:** `f429fb81b8d8f7d228100333c76019d583200d64`. Chapter 14 files were unchanged between that snapshot and repository head `df3f40b1c2cc62fc53c82a8e377f071edb37e21c`. The post-fix run includes the Section 14.3 change published with this record.  
**Environment:** CPython 3.12.14, Linux 6.18.55 x86_64 with glibc 2.39. Run date: 2026-10-27 UTC.

## Results

All 17 section reference suites passed: **204 unittest methods**, 12 per section, with no failures or skips reported. Each fenced reference block was extracted into a separate module, parsed with Python's AST parser, and run using `python -m unittest -v` in an isolated process. [Per-section results](results.json) and [full output](reference-output.log) are retained. Section 14.3's corrected standalone script was also run directly: 12 tests passed and exit code 0; [output](section-03-direct.log).

The earlier Chapter 14 tracker recorded a manually transcribed 14.01 smoke run in Python 3.13.5. This later run used extracted manuscript code on Python 3.12.14/Linux; it does not retroactively establish fidelity of the earlier transcription. The [chapter tracker](../../chapter-14/QA-VALIDATION-TRACKER.md) now distinguishes the historical smoke from this scoped run.

## Finding and correction

Section 14.3's standalone `TextTestRunner` ignored its result. With one deliberately injected failing test, the original runner printed `FAILED` but the process exited **0**. The runner now calls `wasSuccessful()` and exits **1** on failure. The same injected-failure probe after correction exited 1. The normal corrected suite passed.

- [Before probe script](failure-probe-before.py) and [output](failure-probe-before.log): one deliberately failing test; observed exit 0.
- [After probe script](failure-probe-after.py) and [output](failure-probe-after.log): same deliberate failure; observed exit 1.
- The probes are intentionally failing demonstrations, not failures in the normal 204-test run. Their process exits were observed separately from the unittest text logs.

## Reproduction

Retrieve the pinned Book 1 Markdown files under `qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/` in the working directory and replace Section 14.3 with the corrected file in the commit containing this record. Inspect [reference-run.py](reference-run.py), then run in an isolated environment:

```bash
python reference-run.py
```

The script selects the fenced Python block containing `unittest` and `__main__`, parses it, saves it under `/tmp/book1_ch14_01_17` and runs it as a unittest module with a 30-second timeout per section. It checks the process status and unittest summary, not financial correctness. To repeat each deliberate failure probe, run its script directly and inspect its exit status; the before and after probe scripts are intentionally failing. All reference blocks use standard-library imports and synthetic examples.

## Remaining work

Independent probability, distribution, normal-tail and Monte Carlo review; validation of exercises, labs, additional snippets, data assumptions and source references; other Python versions and platforms; and editorial and acceptance review remain pending. The Chapter 14 Actions workflow mentioned in the historical tracker was not run or verified as part of this work. This record does not establish a canonical or production certification.
