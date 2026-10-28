# Chapter 6 — Reference runtime evidence reconciliation

**Date:** 2026-10-27. **Reviewer:** Codex. **Source:** Book 1 manuscript baseline `f429fb81b8d8f7d228100333c76019d583200d64`. Chapter 6 manuscript files were unchanged through `4a5a63c02e5d1b06c1226964f63e4b33c4db16d8`; GitHub comparison returned no changed Book 1 Chapter 6 paths. [results.json](results.json) records each source file's SHA-256.

## Scoped result

PASS: 148 unittest methods across 17 suites, with no skips, failures or errors. Sections 6.1–6.16 each ran eight tests; the Section 6.17 companion solutions ran twenty tests. All 16 standalone implementation demonstrations exited zero, and all 17 extracted lab directories passed compilation. No manuscript corrections were required.

The manuscripts record earlier test, demonstration and compilation passes on Linux. This run reproduces those execution claims for the complete reference listings. Earlier canonical labels describe publication history and do not constitute independent acceptance under the Book 1 validation tracker.

## Environment and reproduction

Python 3.12.14, Linux x86_64 with glibc 2.39, NumPy 2.3.5. Tests and demonstrations ran with `-W error::FutureWarning`.

From the repository root:

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-06-runtime/run_reference_suites.py books/book-01-python-foundations-for-financial-mathematics/chapter-06 /tmp/chapter06-repro
```

The runner extracts complete implementation and unittest blocks into separate lab directories without rewriting their contents. Suites run via `python -W error::FutureWarning -m unittest -v test_reference`; implementations run as separate demonstration processes; each directory is checked with `python -m compileall -q .`. The companion solution listing runs as a test suite, with no separate demonstration. [all-tests.log](all-tests.log) retains detailed test, demonstration and compilation output. JSON records the exit status of each operation.

## Project and performance observations

The portfolio project printed an opening value of 1000.00 and these scenario results:

| Scenario | Return | Ending value | P&L |
|---|---:|---:|---:|
| up | 4.50% | 1045.00 | 45.00 |
| down | -10.50% | 895.00 | -105.00 |
| flat | 0.00% | 1000.00 | 0.00 |

The Section 6.15 benchmark completed its correctness gates for sizes 3, 1000 and 100000. [benchmark.json](benchmark.json) preserves the current raw timing samples and limited host metadata. These are observations on this shared execution host, not expected test values, historical timing reproductions, universal speed rankings or production performance guarantees.

## Limits and next work

Passing existing reference checks does not independently establish every financial formula, exercise answer, statistical assumption or numerical error bound. Windows instructions, external data, alternative NumPy versions, production packaging and comprehensive performance or memory analysis were not validated. Broader mathematical, source, platform and acceptance reviews remain pending. Continue with Chapter 5 runtime evidence reconciliation.
