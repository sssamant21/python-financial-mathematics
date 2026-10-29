# Book 02 — Full runtime refresh after gap remediation

**Date:** 2026-10-29
**Pinned source:** `37aac57a72303a6d4178790f8d172495e2bc0ada`
**Disposition:** Candidate Python/Linux runtime pass; independent review and release approval pending.

## Outcome

| Check | Result |
|---|---:|
| Python source files compiled | 444 / 444 |
| Check/test scripts exited zero | 233 / 233 |
| Failed or timed-out scripts | 0 |
| Downloaded Python/JSON blobs matching pinned Git tree, before and after run | 467 / 467 |
| Script execution elapsed time | 6.745 seconds |

Environment: Python 3.12.14, Linux-6.18.55-x86_64-with-glibc2.39. Checks ran with assertions enabled, their own parent directories as working directories, and a 15-second timeout per script. Aggregate scripts repeat underlying checks; 233 exits are not 233 independent coverage obligations.

## Snapshot and commands

The recursive Git tree was pinned before acquisition. Previously downloaded files were reused only when their Git blob hashes matched that tree; changed/missing files were fetched at the pinned revision. Exact-byte hashes were verified after acquisition and again after execution. The snapshot contains 444 Python sources and 23 JSON records, including tracking metadata; these are not 23 runtime fixtures.

Every .py source under Book 02 was compiled using py_compile.compile(..., doraise=True). Every filename beginning check_ or test_ and ending .py was invoked as [sys.executable, absolute_script_path] through subprocess.run(cwd=script.parent, timeout=15, capture_output=True, text=True). No -O flag was used.

[Machine-readable evidence](runtime-refresh-2026-10-29.json) retains revision, environment, manifest paths/blob hashes, per-script exit codes/timing and SHA-256 fingerprints of captured stdout/NUL/stderr. Fingerprints identify captured output but do not substitute for the raw text, which is not included in that compact record. The record itself was published after the tested revision and is not part of its source manifest.

## Changes included since the earlier full run

This refresh includes the subsequent Section 12.5 rank-scaling fix; Chapter 14 covariance eigenpairs; Section 15.2 finite-difference guards; Section 15.9 path-series oracle and portfolio errors; Chapter 19 report-input/event cases and adaptive policy checks; and Chapter 21 integrated diagnostics/JSON/error propagation.

Focused records retain detailed contracts, reference derivations, mutation experiments and remaining gaps:
- [Rank target scaling](chapter-12-rank-target-scaling-followup.md)
- [Covariance eigenpairs](chapter-14-covariance-eigenpair-followup.md)
- [Scalar finite differences](chapter-15-scalar-difference-followup.md)
- [Taylor oracle](chapter-15-taylor-oracle-followup.md)
- [Account provenance](chapter-19-input-provenance-followup.md)
- [Adaptive policy](chapter-19-adaptive-policy-followup.md)
- [Integrated diagnostics](chapter-21-integrated-diagnostics-followup.md)

The [earlier pinned run](pinned-revision-runtime-validation.md) remains historical evidence at its own revision; this refresh supersedes it as the latest full candidate execution.

## Limits and next work

This run verifies the selected Python files and their existing assertions on one environment. It does not establish all exercise/proof coverage, general numerical validity, supported Windows/Python-version behavior, visual/navigation quality, independent mathematical/editorial review or canonical approval. All 215 sections are mapped, but COV-01–COV-90 still require scoped dispositions.

Next work: consolidate these partial remediations into a gap-disposition register, continue outstanding numerical/report/manual-review items, and retain release gates until their specific evidence is supplied.
