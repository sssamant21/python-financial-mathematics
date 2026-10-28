# Book 02 — Pinned Revision Runtime Validation

**Date:** 2026-10-28  
**Tested revision:** `2366ddd9ea146f841ad2822ffa5193bd637e4e9d`  
**Status:** Python compilation and script execution passed on Linux; independent review and final release approval remain pending.

## Snapshot integrity

A recursive Git tree pinned all Book 02 paths. The runtime snapshot included every Python source file and the Section 1.14 data fixture from that revision: 444 Python files and one JSON fixture. Each local file was checked against the tree's Git blob SHA-1 (hashing the Git blob header plus exact bytes). All 445 matched. The run did not mix source revisions or rely on earlier passing results.

## Environment and method

- Python 3.12.14, Clang 22.1.3.
- Linux 6.18.55, x86_64, glibc 2.39.
- Compilation: every `*.py` under Book 02, using `py_compile.compile(path, doraise=True)`.
- Script selection: every Python file whose basename starts with `check` or `test`.
- Each selected script ran as `[sys.executable, script.name]` with its containing directory as the working directory, captured stdout/stderr and a 15-second timeout.
- Interpreter optimization was not enabled; assertion-based checks were active.
- Script execution elapsed time: 13.826 seconds, excluding preparation and compilation.

## Results

| Measure | Result |
|---|---:|
| Python files compiled | 444/444 |
| Compilation failures | 0 |
| Check/test scripts exited zero | 233/233 |
| Failed or timed-out scripts | 0 |

The recent Chapter 1–4 regression additions and earlier focused numerical fixes are included in this one snapshot. The 233 script count includes aggregate scripts that rerun numbered checks; it is not a count of independent suites, assertions, exercise coverage or mathematical guarantees.

## Limits and next work

This result replaces the older mixed-snapshot runtime baseline for this defined revision. It is a candidate revision runtime pass, not a declaration that the book has reached its final approved revision. Later changes affecting code, fixtures or requirements require appropriate reruns.

Independent mathematical review, derivation/exercise coverage, editorial/source review, unresolved link/title issues and Windows/supported-Python testing remain open. No canonical approval is granted by this report.

Next, reconcile the remaining validation findings and prepare a documented review checklist against the same candidate revision. Final-revision validation must be repeated as needed after review changes.
