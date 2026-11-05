# Section 19.2 — Logistic result range

Date: 2026-11-05. Baseline: `55750b5ea8864ce5e9587eb7eb2d567ed4afa79a`. Corrected executable revision: `9b4ae81bb9d057d7a904083f34f7586dcf3ec301`.

The original logistic helper failed ten of25 checks: a rounded initial/capacity ratio could lose the initial-value identity, collapse a denominator, or turn a positive balance into zero. The corrected helper validates inputs before exact zero/time-zero/equilibrium shortcuts. It evaluates a*K/(K*exp(−r*t)+a*(1−exp(−r*t))) in a private 850-digit decimal context, keeping positive denominator weights and avoiding the intermediate K/a ratio. A conservative exponent guard handles saturation only beyond the largest binary64 input ratio.

[Runnable checker](../chapter-19/code/check_logistic_range.py) uses 1,600-digit reciprocal-coordinate references, selected minimum-subnormal/max-finite combinations, time-zero identities and analytically bounded saturation. All20 numerical cases and five invalid-input cases pass. [Initial failures and reruns](chapter-19-logistic-range-followup.json) retain outputs, exits and scoped hashes. Run from chapter-19/code.

This is selected range evidence, not a guarantee of correct rounding for all decimal exponentials or financial model validity. All30 Chapter19 files compiled and20 scripts passed; [V-62](runtime-refresh-2026-11-05-r4.md) includes the correction.
