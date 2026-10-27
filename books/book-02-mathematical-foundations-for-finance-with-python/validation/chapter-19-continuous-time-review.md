# Book 02 — Chapter 19 Continuous-Time Boundary Review

**Date:** 2026-10-27  
**Scope:** Selected constant-rate account and event cases, not a complete chapter or independent mathematical review.

The local Chapter 19 code matched tree `76b6e049be0447647c6986a1a56d028e974aeafa` except for the six files modified in this review. Additional changes addressed related implementations in Sections 19.3, 19.5, 19.6, 19.8 and 19.10, with a shared regression script; all code changes were published through `507073bec27cd7248eb6c9e6f9ea81d2aa6fee3d`. The event-policy clarification was subsequently added to Section 19.7.

## Findings and changes

- **Sections 19.1, 19.7 and 19.9:** An extremely small nonzero rate could cause a contribution to disappear when rate × time underflowed. The changed expressions use the limiting contribution factor when the exponent rounds to zero and an expm1/exponent formulation otherwise. Regression cases exercise the zero-exponent limit.
- **Sections 19.7 and 19.9:** The depletion ratio could round to zero and return a zero depletion time for positive balance and withdrawal. The code now uses the zero-rate limit in that case; a regression case expects 0.5 years for a synthetic example.
- **Event ordering:** At an exactly simultaneous jump and zero crossing, Section 19.7's illustrative code permits the jump before its post-jump depletion check, while Section 19.9 explicitly gives terminal depletion precedence. The Section 19.7 manuscript now calls out this difference and the need for a numerical event tolerance. The policy of either example was not changed.

## Evidence

All ten Section 19.1–19.10 check scripts and the new shared small-rate regression script exited zero on the local snapshot using Python 3.12.14/Linux, with each invoked from its own directory and a 15-second timeout. These are script exits, not proof of complete mathematical or exercise coverage. No whole-book or cross-platform rerun was performed.

## Follow-up and open findings

- **Section 19.8 discrete contributions:** The near-zero denominator case was corrected using an exprel ratio with a zero-argument limit. Positive, negative and small-rate cases were checked against a 60-digit Decimal finite sum; a subnormal-rate boundary was also checked. The 11 Chapter 19 scripts passed locally on Python 3.12.14 after this change, using tree `0555806b3439d1d5e5bbcba2d1324eee21ecbca0` plus the two changed code files, published through `773899d0f0f52b037c5d34095c1f5b3a136dee8b`. Extreme-range and independent numerical review remain pending.
- Review the changed formulas with independent high-precision references over near-zero, subnormal and large-magnitude inputs. The zero-ratio fallback does not establish accuracy for every subnormal ratio or avoid all intermediate overflow.
- Define and test a practical tolerance for near-simultaneous events; floating-point comparisons can affect event ordering.
- Review all Chapter 19 exercises, numerical solvers and assumptions; conduct independent mathematical review and rerun the final exact revision across supported environments.
