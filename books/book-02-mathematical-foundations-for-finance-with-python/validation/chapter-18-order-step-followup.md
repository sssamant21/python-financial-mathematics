# Book 02 — Section 18.7 quadrature-order and step-study follow-up

**Date:** 2026-10-30  
**Baseline:** `5cfc1d5cf01d2e038c38210362394860a98f1319`  
**Pinned executable source:** `497e1892a8bc08b353d711a092f40ddada9531bf`  
**Disposition:** Selected COV-80 oracle evidence; helper unchanged; independent review pending.

The earlier suite checked decreasing quadrature error and one financial difference step. The [new runnable checker](../chapter-18/code/check_order_step_study.py) adds48 rounded exact rule references,36 measured order checks, nine polynomial difference values and a three-step bond study.

For ax^2+x/2, trapezoidal signed error is a(b-a)h^2/6. For ax^4+x/2, Simpson signed error is 2a(b-a)h^4/15. Six signed-coefficient/interval sets for each rule at2,4,8,16 panels are compared with independent Fraction formulas, including final float rounding. Observed adjacent error ratios give orders2 and4 to the selected tolerance. These are exact smooth polynomial references, not universal behavior for singular/noisy/nonsmooth integrands.

At x=1/2 and h=1/8,1/16,1/32, expanded cubic/quartic expressions verify forward, central and second differences. The bond study uses100-digit Decimal direct powers at the actual represented query rates for h=2e-4,1e-4,5e-5. It retains actual callback prices, ideal stencils, signed analytic errors, duration and convexity. Actual callback discrepancies and a declared selected finite-rounding allowance are kept separate from ideal truncation. The allowance is not a certified universal floating-point error bound; no automatic optimal-step choice is claimed.

Three wrong methods are detected: zero trapezoid, trapezoid substituted for Simpson, reversed forward sign. The first new checker run passed against the unchanged helper; no numerical defect or correction was demonstrated. [Raw record](chapter-18-order-step-followup.json) retains the initial run, exact manifest, environment, commands and scoped outputs.

All25 Chapter18 Python sources compiled and15 scripts passed, with assertions enabled and timeout15 seconds on Python3.12.14/Linux. All25 source hashes match the pinned tree and remained unchanged after execution. This checker supplies the extended step study; the original assessment still uses its single selected h.

This one-checker addition follows [V-48](runtime-refresh-2026-10-30-r12.md), whose earlier full run compiled484 files/passed273 scripts/verified485 required hashes. Current pinned inventory is486 Python files/275 check-test scripts; these are inventory counts, not a new full execution. COV-80 remains partially open, with29 selected categories partially addressed and none closed by the register. Independent review, supported platforms and release acceptance remain pending.

Next substantive item: COV-80 finite-difference range contracts in Sections18.7/18.10: finite sample points, complete denominator/numerator range and nonzero-to-zero results; preserve the selected order/step evidence.
