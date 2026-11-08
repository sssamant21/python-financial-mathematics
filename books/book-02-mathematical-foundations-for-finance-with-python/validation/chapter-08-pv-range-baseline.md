# Next checkpoint: Section 8.5 PV and rate sensitivity

Executable revision `a2de6dbfdacb2ef34d30674ee51b5509a8dc4f35`; [four actual value/sensitivity pairs](chapter-08-pv-range-baseline.json). These functions are separate from the completed accumulation helpers.

The minimum-subnormal payment at rate -1 and horizon 1000 raises OverflowError despite finite complete PV and sensitivity. At payment 1, rate 1 and horizon 750 the derivative loses a nonzero negative subnormal to a rounded zero price. Maximum payment with rate -maximum-float and minimum-subnormal horizon returns infinities although the complete sensitivity is finite. Zero payment at a huge negative rate/horizon returns NaNs instead of algebraic zeros.

Complete direct Decimal references at 200/400 digits agree, including explicit zero signs. Actual probes were replayed against the hash-verified pinned Section 8.5 source. The runnable probe is included in the JSON. Unrepresentable final values are labeled separately without choosing the next batch's output policy.

Next derive the complete PV and sensitivity contract, preserve payment/rate/horizon domains and years-first derivative validation, then reconcile the separate rate-shock expression and change validation. Log-return, stable quotient, centered copy, integer resource limits and independent review remain open. Do not repeat the completed accumulation/exponential/logarithm corpus.
