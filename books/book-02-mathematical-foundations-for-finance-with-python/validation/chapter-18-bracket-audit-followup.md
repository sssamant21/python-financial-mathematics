# Chapter 18 — Bracket trace and evaluation audit

**Date:** 2026-10-28 (America/New_York)
**Scope:** Section 18.8 portion of COV-79.
**Status:** Selected diagnostic gap corrected; scoped runtime passed; independent review pending.

The bracket_invariant flag previously tested only membership in a list of termination-status names. It now derives its value from cached final endpoint signs (or a collapsed zero-residual root), sign preservation for each recorded interval and nesting between trace intervals. Final endpoint residuals and trace endpoint residuals are retained. No new function evaluations are introduced by report construction. The bisection update and stopping rules are unchanged.

The checker independently evaluates deterministic functions at reported endpoints/midpoints, verifies every reported width and midpoint residual, reconstructs each half-interval choice, checks nested intervals and compares observed callback count with the report. The expected count is two endpoint calls plus one per trace row, with one extra call for stagnation. This tests actual observations rather than inferring calls from iteration metadata.

Seven selected paths cover the zero-coupon benchmark, both endpoint-root branches, an exact midpoint root, width convergence, reversed-sign budget exhaustion and adjacent-float stagnation. Valid sign brackets in failure statuses do not imply convergence, continuity, root uniqueness or financial suitability.

Baseline tree: `4b3d528d9d75cb0a563d3ba1e61abe4a4e05dff0`. All 21 Chapter 18 Python sources were fetched at that revision; the local snapshot replaced only Section 18.8 and its checker. Python 3.12.14/Linux: 21/21 files compiled with py_compile; 11/11 check scripts exited zero from their code directory with assertions enabled and a 15-second per-script timeout.

| File | Commit | Blob |
|---|---|---|
| [section_18_08.py](../chapter-18/code/section_18_08.py) | `8ad11db3cf051b1f4c3eb715f2c0fa294e34b864` | `bcf145910188052058ee7a2e4827f95e582598d9` |
| [check_section_18_08.py](../chapter-18/code/check_section_18_08.py) | `1c3b1b710ad8961ab56086a6fbbc55b714c1a5b8` | `006047a91af368433ebe7d8a57dc2c712fc20e24` |
| [18.08-stopping-rules-and-diagnostics.md](../chapter-18/18.08-stopping-rules-and-diagnostics.md) | `e7644afb2158fc08c516b02607ffc21db845aaef` | `9491448d6b6360c76321b7e6ccde716562b88c84` |

This scoped change follows the recorded full-book run. COV-79 remains partially open for other solver trace/call diagnostics, general numerical behavior and independent review.

[Chapter 18 map](coverage-chapter-18.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
