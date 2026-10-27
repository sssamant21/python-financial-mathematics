# Book 02 — Chapter 19 Continuous-Time Boundary Review

**Date:** 2026-10-27  
**Scope:** Selected constant-rate account and event cases, not a complete chapter or independent mathematical review.

The local Chapter 19 code matched tree `76b6e049be0447647c6986a1a56d028e974aeafa` except for the six files modified in this review. Those changes were published through `0eeff9a6b382cb7f39de7b24324042e007375ae8`. The event-policy clarification was subsequently added to Section 19.7.

## Findings and changes

- **Sections 19.1, 19.7 and 19.9:** An extremely small nonzero rate could cause a contribution to disappear when rate × time underflowed. The changed expressions use the limiting contribution factor when the exponent rounds to zero and an expm1/exponent formulation otherwise. Regression cases exercise the zero-exponent limit.
- **Sections 19.7 and 19.9:** The depletion ratio could round to zero and return a zero depletion time for positive balance and withdrawal. The code now uses the zero-rate limit in that case; a regression case expects 0.5 years for a synthetic example.
- **Event ordering:** At an exactly simultaneous jump and zero crossing, Section 19.7's illustrative code permits the jump before its post-jump depletion check, while Section 19.9 explicitly gives terminal depletion precedence. The Section 19.7 manuscript now calls out this difference and the need for a numerical event tolerance. The policy of either example was not changed.

## Evidence

All ten Section 19.1–19.10 check scripts exited zero on the local snapshot using Python 3.12.14/Linux, with each invoked from its own directory and a 15-second timeout. These are script exits, not proof of complete mathematical or exercise coverage. No whole-book or cross-platform rerun was performed.

## Open findings

- **Related implementations still require correction or scoped numerical limits:** Sections 19.3, 19.5, 19.6, 19.8 and 19.10 contain similar `u*expm1(r*t)/r` account expressions. Sections 19.8 and 19.10 also contain depletion formulas vulnerable when the ratio rounds to zero. Section 19.8's discrete-contribution expression needs separate analysis near zero. The ten passing scripts did not cover these edge cases.
- Review the changed formulas with independent high-precision references over near-zero, subnormal and large-magnitude inputs. The zero-ratio fallback does not establish accuracy for every subnormal ratio or avoid all intermediate overflow.
- Define and test a practical tolerance for near-simultaneous events; floating-point comparisons can affect event ordering.
- Review all Chapter 19 exercises, numerical solvers and assumptions; conduct independent mathematical review and rerun the final exact revision across supported environments.
