# Book 02 — Sections 18.7/18.10 quadrature range correction

**Date:** 2026-10-31  
**Baseline:** `6879315494b209ed12fdcd5e542147ba2a4dfef1`  
**Pinned executable source:** `bb4535d9b6692b7e33430e91b33a6808ded5e4b4`  
**Disposition:** Selected COV-80 numerical correction; independent review pending.

Original probes showed collapsed quadrature grids invoking duplicate sample points and returning false zero integrals,loss of smallest-subnormal endpoint halves,and intermediate weighted-sum overflow despite representable complete rules. For a constant1e307 over[0,5e-324] with two panels,all three entry points returned0 after sampling0 twice; the nominal integral is4.9406564584124654e-17. Such an unresolvable two-panel grid now rejects before callbacks. A one-panel trapezoid with constant5e-324 over[0,1] now retains the representable5e-324 result instead of losing both endpoint halves.

The shared routines construct the exact nominal uniform grid from represented bounds and panel count,round each query once,and reject duplicate/nonincreasing grid points before evaluation. Finite callback values and rational rule weights are combined with the exact nominal panel width before one final result rounding. This avoids overflowing width/weighted-sum intermediates when the full result fits. The nominal step may exceed float range if the finite represented nodes and full result remain valid. Nonzero result underflow and final overflow raise ValueError; true zero cancellation remains allowed.

Section18.10's public Simpson routine delegates to Section18.7,with an observed shared call. The [runnable checker](../chapter-18/code/check_quadrature_range.py) verifies32 complete-rule references from2500-digit Decimal constant/affine/odd-integral expectations and independently constructed grids. It tests six pre-callback collapsed grids,nine invalid callback values and six unrepresentable final results. [Raw evidence](chapter-18-quadrature-range-followup.json) retains nine original probes,the failed regression,first passing rerun,manifest and scoped outputs.

All31 Chapter18 sources compiled and21 check/test scripts passed on Python3.12.14/Linux,assertions enabled,separate processes,timeout15 seconds. All31 source hashes match the pinned tree and remain unchanged after execution. Existing exact polynomial-order and integrated financial-study checks passed unchanged.

This source/checker batch follows [V-51](runtime-refresh-2026-10-30-r15.md),the earlier full491-file/280-script/492-input pass. Current pinned inventory is492 Python files/281 scripts,not a new full execution. COV-80 remains partially open;30 selected gap categories remain partially addressed,none closed by the register.

The contract applies to the nominal rule evaluated at rounded callback queries,not an exact continuous integral for arbitrary functions. Grid validity does not prove smoothness,accuracy,good conditioning or a complete error bound. Rational arithmetic cost grows with panels/input precision. Independent mathematics/editorial review,supported environments and release/canonical acceptance remain pending.

Next substantive item: COV-80 Section18.7 stable continuous_cashflow_pv complete product/quotient and small exponent range,with separate financial references and retained unsupported large-growth-factor limits.
