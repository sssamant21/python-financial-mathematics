# Book 02 — Chapter 6 Series Boundary Review

**Date:** 2026-10-27  
**Scope:** Selected geometric-sum inputs and verification tolerances; not comprehensive annuity or independent mathematical review.

The local Chapter 6 code matched tree `8856152c1fc16c20c2aca74ffedf4e9db7846188` except for two modified modules and a new regression script. Changes were published through `19f52c51f959953c6e45f2b5898a6dca10f2adc4`.

## Findings and corrections

- A tiny positive ratio such as 1e-100 was rejected by the geometric-sum formula because ratio minus one rounded to -1, which made log1p invalid. The formula now uses log of the directly supplied positive ratio. This does not change the separate rate-input formula, where log1p(rate) remains appropriate.
- The project verifier accepted infinite tolerances, making its comparisons effectively unconstrained. It now requires finite, nonnegative tolerance values and rejects Boolean values under the existing numeric contract.
- Regression cases cover a tiny ratio, a ratio adjacent to one, an analytic finite geometric sum, invalid tolerances and a zero-rate annuity reference.

## Runtime evidence

All ten Section 6.1–6.10 check scripts and the new series-boundary script exited zero on Python 3.12.14/Linux, each from its code directory with a 15-second timeout. This is not full book-wide, cross-platform or final-revision validation.

## Remaining work

- Independently review growing-annuity valuation across extreme rates, including whether an intermediate PV or geometric factor can overflow when the requested FV remains representable.
- Review direct-sum and closed-form independence, cancellation, negative ratios and large period counts.
- Complete exercise and manuscript coverage, mathematical review and a final agreed revision rerun.
