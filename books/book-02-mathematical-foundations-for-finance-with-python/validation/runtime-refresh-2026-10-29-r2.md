# Book 02 — Full runtime refresh, second recorded pass

**Date:** 2026-10-29 (America/New_York)
**Pinned source:** `7ee99f60d5089510f860a0b6f695f971beb2eac6`
**Disposition:** Candidate Python/Linux runtime passed; independent review and release approval pending.

| Check | Outcome |
|---|---:|
| Python files compiled | 444 / 444 |
| Check/test scripts exited zero | 233 / 233 |
| Failed or timed-out scripts | 0 |
| Python sources plus required JSON fixture matched pinned Git tree | 445 / 445 |
| Script execution elapsed time | 6.458 seconds |

Environment: Python 3.12.14; Linux-6.18.55-x86_64-with-glibc2.39. Each script ran with assertions enabled, its parent as working directory and a 15-second timeout. Aggregate scripts repeat checks; counts do not measure independent coverage.

## Reproduction and retained evidence

The recursive Git tree was pinned before acquisition. Reused source files were copied only when their Git blob hashes matched the pinned tree. Changed files were fetched with that exact revision. All 444 Python files and the Chapter 1 section-1.14 JSON fixture were verified before execution and again afterward. Validation-tracking JSON and earlier runtime reports are excluded from this source/fixture count; this narrower denominator differs from the earlier 467-blob record.

Every Python file was compiled with py_compile.compile(...,doraise=True). Every filename starting check_ or test_ and ending .py was invoked as [sys.executable,absolute_path], with cwd=script.parent, timeout=15 and captured text output. No -O flag was used.

[Machine-readable evidence](runtime-refresh-2026-10-29-r2.json) retains the manifest/blob hashes, exact interpreter/platform, script paths, exit codes, timings and raw stdout/stderr. It was published after the tested revision and is not part of that tested snapshot.

## Included follow-ups

This run includes all prior code changes through the Chapter 12 factor audit, including subsequent Chapter 14 compression bounds, Chapter 16 per-candidate acceptance, Chapter 17 KKT/report-range/final-assessment checks, Chapter 18 bracket diagnostics, and Chapter 20 error-range/metamorphic-input contracts.

The [remediation register](gap-remediation-register.md) tracks fourteen selected partially addressed COV categories. This pass refreshes their execution evidence; it does not close their remaining mathematical, editorial, provenance or broader numerical obligations.

The [previous full refresh](runtime-refresh-2026-10-29.md) and [initial pinned run](pinned-revision-runtime-validation.md) remain historical records at their source revisions. This record is now the latest full candidate execution.

## Remaining gates

All 215 sections are substantively mapped, but documented gaps remain. Independent mathematical/editorial reviewers are unassigned; supported Python/platform coverage, complete visual/navigation review, reviewed release validation and canonical approval remain pending. A passing Linux candidate is not independent review, a general numerical proof or release acceptance.

[Progress tracker](PROGRESS.md) · [Review checklist](remaining-review-checklist.md) · [Coverage index](substantive-coverage-index.md).
