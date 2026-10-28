# Chapter 5 — Runtime evidence reconciliation

> **Current scoped status: PASS.** F13 was resolved in the [backend-resolution follow-up](backend-resolution/README.md). The original partial run and failure evidence below are retained as history. Chapter 5 now has 80 distinct passing reference test methods, including twelve installed methods.

**Date:** 2026-10-27. **Reviewer / execution owner:** Codex. **Source:** Book 1 baseline `f429fb81b8d8f7d228100333c76019d583200d64`. Chapter 5 manuscript files, including the companion, were unchanged through `37d212d01a3a6da7eb49058629a03a7b3c512b09`; GitHub comparison returned no changed Book 1 Chapter 5 paths. [results.json](results.json) records per-file SHA-256 values.

## Initial outcome (superseded by follow-up)

PARTIAL: 68 unittest methods passed across eight suites, with no skips; seven standalone demonstrations, three offline environment/dependency workflows, and thirteen extracted-directory compilation checks passed. The project and companion installed-package workflows are BLOCKED by the exact builder prerequisite. They are not counted as passing tests. No manuscript changes were made.

| Section | Executed reference tests | Other scoped result |
|---|---:|---|
| 5.1 | 8 | Demonstration and compilation passed |
| 5.2 | 9 | Demonstration and compilation passed |
| 5.3 | 9 | Compilation passed |
| 5.4 | 9 | Demonstration and compilation passed |
| 5.5 | 8 | Package-module demonstration and compilation passed |
| 5.6 | — | Offline pip install/failure/repair/cleanup workflow and compilation passed |
| 5.7 | — | Temporary environment isolation/recreation workflow and compilation passed |
| 5.8 | — | Pinned and hashed two-install workflow, altered-artifact rejection and compilation passed |
| 5.9 | 8 | Project-layout demonstration and compilation passed |
| 5.10 | 8 | Configuration demonstration and compilation passed |
| 5.11 | 9 | Research report demonstration and compilation passed |
| 5.12 | Not run | Backend prerequisite BLOCKED; extracted project compilation passed |
| 5.13 companion | Not run | Extended verifier prerequisite BLOCKED; extended project compilation passed |

The companion contains twenty worked answers and four extension test methods. Its documented installed suite has twelve methods in total (eight base plus four extensions), not twenty independent unit tests. Neither the base installed suite nor the extended suite was executed here.

## Environment and method

Python 3.12.14, Linux x86_64 with glibc 2.39. Host pip 26.2.2 and setuptools 84.1.0; the temporary pip environments in Sections 5.6 and 5.8 used ensurepip's pip 25.0.1. Existing application unit tests and demonstrations ran with `-W error::FutureWarning`. Environment workflow scripts ran as published, creating and cleaning their own temporary environments. They installed only local teaching wheel fixtures using offline pip options; no external package-index download was performed.

Use a fresh output directory from the repository root:

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-runtime/run_reference_checks.py books/book-01-python-foundations-for-financial-mathematics/chapter-05 /tmp/chapter05-repro
```

The [runner](run_reference_checks.py) reconstructs the documented multi-file modules, packages, fixtures and project. For Section 5.8 it supplies Section 5.6's documented helper. The companion is assembled in its own copy of the project using the instructed class insertion and success-message update. Runtime source listings and the exact backend guard are preserved. The research demonstration deliberately uses exclusive output creation, so reusing an output directory may fail rather than overwrite its report.

Detailed commands, statuses and source hashes are in [results.json](results.json); test output, workflow stages, demonstration output and prerequisite tracebacks are in [all-checks.log](all-checks.log). Compilation uses `python -m compileall -q .`. The runner exits 2 for a recorded prerequisite blocker and 1 for an unexpected process failure; an exit 2 is not a full chapter pass.

## F13 — Exact build prerequisite unavailable

**State:** BLOCKED. **Severity:** Medium validation blocker. **Owner:** QA executor. **Affected source revision:** unchanged baseline through the head above.

The published verifier requires setuptools 84.0.0 before it builds a regular wheel. The current builder has 84.1.0; no exact wheel was found in the local pip cache or searched workspace/runtime wheel paths. Both the original and companion verifier exited nonzero with:

```text
RuntimeError: Prepare builder with setuptools==84.0.0
```

This is an environment prerequisite failure, not evidence of a package defect. The build, fresh runtime installation, installed import-origin check, installed tests, module/console CLI parity, argument failure and project pip check remain unverified in this run. Earlier manuscript reports of those passes remain historical.

**Next action:** prepare a dedicated builder with the declared setuptools 84.0.0 artifact, rerun Section 5.12 and its extended companion, retain the actual test counts and wheel hashes, and update F13 and the chapter status. Do not remove or loosen the guard to turn this run into a pass.

## Remaining scope

These executions do not establish independent financial correctness of every worked answer, source authenticity, all numerical limits, cross-platform support, or release acceptance. Windows/macOS instructions, external package indexes, source-distribution rebuilds, publication and independent financial review remain pending. Resolve F13 before advancing the sequential runtime reconciliation to Chapter 4.
