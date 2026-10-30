# Section 16.8 — Rank-deficient two-parameter lab

**Date:** 2026-10-30  
**Category:** COV-75, partially addressed; independent review pending.  
**Original main:** `f7a2fe77cb715b3e2fd56291890b06f635196655`  
**Executable snapshot:** `0e2f5e4eebc9b3e0328a3bba2c6e0d7f88954db3`

## Original gap and addition

[Machine evidence](chapter-16-identifiability-followup.json) retains the original absent-field probe and exit-1 assertion failure, original source hashes, final scoped manifest and all twenty-four script outputs. The original lab described the two-parameter example in manuscript step10 but had no corresponding executable report. This was a coverage gap, not a demonstrated numerical defect.

Source addition commit `5f26f72a5dac0070fc9fc95329827e9226f59057`, blob `6cc7131ffe692af4768393bb23b3dcc7dd66ae66`, adds `rank_deficient_example()` and includes its computed output in the assessment. It is a fixed demonstration for observations `(2,3,4)`, model `m(a,b)=a+b`, and ordinary half-squared residual loss. It does not reuse the scalar rate-calibration observations as if they described this different model.

## Independent exact expectations

The supplied analytic Jacobian has three rows `(1,1)`. Its three two-row minors are zero; its first column is nonzero. Therefore its exact rank is one. The code computes these minors/rank and the normal matrix `J^T J=((3,3),(3,3))`, whose determinant is zero.

For `z=(1,-1)`, direct exact multiplication gives `Jz=0` and `(J^T J)z=0`. The model depends only on the parameter sum. Writing `s=a+b`, direct expansion gives
`L(s)=((s-2)^2+(s-3)^2+(s-4)^2)/2 = 1+3*(s-3)^2/2`.
Thus the identifiable fitted sum is3, the minimum loss is1, and no individual a/b pair is singled out.

The [runnable checker](../chapter-16/code/check_rank_deficient_model.py) uses independent Fraction expectations for:
- Five null shifts `d=-4,-1/2,0,1/2,4` of `(1,2)`: predictions3, residuals `(1,0,-1)`, loss1, gradient `(0,0)`.
- Five corresponding shifts of `(0,0)`: predictions0, residuals `(-2,-3,-4)`, loss29/2, gradient `(-9,-9)`. Flatness along the null direction does not imply the base point is optimal.
- The off-null pair `(2,2)`: predictions4, residuals `(2,1,0)`, loss5/2, gradient `(3,3)`.

All **eleven parameter cases**, three rank minors and five null-vector products pass. Two wrong-output variants (reported rank2 and an incorrect shifted parameter pair) are detected. The full assessment serializes as strict JSON.

The Jacobian is supplied analytically for this model; the lab does not implement automatic differentiation, generic SVD, a numerical rank tolerance, near-rank-deficiency diagnosis or statistical parameter uncertainty.

## Actual execution and reproduction

**34/34 Chapter16 files compiled; 24/24 check scripts exited zero**, Python3.12.14/Linux, assertions enabled, cwd each script's parent, 15-second timeout. Original source bytes matched pinned hashes before copying; all corrected scoped hashes matched the published executable tree.

[V-45 full refresh](runtime-refresh-2026-10-30-r9.md) at the same executable revision compiled **478 files**, passed **267 scripts**, and verified **479 required input hashes before and after**. It also includes the preceding normalized-loss corrections/checker.

From a checkout of `0e2f5e4eebc9b3e0328a3bba2c6e0d7f88954db3`:
```bash
cd books/book-02-mathematical-foundations-for-finance-with-python/chapter-16/code
python check_rank_deficient_model.py
```
For the absent-lab baseline, copy only this checker into a separate checkout of `f7a2fe77cb715b3e2fd56291890b06f635196655` and run it before adding the helper; the first report-field assertion fails.

This completes the selected executable lab-step example, not all Chapter16 proofs or independent review. Twenty-eight selected COV categories remain partially addressed; none closed by the register. Supported-platform validation, reviewed-release acceptance and canonical approval remain pending.

Next executable item: COV-76 Section17.4 adjacent-float active-set transition/endpoints around the exact rational uncapped portfolio optimum, with independent weights/multiplier/value references and existing tiny-empty rejection preserved. The Chapter17 coverage map explicitly retains adjacent-boundary/tolerance/degeneracy obligations.
