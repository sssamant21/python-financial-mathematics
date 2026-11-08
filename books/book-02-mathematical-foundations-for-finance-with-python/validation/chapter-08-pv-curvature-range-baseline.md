# Next checkpoint: Section 8.6 PV curvature range

Executable revision `5b919e8b93caf2cd4d6f003b61f60d07bec4bd69`; [six actual probes and complete references](chapter-08-pv-curvature-range-baseline.json). This is the separate Section 8.6 `pv_rate_second`, not the already corrected Section 8.5 PV/rate sensitivity.

Complete C·t²·exp(-r·t) references at Decimal 200/400 digits agree. Actual failures include a lost nonzero subnormal at horizon 750; premature exponential overflow despite finite curvature; NaNs for a huge discount exponent and a zero-payment identity; squared-horizon underflow hiding about 1.79769e-92; and squared-horizon overflow hiding about 1.59667e293. All six model outputs in this selected corpus are finite.

The source blob was verified in the pinned snapshot and the probes replayed identically. Runnable reference/probe code is in JSON. Zero factors are handled algebraically; a conservative negative-exponent cutoff is safe for this bounded three-factor coefficient. These are selected observations, not independent mathematical review.

Next establish complete curvature scaling/final-output and signed-zero conventions, preserving years-first validation and nonnegative payment/horizon domains. Check this helper independently of a rounded local PV. Assess the distinct Section 8.6 value/first-derivative, shock, cash-flow and sampled-second-difference obligations separately; do not attribute Section 8.5 passes to these copies. COV-49 other-helper/range and COV-51 implicit-contract/resource/review scope remain open.
