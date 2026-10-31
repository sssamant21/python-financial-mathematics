# Book 02 — Complete affine interpolation range correction

**Date:** 2026-10-31  
**Baseline:** `23d2410e01c20d73093b1ab7ee4d4e74a4a852dd`  
**Pinned executable source:** `0c6adb3eee831bb109290c5c9e093a05cbdce19a`  
**Disposition:** Selected COV-80 numerical correction; independent review pending.

Original finite-input probes returned-1 instead of0 across a large knot span,NaN in the final helper,infinity across large opposite ordinates,and a false zero after premature ratio underflow. A fifth original probe was a preserved control. [Machine evidence](chapter-18-linear-range-followup.json) retains all five outputs and the failed first regression.

Section18.6 now computes one complete represented-input affine expression before final float rounding. Section18.10 delegates to that shared linear_segment. Nonzero-to-zero underflow and final overflow raise ValueError; exact cancellation remains valid. Intermediate knot/ordinate differences,ratios and products no longer decide whether a representable final value can be returned.

Extrapolation policies are preserved: piecewise_linear rejects out-of-range queries by default and uses an endpoint segment when explicitly enabled; the final interpolate entry point retains its existing mathematical affine extrapolation behavior. The shared linear_segment computes the line for any finite query and does not itself grant financial extrapolation approval.

The [runnable checker](../chapter-18/code/check_linear_range.py) uses2500-digit Decimal barycentric affine references for12 sets at both entry points,plus five multisegment references,two explicit extrapolation cases,four final-range rejections and four invalid final inputs. One shared call is observed and an injected false-zero output is detected. Smallest-subnormal knot/value recovery and large-span cancellation are included.

All33 Chapter18 sources compiled and23 scripts passed on Python3.12.14/Linux,assertions enabled,separate processes,timeout15 seconds. All33 source hashes match the pinned tree and remain unchanged after execution. Existing curvature-bound,curve-convention and final financial-study references pass.

This source/checker batch follows [V-52](runtime-refresh-2026-10-31.md),the earlier493-file/282-script/494-input full pass. Current pinned inventory is494 Python files/283 scripts,not a new full execution. Thirty gap categories remain partially addressed; none closed by the register.

Exact evaluation of the represented affine model does not establish data quality,good conditioning or a suitable financial curve/extrapolation convention. Independent mathematics/editorial review,supported platforms and release/canonical approval remain pending.

Next substantive item: COV-80 Section18.6 Lagrange polynomial normalization,product/sum range and knot recovery,with independently known polynomial references rather than repeated ordinary examples.
