# Chapter 15 — Adjusted-maturity numerical range correction

**Date:** 2026-10-30  
**Inspected revision:** `5681bdab2aa8de1caa4504f58b2d7a7c9624c0dd`  
**Correction commit:** `d8bb3b044d2b868e6f3f6ee01fc53d7707ae4b06`  
**Corrected blob:** `82f10620478a3ba33d5abb4957096d84643beb67`  
**Disposition:** Selected COV-72 numerical defects corrected; category partially open.

## Reproduced failures

The prior direct r*t/(r+dr) rejected (1e308,2,0) despite the exact answer 2, returned zero for (1e-300,1e-100,0) instead of 1e-100, and returned zero for (1e308,1,1e308) after the shocked rate overflowed. The [raw evidence](chapter-15-maturity-range-followup.json) retains probes and the original regression failure.

The implementation validates the rounded shocked rate as finite/nonzero, forms the numerator and quotient using exact Fraction arithmetic on represented inputs, then rounds the final maturity to float. Negative maturities and final overflow reject. A positive exact result that underflows to zero now explicitly rejects instead of claiming zero preserves the level. Zero original maturity remains accepted under the existing domain rules.

## Independent verification

[New checker](../chapter-15/code/check_maturity_range.py): eight 100-digit Decimal references cover positive/negative large rates, tiny numerator products, ordinary signed cases, smallest-subnormal rate and zero maturity. Exact equality to the float-rounded Decimal quotient is required. Exponent preservation is checked at relative 2e-16 without evaluating unrepresentable extreme exponentials.

Five rejections cover shocked-rate overflow, final quotient overflow, positive-result underflow to zero, zero shocked rate and negative maturity. The represented rounded r+dr denominator is intentional; this does not claim preservation relative to an unrounded real sum.

All 25 Chapter 15 Python files compiled and all 15 scripts passed on Python 3.12.14/Linux with assertions enabled and a 15-second timeout per script. Source/checker changes follow [V-37](runtime-refresh-2026-10-30.md); no new full-book run is claimed.

## Remaining scope and checkpoint

This fixes selected arithmetic range failures, not all level-set conditioning, floating-point exponent multiplication, exponential valuation range or applied/unit proofs. Exact rational work adds small overhead to this scalar teaching helper. Twenty-six categories remain partially addressed; independent review and release approval are pending.

Next executable item: COV-72 covariance symmetry/PD restrictions and gradient/Hessian consistency in Sections 15.4/15.6. Read those contracts together before broadening or changing accepted inputs.
