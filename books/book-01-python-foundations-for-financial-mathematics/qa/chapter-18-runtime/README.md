# Book 1 QA — Chapter 18 Reference Runtime

**Status:** Reference runtime checks passed in the recorded environment; comprehensive mathematical, model, editorial and platform validation remains pending.  
**Manuscript snapshot:** `f429fb81b8d8f7d228100333c76019d583200d64`. Chapter 18 manuscript files were unchanged between that snapshot and the repository head `a20484672beae64e7c61037af0b11baba2fd7e54`.  
**Environment:** CPython 3.12.14, Linux 6.18.55 x86_64 with glibc 2.39. Run date: 2026-10-27 UTC.

| Scope | Actual result |
|---|---|
| Sections 18.1–18.7 | Seven isolated suites; 10 tests each passed, 70 total. |
| Sections 18.8–18.14 | Seven isolated suites; 12 tests each passed, 84 total. |
| Section 18.15 | Standalone seeded simulation snippet exited 0; output: `mean: 99.96 estimated SE: 0.1406051812050259`. This is an observation from the specified environment, not a test suite or a universal expected sequence. |

All 14 suite processes exited 0; the unittest output reports 154 tests and no failures or skips. [Per-section results](results.json) and [full output](reference-output.log) are retained. The 18.15 snippet uses 10,000 pseudorandom draws and is reported separately.

## Reproduction

Retrieve the pinned Book 1 Markdown files into `qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/` under the working directory. In an isolated environment, inspect and run [reference-run.py](reference-run.py). It extracts the fenced Python block containing `unittest` and `__main__` for each section 18.1–18.14, writes scripts under `/tmp/book1_ch18_01_14`, and runs each with the invoking Python interpreter and a 30-second timeout. The actual run used this extraction-and-execution script. [snippet-run.py](snippet-run.py) provides the equivalent separate extraction and execution of the Section 18.15 snippet. For example, from the working directory containing the snapshot and scripts:

```bash
python reference-run.py
python snippet-run.py
```

The extraction selects the section's reference suite, not every illustrative code block or every lab step. Test and snippet execution used synthetic data and Python standard-library imports; no external service was required. A seeded output may differ across implementations or versions; retain the actual environment with any rerun.

## Limits and remaining work

These checks establish only the recorded runtime behavior of the extracted reference blocks. Independent review of simulation assumptions, distributions, confidence-interval coverage, random-number reproducibility across environments, numerical extremes, performance claims, exercises and labs, source attribution and editorial consistency is still pending. The results do not certify a model or production application. Other Book 1 chapters and clean-artifact, platform and visual checks remain in the broader QA plan.
