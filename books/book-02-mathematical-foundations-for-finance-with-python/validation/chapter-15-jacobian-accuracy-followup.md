# Chapter 15 — Production-float Jacobian accuracy follow-up

**Date:** 2026-10-30  
**Inspected revision:** `63b4d515c48c10dae70de9278579a2d7badcbeb6`  
**Disposition:** Selected COV-71 accuracy evidence added; implementation unchanged.

The [new checker](../chapter-15/code/check_jacobian_accuracy.py) invokes the actual centered_jacobian_column helper at (2,0.125,2), for principal/rate/time columns, both valuation outputs and steps 1/16,1/32,1/64: eighteen float-column/reference pairs.

Independent 90-digit Decimal references use the exponential centered quotient level*(exp(k*h)-exp(-k*h))/(2*h), where k is the signed held-fixed maturity/rate. Principal dependence is linear, giving level/principal. Float results must agree with these stencil references within relative tolerance 2e-12 and absolute tolerance 1e-14. Against independently computed exact derivatives, the four rate/time output ladders have successive error ratios between 3.99 and 4.01. Principal derivative errors stay below 1e-13.

At step 2^-50, all three columns' future-value relative errors exceed 1%, while their 1/64-step counterparts stay below 0.1%. These are cancellation observations, not expected accuracy guarantees or confirmed guard defects. A separate principal-center case at 1 with step 3*2^-53 confirms unequal represented offsets despite both being distinct; the existing helper accepts this and uses requested 2*h. The manuscript now makes that policy and its limits explicit.

All 23 Chapter 15 Python files compiled and all 13 scripts passed on Python 3.12.14/Linux, assertions enabled and 15-second script timeouts. All 22 existing sources matched pinned Git blobs exactly or after verifying removal of one local trailing newline. [Raw evidence](chapter-15-jacobian-accuracy-followup.json) retains source hashes and outputs. No production implementation was changed; this checker follows [V-36](runtime-refresh-2026-10-29-r5.md), not a new full-book pass.

## Remaining scope and next checkpoint

Only one interior input, selected steps and two fixed valuation functions are covered. General step selection, noise, arbitrary range/domain behavior, nonuniform formulas and independent review remain open. Twenty-five selected categories remain partially addressed; COV-71 is not closed.

Next executable item: COV-72 Section 15.8 zero iso-variance denominator and rate-sign-crossing/domain rejection paths, using its manuscript/implementation contract before adding checks. A full-book refresh should reconcile subsequent Chapter 14 integrations and Chapter 15 checker additions after this batch.
