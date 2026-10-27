# Book 1 QA — Chapter 17 Reference Runtime

**Status:** Scoped reference runs passed after one test correction; independent mathematical, model, editorial and other-platform validation remains pending.  
**Manuscript snapshot:** `f429fb81b8d8f7d228100333c76019d583200d64`. Chapter 17 files were unchanged between that snapshot and repository head `3c9d336821d9f327dad06568f36d18e171e0ad96`. The post-fix run additionally includes the Section 17.12 change published with this record.  
**Environment:** CPython 3.12.14, Linux 6.18.55 x86_64 with glibc 2.39; SciPy 1.17.0 and NumPy 2.3.5 for the project and optional snippet. Run date: 2026-10-27 UTC.

| Scope | Actual result |
|---|---|
| Sections 17.1–17.11 | Eleven isolated suites, 12 tests each, passed: 132 tests. |
| Sections 17.12–17.13 | Eight tests each passed after the 17.12 correction: 16 tests. |
| Section 17.14 | Twelve SciPy-based project tests passed. |
| Section 17.15 | Optional SciPy snippet exited 0; rate `0.13066238629180682`, NPV residual `8.526512829121202e-14`. It is a demonstration, not a test suite. |

The post-fix reference run comprises 160 passing unittest methods across 14 sections; no skips were reported. [Per-section results for 17.1–17.13](results-01-13.json) and [combined output](reference-output.log) are retained. The Section 17.14 output and 17.15 snippet output are in the combined log.

## Finding and correction

The original 17.12 `test_yield` required a price residual below `1e-10` while accepting the bisection function's default bracket-width tolerance of `1e-10` in **rate units**. On this run the resulting price residual was approximately `4.2333e-09`, so the test failed. A bound in root units alone does not guarantee an identical numerical bound in price units. The original failure is retained in [section-12-before.log](section-12-before.log).

The test now explicitly requests `width_tol=1e-12` for this example and independently checks the original price-residual threshold. The manuscript explains that the tighter width is specific to the test and is not a general residual guarantee. The corrected eight-test suite passed and the other 17.1–17.13 reference suites were rerun. This correction does not establish a universally appropriate tolerance or certify the solver.

## Reproduction

Retrieve the pinned Book 1 Markdown files under `qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/` in the working directory, replacing Section 17.12 with the corrected version in the commit containing this record. Inspect scripts and dependencies and use an isolated environment:

- [reference-run.py](reference-run.py) extracts the `unittest`/`__main__` block for each section 17.1–17.13 and runs each in a separate process with a 30-second timeout.
- [project-run.py](project-run.py) extracts the Section 17.14 implementation and test blocks and runs `python -m unittest -v test_financial_solver`.
- [snippet-run.py](snippet-run.py) extracts and runs Section 17.15's optional snippet.

```bash
python reference-run.py
python project-run.py
python snippet-run.py
```

The scripts write temporary files and logs under `/tmp/book1_ch17_01_14`. The recorded test runs used synthetic data; SciPy and NumPy versions are noted above. Other illustrative blocks and all lab steps were not executed by these scripts.

## Remaining work

Independent mathematical and numerical analysis, convergence and edge-case review, verification of SciPy behavior across supported environments, exercise and lab review, source and copyright review, installed-artifact checks and editorial acceptance remain pending. These results are scoped to extracted reference examples, not a production package or a certified financial model.
