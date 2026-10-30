# Chapter 14 — Symmetry and averaging policy follow-up

**Date:** 2026-10-29  
**Inspected source revision:** `4055c7b0aef780f9043c07cbd03d4f7f31eca3a7`  
**Disposition:** Selected COV-68 boundary evidence added; implementation unchanged.

## Explicit contract and reference cases

[New checker](../chapter-14/code/check_symmetry_policy.py) tests nine asymmetric matrices with equal diagonals at scales 1, 2^20 and 2^-20. At each scale, the off-diagonal difference is the float threshold 1e-12*max(1,scale), its immediate predecessor or its immediate successor. Exact Fraction comparisons on these represented values independently establish six accepted and three rejected eigen/decomposition cases. Cholesky rejects all nine because its contract requires exact symmetry.

For accepted cases, exact rational averaging followed by float conversion supplies the expected symmetric off-diagonal. Results match the explicitly symmetrized matrix and its transpose; closed-form eigenvalues are checked. Section 14.2's reconstruction error is bounded below by the intentional asymmetry displacement delta/sqrt(2), allowing 0.1% rounding slack. Its diagnostic uses original input entries, not just the averaged matrix.

Three further zero-diagonal subnormal cases check exact rational midpoint rounding: equal smallest-subnormal off-diagonals, smallest-subnormal versus zero, and smallest versus twice-smallest. A midpoint that rounds to zero is a representation effect; no false claim of exact real-average retention is made.

The max(1,magnitude) floor creates an absolute allowance for small matrices. These tests document the existing policy and do not infer a purely relative test, economic unit compatibility or consistent acceptance across differently scoped helpers.

## Runtime evidence

All 27 Chapter 14 Python files compiled and all 17 scripts exited zero on Python 3.12.14/Linux, assertions enabled and a 15-second timeout per script. All 26 existing source files matched the pinned Git blobs exactly or after verifying removal of one trailing newline from a local copy. [Raw evidence](chapter-14-symmetry-policy-followup.json) retains those hashes and script outputs.

No implementation defect was confirmed in these selected symmetry/averaging cases, so numerical behavior was preserved. The manuscript now states the distinct symmetry policies and averaging limits. This scoped checker addition follows [V-35](runtime-refresh-2026-10-29-r4.md), not a new full-book pass.

## Remaining scope and next checkpoint

Large-value averaging overflow, trace/determinant/residual range, arbitrary asymmetry/cutoff transitions, unit-scaled policy choices and independent review remain open. Twenty-five selected categories remain partially addressed; COV-68 is not closed.

Next executable item: Section 14.5 Cholesky reconstruction norm at tiny nondyadic matrix scales, following the confirmed squared-norm underflow pattern in Section 14.2. Use a direct high-precision reference before changing that helper; refresh full-book runtime after the related diagnostic fixes.
