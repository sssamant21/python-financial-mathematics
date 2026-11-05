# Chapter 18 — Present-value and error diagnostic range

Baseline: `9d5c9ce9786c2963561a64905d73a6e6a4bf73f0`. Corrected executable revision: `5504f2cf019487dae61912e6b01bdb6440931307`.

The original Section 18.1 helper failed 13 of 26 fixtures. For example, the largest finite payment divided by 2¹⁰²⁴ should give 0.9999999999999999; the original raised during denominator evaluation. A minimum-subnormal payment divided by 0.5¹⁰⁷⁵ should give 2, but the rounded denominator was zero. The corrected lab evaluates the whole scaled value in a private wide decimal context. A coarse log bound avoids evaluating powers only when the final value is already beyond the combined binary64 range. Zero payment, zero periods and zero rate retain their exact shortcuts after validation.

The error report calculates absolute and relative differences from the exact represented operands before converting each result. A zero reference still produces an undefined (null) relative error. Nonfinite results or nonzero results rounding to zero raise ValueError rather than returning a misleading diagnostic. These are selected range and arithmetic checks, not a universal rounding guarantee for the decimal PV power.

[Runnable checker](../chapter-18/code/check_pv_error_range.py) uses exact rational powers and ratios, an exact square-root identity and analytically bounded extreme cases. All 26 fixtures passed. [Initial failures and rerun](chapter-18-pv-error-range-followup.json) retain output and exits. Run `python check_pv_error_range.py` from chapter-18/code. See [V-56](runtime-refresh-2026-11-04-r2.md) for the candidate Linux run.
