# Chapter 16 — Finite-difference boundary correction

**Date:** 2026-10-30  
**Category:** COV-75, partially addressed; no category closure or independent sign-off.

## Source and retained failure

Original main: `05942d67022665f8727bda7effaaf38b8b73d1fd`. [Machine evidence](chapter-16-derivative-boundary-followup.json) retains original source blob SHAs, the failing new checker (exit 1), nine constant-callback probes, the corrected local manifest and all fourteen script outputs.

In all three helpers, `x=1, h=1e-20` collapsed both endpoints yet returned zero. With `x=0, h=1e308`, the denominator overflowed yet a constant callback again returned zero. In both second-derivative copies, `h=1e-200` underflowed `h*h` to zero and raised ZeroDivisionError. A small first-derivative step at zero is not automatically invalid: the retained first-derivative `h=1e-200` constant result is a valid geometry control, not a defect.

## Correction and independent expectations

Sections 16.2–16.4 now reject nonfinite/collapsed endpoints and nonfinite/zero denominators before callbacks, validate finite numeric callback outputs excluding bool, and require a finite final estimate. Source correction commits: 16.2 `205921047cd4d1ae7482f88584f23d097effcbbc`; 16.3 `f62339f38069dc1e4a0e907dffb05ecb10132d71`; 16.4 `7b0291569970f211f89c520c2e8ba057d54f7d5f`.

[Runnable checker](../chapter-16/code/check_derivative_boundaries.py), introduced at `fe24a814a26fb542c7b5d6e0f34a0df8ff6eb6a7`, checks 35 input/callback guards, three additional nonfinite-result cases, nine exact dyadic polynomial pairs and one unequal-offset case. The polynomial expectations follow direct binomial expansion, independently of the helper implementation:
- For `f(x)=x^3`, the centered first difference equals `3*x*x+h*h`.
- For `f(x)=x^4`, the centered second difference equals `12*x*x+2*h*h`.

At `x=1/2` and `h=2^-6,2^-7,2^-8`, Fraction expectations and returned floats agree exactly; these dyadic operations have no rounding error. This also exposes the known nonzero truncation terms rather than comparing only a zero or a minimizer.

## Actual rerun and reproduction

All **24 Chapter 16 Python files compiled; 14/14 check scripts exited zero** on Python 3.12.14/Linux with assertions enabled, 15 seconds per script. Corrected executable snapshot: `fe24a814a26fb542c7b5d6e0f34a0df8ff6eb6a7`; unchanged files were verified against pinned source hashes. The [V-40 full refresh](runtime-refresh-2026-10-30-r4.md) additionally covers all Book 02 Python files.

From a checkout of that revision, run:
```bash
cd books/book-02-mathematical-foundations-for-finance-with-python/chapter-16/code
python check_derivative_boundaries.py
```
To reproduce the original failure, use a separate checkout of the original revision above and copy only the new checker from the corrected revision into its Chapter 16 code directory; its first collapsed-stencil assertion fails. Do not replace the original helpers before this baseline run. The JSON contains exact original and rerun blob manifests and actual output.

## Limits and next item

The formula still divides by the requested step. At `x=1, h=3*2^-53`, both endpoints move but the represented offsets differ; the checker records that policy. Guards are not accuracy guarantees: truncation, cancellation, callback domains and intermediate numerator range remain limitations. This is a restricted floating-point teaching stencil, not an arbitrary-range differentiation library. No supported-platform, independent mathematical review, release acceptance or canonical approval is inferred.

Twenty-eight selected COV categories remain partially addressed; none is closed by this register. Next executable item: COV-75 Section 16.6 scalar secant-curvature product/threshold and callback boundaries, using exact represented-number expectations before any correction.
