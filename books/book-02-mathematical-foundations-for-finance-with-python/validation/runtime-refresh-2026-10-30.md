# Book 02 — Full runtime refresh, sixth recorded pass

**Date:** 2026-10-30  
**Pinned source:** `28af429b7695520536cf4a3384af1318614e31aa`  
**Finding:** V-37  
**Disposition:** Candidate Python/Linux runtime passed; independent review and release approval pending.

| Check | Outcome |
|---|---:|
| Python files compiled | 461 / 461 |
| Check/test scripts exited zero | 250 / 250 |
| Failed/timed-out scripts | 0 |
| Required source/fixture hashes matched before and after execution | 462 / 462 |
| Sum of script execution times | 8.821 seconds |

Environment: Python 3.12.14; Linux-6.18.57-x86_64-with-glibc2.39. Assertions enabled, no -O; all Python sources compiled using py_compile.compile(...,doraise=True). Each check_*.py/test_*.py script ran as [sys.executable, script.name], cwd=script.parent, with a 15-second timeout and captured text output.

A fresh snapshot was assembled only from bytes whose Git blob hashes matched the pinned recursive tree. One trailing newline was removed from a reused local copy only when that produced the expected hash. All 461 sources plus the Chapter 1 section-1.14 JSON fixture matched again after execution. Validation reports/tracking files are excluded from this denominator and were published after the tested source revision.

[Machine-readable evidence](runtime-refresh-2026-10-30.json) retains manifests, compiled paths, exact environment, script exits, timings and raw output.

## Reconciliation

Compared with [V-36](runtime-refresh-2026-10-29-r5.md), five checker additions cover Section 14.8 diagnostic integration, Section 14.10 final integration, Chapter 15 Hessian accuracy, Jacobian accuracy and level-set boundaries. Both Chapter 14 assessment implementation changes are included. Counts increase by five Python files and five scripts. Aggregate scripts repeat checks; counts do not measure independent coverage.

[Level-set boundary evidence](chapter-15-level-set-boundary-followup.md) records the latest selected COV-72 assertions. Twenty-six categories are partially addressed; none is closed. Earlier scoped-only records are historical and now covered by this run.

G1 candidate runtime evidence is refreshed. G2–G8 remain in progress/pending/not granted; named independent review, supported environment coverage and reviewed release approval are not established. Next executable investigation: Section 15.8 finite rate-shock addition and extreme intermediate range, using exact/high-precision level-preservation references.

[Progress](PROGRESS.md) · [Review checklist](remaining-review-checklist.md) · [Remediation register](gap-remediation-register.md).
