# Book 1 QA — Chapters 19 and 20 Reference Runs

**Status:** Scoped runtime checks passed; comprehensive Book 1 QA remains in progress.  
**Manuscript snapshot:** `f429fb81b8d8f7d228100333c76019d583200d64`. The Chapter 19 and 20 manuscript files were unchanged between that snapshot and repository head `cdaeb4d4ad70942e831840f021960a6fdd1552ce`.  
**Environment:** CPython 3.12.14, Linux 6.18.55 x86_64 with glibc 2.39; openpyxl 3.1.5 for the Excel example. Run date: 2026-10-27 UTC.

| Scope | Actual result | Evidence |
|---|---|---|
| Sections 19.1–19.14 | 158 unittest tests passed across 14 isolated executions; all exited 0 | [Results](chapter19-results.json) · [Full output](chapter19-tests.log) |
| Section 19.15 | Decimal arithmetic snippet exited 0 and printed `simple return: 0.015`; it is not a test suite | [Output](chapter19-tests.log) |
| Sections 20.1–20.13 | 168 unittest tests passed across 13 isolated executions; all exited 0 | [Results](chapter20-results.json) · [Full output](chapter20-tests.log) |
| Sections 20.14–20.16 | 36 tests passed in the previous scoped run | [Initial QA evidence](../initial-2026-10-27/README.md) |

The combined Chapter 20 reference runs therefore cover 204 unittest tests from all 16 section reference suites, using the stated source snapshot and environment. This count describes executed test methods; it is not a claim of full functional, numerical, security or model coverage.

## Reproduction

Retrieve the pinned Book 1 Markdown files under `qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/` in the working directory. Inspect the scripts and dependencies before executing in an isolated environment. From that working directory, the following scripts extract the fenced block containing both `unittest` and `__main__` for each indicated section, write isolated scripts to `/tmp`, and run them with the invoking Python interpreter:

```bash
python chapter19-reference-run.py
python chapter20-reference-run.py
```

The actual run invoked the same scripts from `/tmp`; each script uses a 30-second timeout per section. The 19.15 snippet was extracted and executed separately, and its output is included in the combined log. The script checks process exit status and the unittest summary; it does not judge the validity of financial assumptions or the quality of individual assertions. No external API or real financial data was used by these reference blocks.

## Remaining work

Independent mathematical and source review, data semantics and point-in-time edge cases, editorial and copyright review, installed-artifact and other-platform checks, exercises and labs beyond these reference blocks, and validation of the other Book 1 chapters remain pending. The tests were run against extracted examples, not a certified production package. A pass does not establish model suitability or a canonical edition.
