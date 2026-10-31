# Book 02 — Sections 18.7/18.10 finite-difference range correction

**Date:** 2026-10-30  
**Baseline:** `a2f32bc271dc7ebf8bb8de55e9452a1d0a58495e`  
**Pinned executable source:** `e5780915662a4c69e0ef7acbbb961eadc16f2237`  
**Disposition:** Selected COV-80 correction/evidence; independent review pending.

The original Section18.7 central difference and Section18.10 copy both returned0 for f(t)=t/1e308, x=0,h=1e308, although the complete stencil rounds to representable1e-308. Their floating denominator2h overflowed. Other original probes raised on a representable second-difference result when h^2 overflowed, on a constant1e308 function whose second stencil is exactly zero, and on an overflowing forward numerator whose divided result is finite. [Raw record](chapter-18-difference-range-followup.json) retains all five original probes and the failed first regression.

Section18.7 now validates finite, distinct represented sample points before calling f, validates each callback value, combines the complete requested-step stencil as exact rational arithmetic and rounds once. Nonzero-to-zero underflow and final overflow raise ValueError; true zero cancellation is valid. This avoids intermediate numerator,2h,h^2 or2f(x) range loss. The forward stencil validates only its required forward point. Section18.10 delegates central differentiation to the shared Section18.7 helper; an observed call checks this integration.

The [runnable checker](../chapter-18/code/check_difference_range.py) uses2500-digit Decimal references for13 selected complete stencils, including large/tiny/ordinary cases and the valid one-sided forward domain. Eleven nonfinite/collapsed sample-point cases reject before any callback. Twelve nonfinite/bool callback cases and four true final-range cases reject. The stencil arithmetic probes include nonsmooth callbacks solely to check the finite-sample algebra; they do not assert that a classical derivative exists there.

All26 Chapter18 sources compiled and16 scripts passed on Python3.12.14/Linux with assertions enabled, separate processes and timeout15 seconds. This includes the preceding exact order/step study. All26 source hashes match the pinned tree and remain unchanged after execution. Corrected Section18.7 blob `6ceed2e6c91e7cc04da77910ef300720994c6b15`; final wrapper blob `511717c74a4b5272afb3eebe7dcf04b842dd8ee2`.

[V-49 full execution](runtime-refresh-2026-10-30-r13.md) compiled487 files, passed276 scripts and verified488 required hashes before/after at the same source pin. It includes three new checkers after V-48 (interpolation-bound, order/step and difference-range) and both changed source modules. Manuscript/report/tracker writes after this pin are outside executable inputs.

The manuscripts describe finite represented samples, requested-step denominators, the new dependency and limitations. No claim is made to recover callback rounding, remove truncation, prove smoothness or choose a universally optimal step. COV-80 remains partially open. Twenty-nine selected gap categories remain partially addressed; none closed by the register; these are not defect counts or percentages. Independent mathematical/editorial review, supported platforms, final release acceptance and canonical approval remain pending.

Next substantive item: COV-81 Section18.9 project evaluation-error contract: direct nonfinite-derivative rejection, invalid relative tolerances/iteration controls and callback sequencing, preserving documented zero-derivative fallback. Broader final applied-scope reconciliation remains open.
