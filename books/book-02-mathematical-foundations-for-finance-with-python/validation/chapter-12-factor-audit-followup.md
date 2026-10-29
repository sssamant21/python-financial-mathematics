# Chapter 12 — Factor-limit audit follow-up

**Date:** 2026-10-29 (America/New_York)
**Scope:** Section 12.9 selected COV-62 obligations.
**Status:** Selected report and rejection gaps addressed; scoped runtime passed; independent review pending.

The project now retains aligned factor_tolerances. Its solver and acceptance rules are unchanged.

A controlled test injects target-solve positions (1.75,1) for matrix ((2,1),(1,-1)) and target (5,1), retaining real inverse-column solves used for conditioning. Independently expected achieved exposure is (4.5,0.75), residual is (0.5,0.25), infinity norm is 0.5, condition number is three, gross/net positions are 2.75, and backward error is 0.5/(3*1.75+5)=2/41. Limits (0.25,0.25) produce RATE failure, CREDIT pass and factor_tolerance_exceeded.

A RATE limit of exactly 0.5 accepts the injected candidate; nextafter(0.5,0) rejects it. Ordinary exact-reference condition limit three accepts; nextafter(3,0) rejects for condition_guardrail_exceeded. The controlled candidate is not a claim about an actual solver failure.

Further assertions cover nonfinite coefficient rejection in ExposureSystem itself, boolean coefficients, wrong matrix units, rectangular matching rejection and selected invalid condition/pivot controls. Existing target/tolerance permutation checks remain.

Baseline tree: `ef9b06d8893c180b28a81de6dc07f0ba91fdf307`. All 21 Chapter 12 Python files were fetched at that revision; the local snapshot replaced only the project and checker. Python 3.12.14/Linux: 21/21 sources compiled and 11/11 check scripts exited zero, with assertions enabled, code-directory working directories and a 15-second per-script timeout.

| File | Commit | Blob |
|---|---|---|
| [section_12_09.py](../chapter-12/code/section_12_09.py) | `fcf7eb5d14123b8c16f811f74105bfd2147e2e7c` | `a769b575d8e58f41d6e874b8d82fbb1c6d011e7e` |
| [check_section_12_09.py](../chapter-12/code/check_section_12_09.py) | `bd1d6303443e620184aa072a27b5433378b15f3e` | `51167cf6618c67f7d1c4abbc0815199f167b662b` |
| [12.09-chapter-project-exposure-matching-linear-solver.md](../chapter-12/12.09-chapter-project-exposure-matching-linear-solver.md) | `a2f31eb28f3dd2176a21efeaf3c1e67bed25804d` | `d6e6872cfe1ca0736163a1a8a6b3c96fdb72ea59` |

COV-62 remains partially open for broader guardrail/range behavior, source/version metadata and independent review. Configured numeric limits are not approved policy or market-data provenance. This scoped change follows the recorded full-book runtime result.

[Chapter 12 map](coverage-chapter-12.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
