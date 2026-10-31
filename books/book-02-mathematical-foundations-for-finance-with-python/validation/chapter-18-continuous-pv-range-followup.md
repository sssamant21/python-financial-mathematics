# Book 02 — Continuous-stream PV range correction

**Date:** 2026-10-31  
**Baseline:** `06fb4298c23624b317cb936e5010de07d37af4f7`  
**Pinned executable source:** `5396db3f4b64acb358f08ccfd89b13427ae33268`  
**Disposition:** Selected COV-80 numerical correction; independent review pending.

Original probes exposed complete-value range failures in Section18.7's continuous_cashflow_pv: cashflow1 with smallest-positive discount rate and maturity1.5 returned2 instead of the reference-rounded1.5; rate/maturity1e-308 returned0 instead of approximately1e-308. A large cashflow/negative-rate case rejected a representable final value after numerator overflow. Zero cashflow and a small-cashflow/large-growth case raised inside expm1 despite finite results. [Raw evidence](chapter-18-continuous-pv-range-followup.json) retains all five probes and the failed first regression.

Inputs still validate before zero cashflow/maturity shortcuts. Zero-rate products and ordinary expm1 product/quotients are combined rationally before final rounding. For x=-rho*T with |x|<=2^-26,a four-term exprel(x) approximation avoids losing the exponent product:1+x/2+x^2/6+x^3/24. Its omitted factor term is bounded by exp(|x|)|x|^4/120,<5e-34 on the selected interval,before callback/library/final rounding.

When positive growth exceeds expm1 range,the helper evaluates the scaled value in the log domain. This is an approximate binary64 branch,not a globally correctly rounded exponential contract. The [runnable checker](../chapter-18/code/check_continuous_pv_range.py) allows relative error2e-12 there and an explicit smaller allowance/ulp floor on ordinary cases. Near range/rounding boundaries and arbitrary models still require review.

Eighteen selected complete PV references use2500-digit Decimal direct expressions; for the selected extreme decay case,the checker uses the C/r limit with an omitted exponential contribution far below float resolution. Five final-range rejections and five invalid-input/before-zero-shortcut cases pass. Nonzero-to-zero/final overflow raise ValueError; true zero input cases remain valid.

All32 Chapter18 sources compiled and22 scripts passed on Python3.12.14/Linux,assertions enabled,separate processes,timeout15 seconds. All32 source hashes match the pinned tree and remain unchanged after execution. This includes preceding quadrature range,order,financial-study and final-report checks. Corrected helper blob `e4a8f1e4f11b5525babe7b39ebfb9632a0afae94`.

[V-52 full runtime](runtime-refresh-2026-10-31.md) compiled493 files,passed282 scripts and verified494 required hashes before/after at the same pin. It includes both quadrature/PV corrections and two new checkers after V-51. Later manuscript/report/tracker writes are outside executable inputs.

These are constant continuously discounted cash-flow numerical contracts,not financial-data validation,smoothness proofs,independent reviewer sign-off,supported-platform acceptance or release/canonical approval. Thirty selected categories remain partially addressed; none closed by the register.

Next substantive item: COV-80 Section18.6 piecewise-linear and Section18.10 interpolate accepted-input/result range,including complete affine quotients and declared extrapolation behavior,with independent affine references. Preserve the previously recorded interpolation-curvature evidence.
