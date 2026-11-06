# V-92 — Book 02 full runtime refresh

Executable source: [`641c6ad0304d242fd3a780b12908726b4778d724`](https://github.com/sssamant21/python-financial-mathematics/tree/641c6ad0304d242fd3a780b12908726b4778d724/books/book-02-mathematical-foundations-for-finance-with-python/). [Per-path results and exact blob manifest](runtime-refresh-2026-11-06-r11.json) · [Section 20.7 follow-up](chapter-20-execution-provenance-followup.md).

| Check | Result |
|---|---:|
| Book 02 Python files compiled | 557/557 |
| Check scripts exited zero | 344/344 |
| Required source and fixture blobs verified before and after | 558/558 |
| Chapter 20 Python files compiled | 34/34 |
| Chapter 20 check scripts exited zero | 23/23 |

The pinned recursive tree supplied all Book 02 Python paths and `chapter-01/data/section-1.14-cases.json`. Git blob SHA-1 values matched before and after execution. Every Python file compiled with `py_compile.compile(path, doraise=True)`. Each `check_*.py` and `test_*.py` ran separately from its containing directory with assertions enabled and a 60-second timeout. The new Section 20.7 check additionally uses a temporary local Git fixture. JSON retains paths, statuses, timings and environment.

Runtime: `3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]` on `Linux-6.18.57-x86_64-with-glibc2.41`. This pass is scoped to the selected candidate runtime. Independent review, supported platforms, release acceptance and canonical approval remain pending.
