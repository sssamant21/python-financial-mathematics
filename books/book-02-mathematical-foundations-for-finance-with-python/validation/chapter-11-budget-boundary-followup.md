# Chapter 11 — Budget and constraint boundary follow-up

**Date:** 2026-10-29 (America/New_York)
**Scope:** Section 11.7 portion of COV-59.
**Status:** Selected missing budget/threshold cases passed; implementation unchanged; independent review pending.

Weights (0.5,0.25), budget one, long-only enabled, absolute cap 0.6 and gross cap one isolate budget failure: net/long/gross are 0.75, short is zero, feasibility is false and the exact breach list is ["budget"].

Using the exact dyadic tolerance 2^-20, the checker tests budget deviations on both sides of one, inclusive boundaries and adjacent representable outside values. Zero tolerance rejects the next float above one. Absolute-name and gross caps are tested independently at their effective thresholds and immediately beyond. Long-only checks distinguish -tolerance from the adjacent more-negative value. Selected negative caps and out-of-range tolerances are rejected.

A temporary in-memory variant omitting the budget check was detected. No implementation or mutant was published. These cases characterize selected binary-float comparisons; broader signed/sector policies and financial suitability are not inferred.

Baseline tree: `61e4e27d1d05d7aa60e8b2ca0cdba853d1e67cd3`. All 21 Chapter 11 Python files were fetched at that revision; only the Section 11.7 checker was replaced locally. Python 3.12.14/Linux: 21/21 files compiled and 11/11 check scripts exited zero with assertions enabled, own-directory working directories and a 15-second per-script timeout.

Published [checker](../chapter-11/code/check_section_11_07.py): commit `1d3b903f27d62ff50a3472324b2d0f5ebf3a1014`; blob `d3fe80a954fd86a8f644873543e4f383b0001a27`. Implementation blob remains `24ba3cfa7d35d4bd78573f9df43b91a829f1b8a1`.

This addresses the selected previously missing Section 11.7 budget path. COV-59 remains partially open for broader tolerance-unit/scale, conceptual policy and independent review. This scoped checker change follows the full-book runtime record.

[Policy audit](chapter-11-policy-audit-followup.md) · [Chapter 11 map](coverage-chapter-11.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
