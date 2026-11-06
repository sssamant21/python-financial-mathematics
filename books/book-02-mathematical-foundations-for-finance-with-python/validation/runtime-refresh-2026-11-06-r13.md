# V-94 — Book 02 full runtime refresh

Executable source: [`44c6a0bcd5d5e8e6ab8ac84e9691c89610d3ed3e`](https://github.com/sssamant21/python-financial-mathematics/tree/44c6a0bcd5d5e8e6ab8ac84e9691c89610d3ed3e/books/book-02-mathematical-foundations-for-finance-with-python/). [Per-path results and exact blob manifest](runtime-refresh-2026-11-06-r13.json) · [Chapter 21 capstone receipt](chapter-21-integrated-provenance-followup.md).

| Check | Result |
|---|---:|
| Book 02 Python files compiled | 559/559 |
| Check scripts exited zero | 346/346 |
| Required source and fixture blobs verified before and after | 560/560 |

The pinned recursive tree supplied all Book 02 Python paths and `chapter-01/data/section-1.14-cases.json`. Git blob SHA-1 values matched before and after execution. Each Python file compiled with `py_compile.compile(path, doraise=True)`; each `check_*.py` and `test_*.py` ran separately from its containing directory with assertions enabled and a 60-second timeout. The new capstone check runs as a validation script and invokes the actual report in isolated temporary directories. The JSON retains paths, statuses, timings and environment.

Runtime: `3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]` on `Linux-6.18.57-x86_64-with-glibc2.41`. This pass is scoped to the observed Linux candidate runtime. Independent review, supported platforms, release acceptance and canonical approval remain pending.
