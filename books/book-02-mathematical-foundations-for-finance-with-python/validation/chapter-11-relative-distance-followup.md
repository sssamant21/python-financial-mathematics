# Chapter 11 — Relative-distance contract follow-up

**Date:** 2026-10-29 (America/New_York)
**Scope:** Section 11.4 relative-distance portion of COV-60.
**Status:** Selected contract checks passed; implementation unchanged; independent review pending.

For actual (1,2) and benchmark (4,6), differences have magnitudes (3,4). Independent relative-distance references are L1=7/10, L2=5/sqrt(52), Linfinity=4/6. Reversed inputs give 7/3,5/sqrt(5),2, directly discriminating the benchmark denominator.

The checker tests these values at common scales 1,2,-2,1e100,1e-100 with permuted labels. It asserts zero self-distance, distance one for zero actual versus nonzero benchmark, and rejection of zero benchmarks including zero/zero. A smallest-subnormal scalar reference remains nonzero and yields relative distance one for zero actual. An overflowing relative ratio is rejected. Unit/axis/label mismatches and unknown norms are checked.

The assessment's deviation dictionary is asserted directly and its relative L2 distance is checked against sqrt(3/107). A temporary in-memory implementation using the actual norm as denominator was detected. No implementation or mutant was published.

Baseline tree: `098e8583d49ea0525b6cbc7f000fd7f9bbe9dadd`. All 21 Chapter 11 Python files were fetched at that revision; only the Section 11.4 checker was replaced locally. Python 3.12.14/Linux: 21/21 files compiled and 11/11 check scripts exited zero with assertions enabled, own-directory working directories and a 15-second per-script timeout.

Published [checker](../chapter-11/code/check_section_11_04.py): commit `6c75836c76ed035890c3fced1e5aea170d9d5df5`; blob `6abd90cda25edd504fe70e9f07d40514749a26eb`. Implementation blob remains `ebd9f6e1c3ff4d691bd6e9bed5d5f8b581b23da0`.

COV-60 remains partially open for broader report/cumulative/range obligations and independent review. Selected scaled cases do not prove arbitrary-range scale invariance; finite representability and rounding remain constraints. This scoped checker change follows the latest full-book run.

[Projection audit](chapter-11-projection-audit-followup.md) · [Chapter 11 map](coverage-chapter-11.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
