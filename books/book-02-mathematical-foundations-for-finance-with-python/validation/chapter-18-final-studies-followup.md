# Book 02 — Final sensitivity/quadrature report integration

**Date:** 2026-10-30  
**Baseline:** `0057d198dfb5c70affb1380df3564d583bd03d33`  
**Pinned executable source:** `015137295af393e4f1783474fc1d24a7cb1c1c7b`  
**Disposition:** Selected COV-81 report integration; independent review pending.

Section18.10's final report lacked Applied D's actual three-step first/second sensitivity study and Applied E's trapezoid comparison. The corrected new checker failed on missing sensitivity_study before source changes. A prior checker import error (ExitStack imported from the wrong standard-library module) is retained separately; it was a harness defect, not a numerical source defect. [Raw evidence](chapter-18-final-studies-followup.json) preserves both and all subsequent reruns.

The final report now calls Section18.7's actual price, forward/central/second difference, trapezoid, Simpson and stable analytic PV helpers. Three steps(2e-4,1e-4,5e-5) retain derivatives, duration, convexity and discrepancies against the reported rounded analytic reference. No optimal step is selected. The continuous stream uses20,40,80 panels, retains both methods, signed errors, refinement ratios and units/conventions. Legacy duration and40-panel Simpson fields map to the integrated rows.

The [runnable checker](../chapter-18/code/check_final_studies.py) uses100-digit Decimal direct-price stencils/derivatives and an independent geometric-series trapezoid expression; Simpson references are derived from the composite-rule identity(4T_n-T_(n/2))/3. Selected rounding allowances are explicit, not universal certified math-library bounds. It observes22 price calls, three calls to each difference and quadrature helper, and one analytic-PV call. Seven wrong helper outputs are detected. Repeated strict JSON serialization/round-trip passes.

All29 Chapter18 sources compiled and19 scripts passed on Python3.12.14/Linux, assertions enabled, separate processes, timeout15 seconds. All29 source hashes match the pinned tree and remain unchanged after execution. This supplies actual final-report fields rather than merely rerunning the earlier supplemental study.

This source/checker batch follows [V-50](runtime-refresh-2026-10-30-r14.md), whose earlier full run compiled489 files/passed278 scripts/verified490 hashes. Current pinned inventory is490 Python files/279 check-test scripts, not a new full execution. COV-81 remains partially open, with30 selected categories partially addressed and none closed by the register. Supported-platform validation, independent mathematics/editorial review and release/canonical acceptance remain pending.

Next substantive item: COV-81 Section18.10 multiple-IRR valuation/input/range contract and actual root rejection. Reconcile its copied NPV arithmetic with Section18.5's corrected finite-period evaluator while preserving the final valuation API's single-cash-flow/all-zero cases and the stricter IRR-discovery contract.
