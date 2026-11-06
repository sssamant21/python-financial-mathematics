# V-90 — Book 02 full runtime refresh

Executable source: [`bf9d4fccf807a1ee631a737cb4b20e507808e0cc`](https://github.com/sssamant21/python-financial-mathematics/tree/bf9d4fccf807a1ee631a737cb4b20e507808e0cc/books/book-02-mathematical-foundations-for-finance-with-python/). [Per-path evidence and exact blob manifest](runtime-refresh-2026-11-06-r09.json) · [Section 19.3 applied linear-account follow-up](chapter-19-linear-applied-range-followup.md).

| Check | Result |
|---|---:|
| Book 02 Python files compiled | 555/555 |
| Check scripts exited zero | 342/342 |
| Required source and fixture blobs verified before and after | 556/556 |
| Chapter 19 Python files compiled | 52/52 |
| Chapter 19 check scripts exited zero | 42/42 |

The pinned recursive tree supplied the manifest: all Book 02 Python files and `chapter-01/data/section-1.14-cases.json`. Each staged file's Git blob SHA-1 was compared with the pinned tree both before and after execution. Every Python path was compiled with `py_compile.compile(path, doraise=True)`. Every `check_*.py` and `test_*.py` was run separately as `python SCRIPT` from its containing directory, with assertions enabled and a 60-second timeout. The JSON records the complete inventory, exits, timings and environment.

Runtime: `3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]`, `Linux-6.18.57-x86_64-with-glibc2.41`. This refresh includes the Section 19.3 correction and checker. It covers the selected Linux candidate runtime; independent review, supported-platform validation, release acceptance and canonical approval remain pending.
