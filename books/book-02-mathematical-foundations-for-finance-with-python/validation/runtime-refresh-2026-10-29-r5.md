# Book 02 — Full runtime refresh, fifth recorded pass

**Date:** 2026-10-29  
**Pinned source:** `82ec4d155b0b370008fab16f42a9781b7c4cd322`  
**Finding:** V-36  
**Disposition:** Candidate Python/Linux runtime passed; independent review and release acceptance pending.

| Check | Outcome |
|---|---:|
| Python files compiled | 456 / 456 |
| Check/test scripts exited zero | 245 / 245 |
| Failed/timed-out scripts | 0 |
| Required source/fixture blobs verified before and after execution | 457 / 457 |
| Sum of script execution times | 8.299 seconds |

Environment: Python 3.12.14; Linux-6.18.55-x86_64-with-glibc2.39. Assertions enabled, no -O; py_compile.compile(...,doraise=True). Each check_*.py/test_*.py ran as [sys.executable, script.name], cwd=script.parent, timeout=15, with captured text stdout/stderr.

A fresh snapshot was assembled by matching reusable local bytes against the pinned recursive Git tree, allowing removal of one trailing newline only when the resulting Git blob hash matched. All 456 Python sources and the Chapter 1 section-1.14 JSON fixture matched before and after execution. Reports/tracking files are excluded from this denominator and were published after the tested source revision.

[Machine-readable evidence](runtime-refresh-2026-10-29-r5.json) retains the manifest, compiled paths, exact interpreter/platform, per-script exit codes, timings and raw outputs.

## Included changes

Compared with [V-35](runtime-refresh-2026-10-29-r4.md), this run adds four checkers: unequal spectra, spectral report range/iterators, symmetry policy and tiny Cholesky norms. It includes the Section 14.1 small-eigenvalue correction, Section 14.2 one-shot-input/tiny-norm corrections and Section 14.5 tiny-norm correction. Source counts rise by four and script counts by four. Aggregate suites repeat checks; these counts do not measure independent coverage.

[Cholesky failure/fix evidence](chapter-14-cholesky-norm-followup.md) records the latest correction. Earlier scoped-only wording remains historical; this full run covers all four subsequent changes.

## Gates and next checkpoint

G1 candidate runtime evidence is refreshed; G2–G8 remain in progress/pending/not granted. Twenty-five selected COV categories remain partially addressed. No independent reviewer, platform support, general stability proof or release approval is claimed.

Next executable item: COV-67, distinguish Section 14.8/14.10 literal reference reports from computed-factor integration and add meaningful fault-detection evidence or narrow their stated contract. Broader Chapter 14 range and independent-review obligations remain open.

[Progress](PROGRESS.md) · [Review checklist](remaining-review-checklist.md) · [Coverage index](substantive-coverage-index.md).
