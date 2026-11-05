# Chapter 18 — Annuity present-value range

**Date:** 2026-11-04  
**Baseline:** `a6045562df26603dc69339e9b9ffc28549df57b4`  
**Corrected executable revision:** `eac8f8da5643d573ad9f5946c09b12622c422c7e`

The original annuity helper failed 14 of 22 numerical fixtures. It lost representable values by rounding the payment-times-discount-change product or the exponent to zero, and could overflow before payment scaling. For example, a payment of 1e-300 at rate −0.5 over 2,000 periods now yields approximately 2.296261390548509e302. Zero payment or periods now returns zero after input validation. Positive results that round to zero or infinity raise ValueError, including the zero-rate branch.

The nonzero-rate path retains the full compound discount and payment scaling at 850 decimal digits before conversion. The coarse exponent guards handle discount saturation and unavoidable overflow without computing enormous powers. The high precision is for range and cancellation in this educational implementation; it is not an all-input correct-rounding claim. Fractional periods describe the formula's analytic extension, not discrete payments.

The [runnable checker](../chapter-18/code/check_annuity_range.py) uses 1,200-digit direct cash-flow sums for bounded integer periods, the rationalized half-period identity, and justified limiting references for tiny or extreme periods. All 22 numerical cases and five invalid-input cases passed on rerun. [Initial failures and rerun](chapter-18-annuity-range-followup.json) retain exit codes and outputs. Run `python check_annuity_range.py` from chapter-18/code. [V-55](runtime-refresh-2026-11-04.md) covers the corrected source on candidate Linux only. Independent mathematical review, supported platforms and release acceptance remain open.
