# Book 02 — Full runtime refresh, eighth recorded pass

**Date:** 2026-10-30  
**Pinned source:** `18be350b40cc2a0a963e0c5fd91b793cf0c3c634`  
**Finding:** V-39  
**Disposition:** Candidate Python/Linux runtime passed; independent review and release acceptance pending.

| Check | Outcome |
|---|---:|
| Python files compiled | 467 / 467 |
| Check/test scripts exited zero | 256 / 256 |
| Failed/timed-out scripts | 0 |
| Required source/fixture hashes matched before and after execution | 468 / 468 |
| Sum of script execution times | 9.601 seconds |

Environment: Python 3.12.14; Linux-6.18.57-x86_64-with-glibc2.39. Assertions enabled, no -O. Every Python source compiled using py_compile.compile(...,doraise=True). Each check_*.py/test_*.py script ran as [sys.executable, script.name], cwd=script.parent, timeout=15, with captured text stdout/stderr.

The fresh snapshot reused bytes only when their Git blob hashes matched the pinned tree, allowing one trailing-newline removal only when it produced the expected hash. All 467 Python sources plus the Chapter 1 section-1.14 JSON fixture matched again after execution. Validation reports/tracking files are excluded from this denominator and were published after the tested source revision.

[Machine-readable evidence](runtime-refresh-2026-10-30-r3.json) retains manifests, compiled paths, environment, per-script exits, timings and raw output. Aggregate suites repeat checks; script counts do not measure independent coverage.

Compared with [V-38](runtime-refresh-2026-10-30-r2.md), this refresh includes three Chapter 16 checker additions: exact Armijo/status contracts, independent multistart roots/failure pools, and scaling/curvature/stable-step references. No production implementation changed in those three follow-ups. [Latest scoped evidence](chapter-16-scaling-reference-followup.md).

Twenty-eight selected COV categories remain partially addressed. G1 candidate execution is refreshed; G2–G8 retain in-progress/pending/not-granted states. No independent reviewer, general numerical proof, supported-platform result or release acceptance is claimed.

Next executable item: COV-75 Sections 16.2–16.4 derivative representability and denominator extremes, using exact-polynomial references before any correction.

[Progress](PROGRESS.md) · [Review checklist](remaining-review-checklist.md) · [Remediation register](gap-remediation-register.md).
