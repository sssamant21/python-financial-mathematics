# Section 16.6 — Scalar secant-curvature boundary correction

**Date:** 2026-10-30  
**Category:** COV-75, partially addressed. Independent review remains pending.  
**Original source revision:** `d908f551c16551f4a2b9c67c74bf4ce35087d17a`  
**Corrected executable revision:** `af766375b896e5742389d343580dbd8d426afd33`

## Confirmed findings and retained failures

[Raw evidence](chapter-16-secant-boundary-followup.json) retains the initial failing checker (exit 1), four actual probes, original source blob hashes, corrected chapter manifest and all fifteen rerun outputs.

| Original probe | Actual result before correction | Required contract |
|---|---|---|
| Quadratic gradient `2*x`, pair `0, 2^-600`, threshold zero | ValueError from product underflow | Positive represented differences give curvature exactly two |
| `s=nextafter(1,+inf), y=nextafter(1,0)`, threshold one | ValueError because floating product rounds to one | Exact represented product exceeds one |
| Boolean callback `bool(x)`, pair zero/one | Accepted curvature one | Reject Boolean callback values before subtraction |
| `s=2^1000, y=2^-1000`, threshold zero | Returned zero | Reject unrepresentable positive curvature |

The first regression failure is preserved separately from the successful rerun. These are specific arithmetic/validation defects, not four additional COV categories.

## Correction and independently derived checks

The helper validates each callback value before taking its finite represented difference. It compares `Fraction(s)*Fraction(y)` strictly against `Fraction(threshold)`, so product underflow, overflow or rounding cannot change the comparison. It then requires a finite, strictly positive quotient; a quotient rounded to zero is rejected. Finite input/displacement/gradient-difference restrictions remain.

Source correction commit: `b930abcc65de6007678a88cf1970b6efb23555d1`; corrected blob: `61e9dd8ae631cf1984248806c0866753462582b4`.

The [runnable checker](../chapter-16/code/check_secant_boundaries.py) derives curvature two from `f(x)=x^2`, using exact dyadic pairs at six exponents (-600, -300, -30, 0, 300, 600) in both orientations: twelve exact references. Six adjacent-threshold gates test below/equal/above an exact dyadic product in both orientations. A separate exact-rational product proves the rounded-to-one counterexample. Two cases preserve intentional rejection by positive absolute thresholds. Nineteen callback/domain/range cases cover both callback positions, Boolean/string/NaN/Inf, zero/nonpositive pairs, nonfinite differences and quotient over/underflow.

Threshold is an absolute bound in objective units for consistently defined `s` and gradient difference `y`; multiplying the objective by a positive constant scales this product and requires a corresponding threshold choice. Default `1e-14` still rejects some valid but small pairs by policy. This is not a relative noise or conditioning criterion.

## Actual scoped rerun

At the corrected executable revision, **25/25 Chapter 16 files compiled and 15/15 check scripts exited zero**, Python 3.12.14/Linux, assertions enabled, 15-second timeout per script. All unchanged chapter inputs were copied only after their Git blob hashes matched the original pinned tree. The corrected local manifest matches the published executable blobs.

From a checkout of `af766375b896e5742389d343580dbd8d426afd33`:
```bash
cd books/book-02-mathematical-foundations-for-finance-with-python/chapter-16/code
python check_secant_boundaries.py
```
For the baseline, use a separate checkout of `d908f551c16551f4a2b9c67c74bf4ce35087d17a`, copy only this new checker into its code directory, and run it before applying the correction. It fails at the underflowing positive quadratic pair. The raw JSON preserves the other original probe outputs.

Fresh tree inventory at `af766375b896e5742389d343580dbd8d426afd33`: **469 Book 02 Python files and 258 check_/test_ scripts**. These inventory counts are not new full-book execution counts. [V-40](runtime-refresh-2026-10-30-r4.md) remains the last full run at its own earlier revision: 468 compiled, 257 scripts passed, 469 required hashes verified. This one helper correction and checker have the scoped rerun above; refresh the full book when further executable changes accumulate.

## Limits and checkpoint

The product comparison is exact for already-rounded finite differences, not exact differentiation of an arbitrary objective. Callback cancellation, nonfinite displacement/difference, user threshold choice and derivative accuracy remain limited. This scalar secant helper is not a BFGS matrix update or a general quasi-Newton solver. Independent mathematical/editorial review, supported environments, release acceptance and canonical approval remain open. Twenty-eight categories remain partially addressed; none is closed by the register.

Next executable item: COV-75 Section 16.6 Newton/quasi-Newton update scaling and represented-range boundaries, beginning with exact rational quadratic updates; keep general convergence/BFGS claims separate.
