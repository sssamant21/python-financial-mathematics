# Next checkpoint: Section 8.5 log return

Executable revision `63ff224ef85691be6a513db55f27c3f567889f76`. [Eight actual probes and independent references](chapter-08-log-return-range-baseline.json).

For positive finite prices the model ln(end)-ln(start) is finite, including maximum/minimum-subnormal price ratios. Current log1p((end-start)/start) can return infinity or raise ValueError when a relative change overflows or rounds to -1. Four retained range probes demonstrate these failures. Four half-price, adjacent-unity and equal-price controls retain working accuracy.

Independent differences of Decimal logarithms agree at 200/400 digits. Actual probes replay identically beside the exact hash-verified source/dependency. The JSON retains runnable code. These are selected failing observations, not independent review.

Next establish a range-safe log-return evaluation that preserves near-unity accuracy, finite positive-price domains, input validation priority and equal-price zero behavior. Stable exponential quotient, centered-copy, resource-limit and independent-review obligations remain open. Do not repeat completed rate-shock/PV/accumulation examples.
