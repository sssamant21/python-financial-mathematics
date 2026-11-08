# Next checkpoint: Section 8.5 rate shock

Executable revision `536dc531ca19a913507977f63df20d2cefd1f90b`; [four actual probe/reference pairs](chapter-08-rate-shock-range-baseline.json). Completed PV/rate-sensitivity scaling does not repair the separate shock expression.

Four probes expose separate intermediate failures: an underflowed PV times an overflowing exponential (true change 1), an unrepresentable base PV with finite complete change (about -1.59667e293), an underflowed horizon/change product with finite complete change (about -8.88178e-17), and a zero payment producing NaN for a huge negative shock. Actual results are OverflowError, ValueError, negative zero and NaN respectively.

Independent differences of complete Decimal prices agree at 1600/2200 digits. The JSON retains the runnable probe and explicit zero signs. Probes replay identically beside the hash-verified pinned source and dependency. These are four failing selected observations, not four independently reviewed defects.

Next derive the complete represented-input price-change contract. Preserve years/change prevalidation, payment/rate/year domains and validation order; explicitly reconcile shifted-rate/exponent convention and final overflow/zero behavior. A finite change must not require a representable base PV or a separately representable shock exponential/product. Log-return, stable quotient, centered-copy, resource-limit and independent-review obligations remain open. Do not repeat completed PV/sensitivity or accumulation examples.
