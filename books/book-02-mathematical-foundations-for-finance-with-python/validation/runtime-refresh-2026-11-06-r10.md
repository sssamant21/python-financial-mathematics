# V-91 — Book 02 full runtime refresh

Executable source: [`b8d9ad694136393a36aca2c06d9c0798062cb21c`](https://github.com/sssamant21/python-financial-mathematics/tree/b8d9ad694136393a36aca2c06d9c0798062cb21c/books/book-02-mathematical-foundations-for-finance-with-python/). [Per-path results and exact blob manifest](runtime-refresh-2026-11-06-r10.json) · [Section 19.1 follow-up](chapter-19-introductory-range-followup.md).

| Check | Result |
|---|---:|
| Book 02 Python files compiled | 556/556 |
| Check scripts exited zero | 343/343 |
| Required source and fixture blobs verified before and after | 557/557 |
| Chapter 19 Python files compiled | 53/53 |
| Chapter 19 check scripts exited zero | 43/43 |

The pinned recursive tree supplied the inventory: all Book 02 Python paths and `chapter-01/data/section-1.14-cases.json`. Git blob SHA-1 values matched both before and after execution. Every Python file compiled with `py_compile.compile(path, doraise=True)`. Each `check_*.py` and `test_*.py` ran as a separate process from its containing directory with assertions enabled and a 60-second timeout. The JSON retains paths, statuses, timings and environment.

Runtime: `3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]` on `Linux-6.18.57-x86_64-with-glibc2.41`. This pass is scoped to the selected candidate runtime. Independent review, supported platforms, release acceptance and canonical approval remain pending.
