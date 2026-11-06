# Section 13.9 — scoped TWR review

Reviewed [Time-Weighted Return](../../chapter-13/13.09-time-weighted-return.md) against main at `575f8e472cb8e5eb0d2c62d9487d3d9f75a61cbb`. Run `python -B review.py` from this directory; it writes [results.json](results.json). The [baseline](baseline.json) records the same checks on the original manuscript, including every failed predicate. JSON records the exact source and listing hashes, command output, expectations and tolerances.

The single lab workflow requires only Python's standard library. Save the unmodified fence as `time_weighted_return.py`, run it, and compile it. The runner also checks that importing the file in isolation produces no output. The three commands passed before and after the correction, and the first command ran the same twelve existing test methods both times. No historical unique methods were added. The 43 additional predicates are recorded separately: 15 initially failed and all passed after correction.

| Local records | Review and independent expectations |
|---|---|
| 1–4 | Gains are the changes 10 and −16 divided by capital 100 and 160. Linking leaves 99 cents per dollar; unadjusted growth is 44/100. |
| 5–9 | Adding 50 to 110 gives 160, and withdrawing 20 leaves 90. The 9 gain on 90 repeats the first 10% gain, so 100 performance-index units grow to 121 while actual balance ends at 99. |
| 10 | The quarterly factor is 131222/125000, giving 4.9776%. |
| 11–14 | Profit is 165−100−50 = 15, and time at risk adds 25 to starting capital, giving 15/125. A 50 deposit without portfolio gain leaves unit price constant. Exercise 12 now supplies the opening value explicitly. |
| 15–18 | Conceptual: allocation between internal accounts leaves ownership unchanged; a retained dividend is portfolio income; fee basis changes measured profit; pre-flow valuation separates investment changes from the movement of outside capital. |

The separate seven-task mini-project was checked with [a supplemental ledger and CSV exporter](project.py), because the exact manuscript functions return a scalar and have no order key or CSV contract. Row 0 is the input capital. The three post-flow bases are 1280, 1116 and 1227.60; the returns are 8%, −5% and 10%. The independent benchmark issues or redeems shares at each pre-flow price; unit prices rebased to 100 give 108, 102.60 and 112.86, and the exact-source scalar agrees with 12.86%. The naive growth is 22.76%. The supplemental checks exercise order, missing data, nonfinite flows, exhausted capital and CSV structure. The supplied ordinal tests ordering only; timestamp cutoffs, source-system reconciliation, and the operational policy in §15 were reviewed as design considerations.

**F103.** Binary float arithmetic erased signed small returns, overflowed before offsetting factors and flows, and could confuse a positive remaining valuation with a true total loss. The corrected listing retains fractions through accumulation and converts the final result with an explicit reporting boundary. The Dietz approximation checks output range but does not impose the exact long-only total-loss convention. The project now supplies order keys, defines final-row handling, and provides the worked index. The fraction examples are educational; no performance or cross-platform claim is made. F28, F32 and independent acceptance remain open.
