# V-98 — Book 02 full runtime refresh

Executable source: [`2a87994b660c5ea1f600a9187edf097d3ca70dce`](https://github.com/sssamant21/python-financial-mathematics/tree/2a87994b660c5ea1f600a9187edf097d3ca70dce/books/book-02-mathematical-foundations-for-finance-with-python/). [Per-path results and exact blob manifest](runtime-refresh-2026-11-07-r04.json) · [INT-01 acceptance reconciliation](chapter-21-equivalent-factor-property-followup.md).

| Check | Result |
|---|---:|
| Book 02 Python files compiled | 563/563 |
| Check scripts exited zero | 350/350 |
| Required source and fixture blobs verified before and after | 564/564 |

The pinned recursive tree supplied all Book 02 Python paths and `chapter-01/data/section-1.14-cases.json`. Git blob SHA-1 values matched before and after execution. Each Python file compiled with `py_compile.compile(path, doraise=True)`; each `check_*.py` and `test_*.py` ran separately from its containing directory with assertions enabled and a 60-second timeout. The JSON retains paths, statuses, timings and environment.

Runtime: `3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]` on `Linux-6.18.57-x86_64-with-glibc2.41`. This pass is scoped to the observed Linux candidate runtime. Independent review, supported platforms, release acceptance and canonical approval remain pending.
