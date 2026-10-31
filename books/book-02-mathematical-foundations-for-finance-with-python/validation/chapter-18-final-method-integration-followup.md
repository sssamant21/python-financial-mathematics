# Book 02 — Final solver/curve method integration

**Date:** 2026-10-30  
**Baseline:** `bb4c8d98ab92cb9d22cb9811bf977906d86e1521`  
**Pinned executable source:** `54c73a8f98043676edad54efc5725e80f4af883c`  
**Disposition:** Selected COV-81 final-report integration; independent review pending.

The Section18.10 final report omitted Applied A's actual safeguarded-Newton comparison and Applied C's log-discount convention. The first new checker failed on missing solver_comparison; [machine evidence](chapter-18-final-method-integration-followup.json) preserves that baseline and subsequent passing reruns. This was an applied-report gap, not a demonstrated incorrect original bisection answer.

The final report now calls Section18.9's solve on its zero-coupon objective/derivative and Section18.6's financial_comparison. Bisection and safeguarded Newton use the same[0,0.2] bracket and absolute width threshold1e-12; Newton relative tolerance is zero. Iterations, widths, residuals and callback counts remain visible. Bisection's single post-solve residual verification is counted separately.

| Recorded method | Iterations | Solver objective calls | Derivative calls |
|---|---:|---:|---:|
| Bisection | 38 | 41 | 0 |
| Safeguarded Newton | 40 | 83 | 40 |

This conservative safeguard/callback implementation is not faster by these counts; neither iteration counts nor callback counts establish wall-clock performance. Bisection additionally performs one reported residual verification. Widths are approximately7.276e-13 and6.198e-13, respectively.

The interpolation record includes rate interpolation followed by discounting, direct discount-factor interpolation and log-discount interpolation, with actual helper outputs and preserved legacy fields. No claim is made that the fixed illustrative curve is the appropriate market model.

The [runnable checker](../chapter-18/code/check_final_method_integration.py) uses100-digit Decimal direct price, analytic yield and interpolation-convention references. Selected price-evaluation rounding allowances remain separate from a certified mathematical enclosure. It observes the two actual method/curve helper calls and independently counts bisection, Newton objective and Newton derivative callbacks. Five injected wrong outputs (root,residual,midpoint rate,rate-derived discount,log discount) are detected. Repeated strict JSON serialization/round-trip is deterministic for the selected recorded case.

All28 Chapter18 Python sources compiled and18 check/test scripts passed on Python3.12.14/Linux, assertions enabled, separate processes, timeout15 seconds. All28 source hashes match the pinned tree and remained unchanged after execution. Final source blob `1e0054274cad05a54a6a7e3e0e248396da8a9298`; checker blob `7bcfb68c74f63bd2b75e56017a416c39f9c1cb06`.

[V-50 full runtime](runtime-refresh-2026-10-30-r14.md) compiled489 files,passed278 scripts and verified490 required input hashes before/after at the same pin, including the preceding project-error checker. Later manuscript/report/tracker writes are outside executable inputs.

COV-81 remains partially open: final three-step sensitivity/trapezoid studies, multiple-IRR input/range integration and general applied/error/model obligations remain. Thirty selected gap categories are partially addressed; none closed by the register. Independent mathematics/editorial review,supported environments,final reviewed-release validation and canonical approval remain pending.

Next substantive item: COV-81 Section18.10 actual Section18.7 three-step first/second sensitivity and trapezoid/Simpson PV report integration. Reuse and extend the retained mathematical oracles; do not treat the supplemental checker's study as an already integrated final-report field.
