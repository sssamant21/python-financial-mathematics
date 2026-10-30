# Section 16.6 — Newton update range and scaling follow-up

**Date:** 2026-10-30  
**Category:** COV-75, partially addressed; independent review pending.  
**Original main:** `1199c3acf71e768c71982a4847627de479b413a3`  
**Corrected executable snapshot:** `a10a3efdbc8c69abb68089855216f70f070996da`

## Retained original results

[Machine evidence](chapter-16-newton-range-followup.json) preserves four original probes, the new checker's original exit-1 assertion failure, source hashes, corrected scoped manifest and all script outputs.

- With `x=0, g=h=2^-1000, damping=2^-100`, the original Newton step returned zero; the exact update is `-2^-100`, a representable nonzero float. The intermediate damped gradient had underflowed.
- With `x=2^1023, g=5*2^1021, h=1/2`, both Newton and supplied-curvature quasi-Newton rejected an overflowing intermediate quotient. The exact final result is `-3*2^1022`, a finite float.
- With `x=g=1, h=3`, the original two-rounding expression returned `0.6666666666666667`. The new once-rounded exact represented-input expression returns `float(Fraction(2,3))`. This last-bit difference is an explicit arithmetic-policy change; it is not a claim that every old rounded approximation constituted an independent defect.

## Correction and expectations

Source correction commit `2c79db239d84c6ff7976f3c9489cadc4128b6038`, blob `611a845585edcb513c0d9d8f189bce3675914c81`, combines `x-damping*g/curvature` as a Fraction expression of validated represented inputs and converts only the final expression to float. Final overflow becomes ValueError. Callback validation, positive curvature and damping restrictions remain. Quasi-Newton uses the same private combined-update helper with unit damping.

[Runnable checker](../chapter-16/code/check_newton_range.py) tests:
- Six signed finite-result range cases, derived as exact rational expressions.
- Twenty-eight update references from seven exact quadratic objective scales `2^-1000,...,2^1000`, three Newton damping values and unit-damped supplied-curvature quasi-Newton.
- Seven real one-iteration Newton solves at zero gradient tolerance.
- Two nondyadic single-rounding references, two absolute-stopping-scale examples, twenty-three invalid/range cases and two final-rounding limitations.

For `f_a(x)=a*(x-b)^2/2`, `b=1/4, x=3/2`, the independent update expectation is `x-alpha*(x-b)`, so `a` cancels algebraically. The chosen dyadic callbacks preserve this exactly across the selected scales. This does not assert scale invariance for arbitrary rounded derivative callbacks.

## Actual scoped and full reruns

**26/26 Chapter 16 sources compiled and 16/16 scripts passed**, Python 3.12.14/Linux, assertions enabled, 15-second timeout per script. Every unchanged source matched the original pinned chapter manifest; every corrected scoped blob matched the published executable tree.

[V-41 full refresh](runtime-refresh-2026-10-30-r5.md) at the same executable snapshot subsequently compiled **470 files**, passed **259 scripts**, and verified **471 required input hashes before and after**. This covers both recent Section 16.6 changes and their two new checkers. Counts were derived from the pinned tree.

From a checkout of `a10a3efdbc8c69abb68089855216f70f070996da`:
```bash
cd books/book-02-mathematical-foundations-for-finance-with-python/chapter-16/code
python check_newton_range.py
```
For the original failure, use a separate checkout of `1199c3acf71e768c71982a4847627de479b413a3`, copy only the new checker into its code directory and run it before changing the helpers. The initial damped-underflow assertion fails; raw evidence retains all original probe outputs.

## Scoped limits and next obligation

Finite final rounding can legitimately produce zero or leave an iterate unchanged. A tiny objective scale can satisfy the solver's unchanged absolute gradient tolerance at its initial point, while the normally scaled version takes a step. The checker records this distinction: update invariance is not stopping invariance. Exact combined arithmetic does not validate derivatives, objective decrease, local convergence assumptions, multidimensional Newton solves or BFGS/L-BFGS algorithms.

Twenty-eight selected COV categories remain partially addressed; none closed by the register. Independent review, supported environments, release acceptance and canonical approval remain open.

Next executable item: COV-74 Section 16.8 observation/weight/metric validation and extreme residual-metric range, beginning with independent exact/Decimal references and preservation of any original failures.
