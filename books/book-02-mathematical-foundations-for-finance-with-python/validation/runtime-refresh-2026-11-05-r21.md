# V-79 — Book 02 pinned runtime refresh

**Executable revision:** `c961e9064fbb07217c8c7af64adf909e399f165f`  
**Result:** 544 Python files compiled, all 331 discovered scripts exited zero, and all 545 required source and fixture blobs matched before and after execution. Chapter 19 accounted for 41 files and 31 passing scripts.

[Runtime manifest and per-script results](runtime-refresh-2026-11-05-r21.json) · [End-period extension evidence](chapter-19-end-period-exponent-followup.md) · [Next RK4 range baseline](chapter-19-rk4-stage-range-baseline.md)

The manifest was derived from the pinned recursive tree: all Book 02 Python sources and the Section 1.14 JSON fixture. Replay with `git hash-object <path>` for each manifest file, `py_compile.compile(path, doraise=True)` for each Python file, and `python <basename>` with assertions enabled from the parent directory of each tracked `check_*.py` or `test_*.py`, with a 60-second timeout per script. The log retains exits and timings; successful stdout/stderr were omitted.

Environment: `3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]`; `Linux-6.18.57-x86_64-with-glibc2.41`. This candidate Linux pass applies to the named source and discovery rule. Independent mathematical and editorial review, supported-platform validation, canonical and release decisions remain pending.
