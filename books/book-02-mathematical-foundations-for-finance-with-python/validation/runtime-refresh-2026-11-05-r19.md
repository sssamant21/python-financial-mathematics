# V-77 — Book 02 pinned runtime refresh

**Executable revision:** `bc29b0d67dfd61b3d522d36d956b768101fee0ab`  
**Result:** 542 Python files compiled, all 329 discovered scripts exited zero, and all 543 required source and fixture blobs matched before and after execution. Chapter 21 accounted for 23 files and 14 passing scripts. This refresh includes the new replication and allocation checkers.

[Runtime manifest and per-script results](runtime-refresh-2026-11-05-r19.json) · [Replication evidence](chapter-21-capstone-replication-range-followup.md) · [Allocation evidence](chapter-21-capstone-allocation-range-followup.md) · [Next account baseline](chapter-21-capstone-account-range-baseline.md)

Discovery used all tracked Book 02 `.py` files and the Section 1.14 JSON fixture in the executable revision's recursive tree. Each file was matched to its Git blob SHA before compilation and again after the checks. Each Python file was compiled with `py_compile.compile(path, doraise=True)`. All files whose basename began with `check_` or `test_` ran separately as `python <basename>` from their own parent directory with assertions enabled and a 60-second timeout. The log retains exits, timings, and output for failed scripts; successful stdout/stderr were omitted. To replay, check out the executable revision, match the manifest using `git hash-object <path>`, compile each listed file, and run the listed scripts with the same working directories.

Environment: `3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]`; `Linux-6.18.57-x86_64-with-glibc2.39`. This candidate Linux runtime pass is scoped to that snapshot and discovery rule. It is separate from mathematical/editorial review, supported-platform testing and release or canonical approval. G2–G8 remain pending.
