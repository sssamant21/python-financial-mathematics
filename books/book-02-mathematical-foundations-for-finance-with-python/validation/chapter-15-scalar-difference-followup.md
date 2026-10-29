# Chapter 15 — Scalar finite-difference follow-up

**Date:** 2026-10-28
**Scope:** Section 15.2 portion of COV-71 / V-16.
**Status:** Fix and scoped runtime pass complete; independent review pending.

## Confirmed behavior and correction

The centered-rate helper previously checked only positive finite step size. At rate 0.05 with step 1e-30, both perturbed rates round back to the base rate, producing a misleading zero derivative. With the linear callback f(a,r,t)=r, base rate zero and step 1e308, the denominator 2h overflows; the result is invalid instead of the exact derivative one.

The helper now validates the base rate, finite distinct perturbations and representable denominator before evaluation, then validates the returned difference. Unrepresentable or nonfinite perturbations raise ValueError; denominator overflow raises OverflowError. Valid finite differences retain their interface. This does not guarantee numerical accuracy for every accepted step.

## Regression and runtime evidence

Baseline tree: `ea555618814bccae45297a59418ca39b5c1294b9`. All 21 Chapter 15 Python files were fetched at that revision; the local snapshot replaced only the two files below.

| Published file | Commit | Resulting blob |
|---|---|---|
| [Scalar helper](../chapter-15/code/section_15_02.py) | `e05d82901d7f31351528361f4e37a051ee3a422b` | `45105b3374d8a55dfaccdb9695d2f672256cb8d1` |
| [Boundary checks](../chapter-15/code/check_finite_difference_boundaries.py) | `8f78a5a89e9531bd4ae41d150d9c6ac81330f749` | `3a9e82148a9b5ae7126cac290315208d9b6693de` |

Python 3.12.14/Linux: 21/21 files compiled with py_compile; 11/11 check scripts exited zero. Each script ran from chapter-15/code with a 15-second timeout and assertions enabled. The boundary suite passed nine unittest methods, five newly covering the scalar helper: lost perturbation, denominator overflow, perturbed-rate overflow, exact linear derivative three, and analytical FV/PV rate derivatives. These are scoped follow-up results, not a new full-book run.

## Remaining scope

COV-71 is partially remediated. Perturbation asymmetry, step selection, convergence/roundoff behavior and selected Hessian numerical benchmarks remain open. COV-70 project error reporting and independently expected nonzero full-Hessian contractions are unchanged. No independent reviewer or canonical approval is implied.

See the [original Chapter 15 map](coverage-chapter-15.md), [remediation queue](substantive-coverage-index.md) and [progress tracker](PROGRESS.md).
