# Book 02 — Full runtime refresh, seventh recorded pass

**Date:** 2026-10-30  
**Pinned source:** `378775bc25034f5551f1d1efa51d836da77d6737`  
**Finding:** V-38  
**Disposition:** Candidate Python/Linux runtime passed; independent review and release acceptance pending.

| Check | Outcome |
|---|---:|
| Python files compiled | 464 / 464 |
| Check/test scripts exited zero | 253 / 253 |
| Failed/timed-out scripts | 0 |
| Required source/fixture hashes matched before and after execution | 465 / 465 |
| Sum of script execution times | 8.353 seconds |

Environment: Python 3.12.14; Linux-6.18.57-x86_64-with-glibc2.39. Assertions enabled, no -O; py_compile.compile(...,doraise=True). Each check_*.py/test_*.py ran as [sys.executable, script.name], cwd=script.parent, timeout=15 with captured text output.

The fresh snapshot reused bytes only after matching pinned Git blob hashes. Removal of one trailing newline was allowed only when it produced the expected hash. All 464 Python sources and the Chapter 1 section-1.14 JSON fixture matched before and after execution. Reports/tracking files are excluded from the 465-blob denominator and published after the tested revision.

[Raw machine evidence](runtime-refresh-2026-10-30-r2.json) retains the manifest, compiled paths, exact interpreter/platform, individual timings, exits and stdout/stderr. Aggregate scripts repeat checks; counts are not independent coverage measures.

## Included changes and remaining gates

Compared with [V-37](runtime-refresh-2026-10-30.md), this run includes three new checkers for adjusted-maturity range, covariance consistency and restricted determinant screening. It also includes the Section 15.8 maturity correction and Sections 15.4/15.6 shared covariance normalization/finite determinant screening. Earlier scoped-only records are historical.

[Determinant-screen evidence](chapter-15-covariance-screen-followup.md) explicitly records exact-PD inputs outside the restricted numerical acceptance contract. No general PD classifier or stability proof is claimed. Twenty-six COV categories remain partially addressed.

G1 candidate execution is refreshed. G2–G8 remain in progress/pending/not granted; independent reviewers, supported-environment results and reviewed release approval remain open. Next executable work: Chapter 16 COV-73/75 optimizer status/scaling obligations, guided by its coverage map.

[Progress](PROGRESS.md) · [Review checklist](remaining-review-checklist.md) · [Remediation register](gap-remediation-register.md).
