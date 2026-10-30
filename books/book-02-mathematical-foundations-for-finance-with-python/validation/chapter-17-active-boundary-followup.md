# Section 17.4 — Adjacent active-set boundaries and cap duals

**Date:** 2026-10-30  
**Category:** COV-76, partially addressed; independent review pending.  
**Original main:** `09e9d92f60041c64d51d58c8118651ae45c3bc9b`  
**Corrected executable snapshot:** `bf81791b09530e2711c89ca4960d62bd571bb9b9`

## Retained original results

[Machine evidence](chapter-17-active-boundary-followup.json) retains three adjacent-transition probes, the original checker failure, original source hashes and all eleven final script outputs. The first baseline assertion failed on an absent exact-geometry field; the numerical probes separately establish the multiplier discrepancy.

At the represented cap immediately below `float(8/11)`, the original subtraction of nearly equal rounded gradient components gave cap multiplier `2.7755575615628914e-17`. The independent rational decimal-model formula gives `1.9984014443252817e-17`, about39% smaller relative to the true tiny value. The absolute error is small enough to pass the ordinary KKT tolerance, which does not make it a reliable shadow-price computation near this transition.

The rounded transition itself lies **above** exact8/11 by `1/49539595901075456`. Its legacy display label was weakly active, and its returned rounded weights gave a zero cap residual. This label/residual combination must not be confused with exact rational-model cap geometry.

## Correction and distinct report contracts

Correction commit `29a9066f87ae6905c97c1f8a0b671b1dbe0d6f0b`, blob `3f581603f381837951e52c959bf74249ded948a9`, forms the exact represented cap `u`, rational optimizer `x=min(u,8/11)` and:
- `lambda=(8*x-9)/50`.
- `mu=max(0,(8-11*x)/50)`.
- Model cap slack `u-x`.

Duals are rounded only after the complete rational calculation. Returned weights remain rounded floats; the existing variance and KKT residual calculations remain floating-point diagnostics.

For compatibility with the existing teaching display and numbered checks, `regime` still recognizes the rounded transition. Its basis is explicitly labelled `rounded_transition_display`. New `exact_model_regime`, `model_cap_active` and `model_cap_slack` describe the rational decimal model for the actual represented cap. In particular, the nearest float to8/11 is a display transition while its exact model cap is inactive with positive slack. Exact8/11 cannot be supplied by the helper's int/float API.

The KKT report's `active` list remains tolerance-based on its raw returned-weight residuals. Even tolerance zero cannot undo rounding in the weights themselves; it is not an exact symbolic activity test.

## Independent expectations and actual execution

[Runnable checker](../chapter-17/code/check_active_boundaries.py) checks **nine cap sets**: zero, the smallest positive float, two predecessor caps, the rounded transition, two successors, the predecessor of one and one.

Sixty-three weight/dual/value/geometry assertions use independently derived Fraction expectations. The value oracle is the expanded polynomial
`11*x*x/100-4*x/25+9/100`, allowing four output ulps for the unchanged floating variance calculation. Duals and rounded weights require exact float-reference agreement. Twenty-seven raw-activity reports cover tolerances0,1e-18,1e-9. Three explicit distinctions show exact model slack, rounded zero residual and tolerance-expanded activity.

**21/21 Chapter17 Python files compiled; 11/11 check scripts exited zero**, Python3.12.14/Linux, assertions enabled, cwd each script's parent, timeout15 seconds. This includes the existing Chapter17 tiny-empty-interval rejection regressions. Unchanged sources matched their original pinned blobs; all final scoped hashes matched the published executable tree.

From a checkout of `bf81791b09530e2711c89ca4960d62bd571bb9b9`:
```bash
cd books/book-02-mathematical-foundations-for-finance-with-python/chapter-17/code
python check_active_boundaries.py
```
For the baseline, copy only this checker into a separate checkout of the original revision above and run before changing the helper. It fails on missing exact-geometry evidence; raw probes retain the original near-transition multiplier and nominal activity results.

Fresh tree inventory: **479 Python files /268 check-test scripts**, not a new full-book execution count. [V-45](runtime-refresh-2026-10-30-r9.md) remains the latest full run at its earlier pin (478 compiled /267 scripts /479 required hashes). This subsequent one-helper/one-checker batch has scoped evidence above; refresh after related executable changes accumulate.

## Limits and checkpoint

This is the fixed two-asset decimal covariance model, not arbitrary covariance ingestion, a general QP solver or independent reviewer acceptance. The display policy, exact mathematical geometry and numerical certificate remain deliberately distinct. Broader tolerance units/scales, multiplier degeneracy and conditioning remain open. Twenty-eight categories remain partially addressed; none closed by the register. Supported platforms, reviewed release and canonical approval remain pending.

Next executable item: COV-76 Section17.4 degenerate cap-zero nonunique lower-bound/cap multiplier families, with exact stationarity/complementarity references and isolated sign failures.
