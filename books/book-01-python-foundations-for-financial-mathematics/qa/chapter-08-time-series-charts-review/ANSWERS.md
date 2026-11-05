# Section 8.4 — Worked answer review

| Prompt | Reviewed answer | Evidence |
|---|---|---|
| 1. Repeated hour | 01:30 EDT is 05:30 UTC; 01:30 EST is 06:30 UTC. The offset distinguishes the instants, which are one elapsed hour apart. | Source labels and coordinate spacing |
| 2. Different timezone | Converting to Tokyo changes local representation without moving the instants. The aligned frame, index values and presence flags are identical. | Source with converted input |
| 3. Coverage | The 6×2 grid has 12 slots. The missing row removes two, and BETA's missing value in a supplied row removes one, leaving nine. | Source counts and independent arithmetic |
| 4. Baseline | Each index must begin at the same instant. Individually selecting first quotes would change the comparison windows; the source rejects a missing first price. | Source rejection and interpretation |
| 5. BETA final index | 100×206/200 = 103; the final price is 3% higher than the common base price. It is neither USD 103 nor total investment return. | Source and rational oracle |
| 6. Calendar | The grid is a caller-supplied synthetic hourly schedule. It cannot establish whether any exchange opened or owed quotes on that Sunday. | Conceptual review |
| 7. Present with no values | A non-baseline row can be supplied with both cells missing. It and the absent row both have zero observed prices; only the supplied row has its presence flag set. | Source with modified fixture |
| 8. Multi-date display | Add local dates at transitions or use a date-aware locator/formatter. Retain timezone offsets where a clock time repeats. This is a presentation change, not a change to the UTC coordinates. | Design review |
