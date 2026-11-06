# V-93 — Book 02 full runtime refresh

Executable source: [`7b2430e2a88336993306dd6b1394ee250cb357e2`](https://github.com/sssamant21/python-financial-mathematics/tree/7b2430e2a88336993306dd6b1394ee250cb357e2/books/book-02-mathematical-foundations-for-finance-with-python/). [Per-path results and exact blob manifest](runtime-refresh-2026-11-06-r12.json) · [Section 20.7 publication checks](chapter-20-manifest-publication-followup.md).

| Check | Result |
|---|---:|
| Book 02 Python files compiled | 558/558 |
| Check scripts exited zero | 345/345 |
| Required source and fixture blobs verified before and after | 559/559 |
| Chapter 20 Python files compiled | 35/35 |
| Chapter 20 check scripts exited zero | 24/24 |

The pinned recursive tree supplied all Book 02 Python paths and `chapter-01/data/section-1.14-cases.json`. Git blob SHA-1 values matched before and after execution. Each Python file compiled with `py_compile.compile(path, doraise=True)`; each `check_*.py` and `test_*.py` ran separately from its containing directory with assertions enabled and a 60-second timeout. The JSON retains paths, statuses, timings and environment.

Runtime: `3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]` on `Linux-6.18.57-x86_64-with-glibc2.41`. This pass is scoped to the observed Linux candidate runtime. Independent review, supported platforms, release acceptance and canonical approval remain pending.
