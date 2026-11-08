# Next checkpoint: local Section 8.6 PV and first derivative

Executable revision `274ce4598c7a97d25f996a33512c1d8f5e176048`. [Four actual paired probes and independent complete references](chapter-08-section-06-pv-baseline.json).

These are `section_8_06.present_value` and `pv_rate_first`, separate from the corrected curvature helper and Section 8.5 implementations. New inputs retain finite complete prices/sensitivities lost to exponential overflow, a nonzero sensitivity beside a price rounded to zero, finite sensitivity beside unrepresentable price and zero-payment NaNs.

Complete Decimal price/first-derivative references agree at 200/400 digits, including explicit zero signs. Actual probes replay identically beside the hash-verified pinned source/dependency. JSON retains runnable probe code and labels unrepresentable prices separately from finite sensitivities.

Next establish complete scaling/output and signed-zero policies for these local helpers; preserve payment/rate/year validation, years-first derivative validation and nonnegative payment/horizon domains. Then assess local Taylor/exact shocks, signed cash-flow derivatives, polynomial helpers and sampled-second-difference output range separately. Do not claim those copies inherit the completed Section 8.5 or curvature passes. Resource limits and independent review remain open.
