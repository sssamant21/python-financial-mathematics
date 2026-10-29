# Book 02 — Full runtime refresh, fourth recorded pass

**Date:** 2026-10-29  
**Pinned source:** `3e185649bf53f5a72ad9e1869d17762110444a26`  
**Finding:** V-35  
**Disposition:** Candidate Python/Linux runtime passed; independent review and release acceptance pending.

| Check | Outcome |
|---|---:|
| Python files compiled | 452 / 452 |
| Check/test scripts exited zero | 241 / 241 |
| Failed or timed-out scripts | 0 |
| Required source/fixture blobs verified before and after execution | 453 / 453 |
| Sum of script execution times | 12.685 seconds |

Environment: 3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]; Linux-6.18.55-x86_64-with-glibc2.39. Assertions enabled; no -O. Files were copied into a fresh snapshot only after their Git blob hashes matched the pinned recursive tree. Exactly one trailing newline was removed from a reused file only when that produced the expected blob hash. Every Python source was compiled using py_compile.compile(..., doraise=True). Each check_*.py or test_*.py script ran as [sys.executable, script.name], cwd=script.parent, with a 15-second timeout and captured stdout/stderr. All required hashes matched again after execution.

[Machine-readable evidence](runtime-refresh-2026-10-29-r4.json) retains the full source manifest, compiled paths, environment, exit codes, individual timings and raw output. Reports/tracking files are excluded from the 453-blob denominator; it comprises 452 Python sources and the Chapter 1 section-1.14 JSON fixture.

## Change reconciliation

Compared with [V-34](runtime-refresh-2026-10-29-r3.md), this run adds eight Chapter 13/14 checkers: QR rank screen, ridge optimality, project contract, basis span, null basis, near-repeated eigenpairs, near-SPD Cholesky and SVD factor ordering. Counts rise by eight sources and eight scripts; aggregate scripts still repeat checks, so these counts are not independent-coverage measures.

The tracker contained stale “latest” labels and associated V-33/second-refresh counts with the V-34 revision. The historical second-refresh source is `7ee99f60d5089510f860a0b6f695f971beb2eac6`; V-34 remains `f4cffe7ec0877454330b96ff07a15cdea1a5abbb`. Current summary pointers and those historical labels are reconciled alongside this report; earlier evidence files are preserved.

## Remaining work and checkpoint

Twenty-five selected COV categories remain partially addressed; none is closed by this run. G1 candidate runtime evidence is refreshed. G2–G8 retain their pending/in-progress/not-granted dispositions. No independent reviewer, supported-platform result or release approval is inferred.

Next executable investigation: COV-68, Section 14.1 highly unequal spectra and cancellation in the smaller eigenvalue. Use an exact determinant/high-precision reference and a minimal reproducer before changing behavior; keep general range and symmetry-policy obligations separate.

[Progress](PROGRESS.md) · [Review checklist](remaining-review-checklist.md) · [Remediation register](gap-remediation-register.md).
