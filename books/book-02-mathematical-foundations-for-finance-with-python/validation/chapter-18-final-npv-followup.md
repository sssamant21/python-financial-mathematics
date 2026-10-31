# Book 02 — Final periodic valuation and false-root correction

**Date:** 2026-10-30  
**Baseline:** `13b98008e161a628429c99f6d0f0b83cbc66f6a0`  
**Pinned executable source:** `ae81661567a38edf78cac3a8c95bc0897819989a`  
**Disposition:** Selected COV-81 numerical correction; independent review pending.

For flows(-1,2+d,-(1+d)),d=2^-30, the rate polynomial is -r(r-d), with roots0 andd. The final lab's copied rounded-power NPV formula evaluated both endpoints of two non-root brackets as zero and returned endpoint_root at a non-root with zero-width bracket. The intervals[-d,-d/4] and[d/4,3d/4] contain neither algebraic root. [Machine evidence](chapter-18-final-npv-followup.json) retains the original endpoint values,false-success reports and failed first regression.

Section18.10 now delegates valuation to Section18.5's periodic_npv. One private exact rational Horner kernel supplies both generic valuation and the existing IRR-specific npv API. The generic valuation contract preserves nonempty single-cash-flow and all-zero streams; the IRR npv/scan/discovery routes still reject fewer than two periods and all-zero cash flows. A valuation zero is not evidence of a unique IRR. Nonzero valuation underflow and final overflow raise ValueError.

The [runnable checker](../chapter-18/code/check_final_npv_contract.py) verifies21 independent direct rational valuation references, including zero/single/large/subnormal/near-domain examples and represented-int conversion. Both false-root brackets now reject,while two true representable roots terminate correctly. Six stricter-discovery rejections remain; two final-range and seven invalid-input cases reject. Default worked IRRs retain rational-root-containing brackets to the requested width. One shared valuation call is observed and a deliberately false-zero helper output is detected.

All30 Chapter18 Python files compiled and20 scripts passed on Python3.12.14/Linux,assertions enabled,separate processes,timeout15 seconds. All30 source hashes match the pinned tree and remain unchanged after execution. Shared source blob `669110279befc6141f6eba806e333c7eb37feea9`; final source blob `aa6a3556c8e2f163ee6318ff738601ad14361bd7`.

[V-51 full execution](runtime-refresh-2026-10-30-r15.md) compiled491 files,passed280 scripts and verified492 required hashes before/after at the same pin,including the preceding final-study integration/checker. Later manuscript/report/tracker writes are outside executable inputs.

The correction concerns accepted represented inputs and actual final solver rejection. It does not validate financial data,prove unique/all IRRs,certify arbitrary numerical scale or promise large-polynomial throughput. Thirty selected gap categories remain partially addressed; none closed by the register. Independent mathematics/editorial review,supported environments,final reviewed-release validation and canonical approval remain pending.

Next substantive item: COV-80 Sections18.7/18.10 quadrature grid/result range contracts,including underflowed/collapsed panel steps and avoidable weighted-sum/intermediate overflow. Preserve the existing polynomial-order and integrated financial-study references.
