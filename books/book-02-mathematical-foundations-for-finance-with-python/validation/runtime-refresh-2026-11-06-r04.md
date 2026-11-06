# V-85 — Book 02 pinned runtime refresh

**Executable revision:** `5621a516346213dd09780c0eba7c49a402aee143`  
**Result:** 550 Python files compiled, all 337 discovered scripts exited zero, and all 551 required source and fixture blobs matched before and after execution. Chapter 19 accounted for 47 files and 37 passing scripts.

[Runtime manifest and per-script results](runtime-refresh-2026-11-06-r04.json) · [Euler analytical boundary evidence](chapter-19-euler-analytical-boundary-followup.md) · [Next event-order baseline](chapter-19-project-event-order-boundary-baseline.md)

The manifest came from the pinned recursive tree: all Book 02 Python sources and the Section 1.14 JSON fixture. Replay with `git hash-object <path>` for each manifest file, `py_compile.compile(path, doraise=True)` for each Python file, and `python <basename>` with assertions enabled from the parent directory of each tracked `check_*.py` or `test_*.py`. Each script had a 60-second timeout. The log retains exits and timings; successful stdout/stderr were omitted.

Environment: `3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]`; `Linux-6.18.57-x86_64-with-glibc2.41`. This candidate Linux pass applies to the named source and discovery rule. Independent mathematical and editorial review, supported-platform validation, canonical and release decisions remain pending.
