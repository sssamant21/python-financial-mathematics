# V-78 — Book 02 pinned runtime refresh

**Executable revision:** `59f713d346fbcbf14e7125902637cd2f6e2c56e4`  
**Result:** 543 Python files compiled, 330 discovered scripts exited zero, and all 544 required source and fixture blobs matched before and after execution. Chapter 21 accounted for 24 files and 15 passing scripts.

[Runtime manifest and per-script results](runtime-refresh-2026-11-05-r20.json) · [Account transition evidence](chapter-21-capstone-account-range-followup.md) · [Requirements and preflight evidence](chapter-21-capstone-requirements-evidence-map.md) · [Next Section 19.8 baseline](chapter-19-end-period-exponent-baseline.md)

The manifest was derived from the pinned recursive tree: all Book 02 `.py` blobs and the Section 1.14 JSON fixture. Replay with `git hash-object <path>` for each listed file, `py_compile.compile(path, doraise=True)` for each Python file, and `python <basename>` with assertions enabled from the parent directory of each tracked `check_*.py` or `test_*.py`, with a 60-second timeout per script. The log retains exits, timings and failed-script output; successful stdout/stderr were omitted.

Environment: `3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]`; `Linux-6.18.57-x86_64-with-glibc2.39`. This candidate Linux pass is scoped to the named source and discovery rule. Independent mathematical/editorial review, supported-platform validation, canonical and release decisions remain pending.
