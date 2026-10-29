# Chapter 13 — Fixed-model ridge optimality follow-up

**Date:** 2026-10-29  
**Implementation blob tested:** `e192df2252745fdaa32b8674234ca6edd4344549`  
**Disposition:** COV-65 partially addressed; independent review pending.

## Selected exact references

The new [checker](../chapter-13/code/check_ridge_optimality.py) independently constructs the objective for two identical columns (1,2), target (3,6), and positive ridge strength. Fraction arithmetic solves the two-by-two normal equations by determinants rather than calling the helper's closed form.

At strengths 1/2, 2, 20 and 2^-20, checks compare both positions, signed residuals and separate data/penalty/total objectives against these exact references. Three nonoptimal perturbations per strength have strictly greater objectives. Their exact excess is 5/2*(dx+dy)^2 + lambda/2*(dx^2+dy^2), including a null-space displacement (1,-1) whose data loss is unchanged but penalty rises.

Six positive strengths 1, 2^-4, 2^-8, 2^-12, 2^-16 and 2^-20 give decreasing position errors relative to the minimum-norm exact hedge (1.5,1.5). Errors match 1.5*lambda/(10+lambda). Zero strength remains rejected by the existing public contract.

## Runtime evidence

All 23 Chapter 13 Python files compiled; all 13 check scripts exited zero on Python 3.12.14/Linux with assertions enabled and a 15-second per-script timeout. The implementation blob above was verified locally against GitHub. Implementation unchanged. This scoped run includes the preceding QR checker and follows the [third full-book run](runtime-refresh-2026-10-29-r3.md), which includes neither new Chapter 13 checker.

## Remaining scope

These are fixed-model exact calculations and selected finite-sequence observations. They do not add a general ridge solver, support lambda=0, establish arbitrary-matrix conditioning/range behavior or complete weighted/unit/target-scale and broader optimality obligations. COV-65 remains partially open; independent mathematical/editorial review and release approval remain pending.
