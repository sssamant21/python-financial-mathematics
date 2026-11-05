# Section 8.3 — Worked answer review

| Prompt | Reviewed answer | Evidence |
|---|---|---|
| 1. Interpolation | Day 2 is halfway from day 1 at USD 1020 to day 3 at USD 1010. Linear interpolation gives USD 1015; day 2 is not a supplied observation. | Supplemental rational midpoint and exact source grid |
| 2. Threshold equality | Day 1→3 lasts two days. The separator condition is strictly greater than two, so this interval remains connected. | Exact source coordinates |
| 3. Threshold three | Day 4→7 is now allowed. B connects USD 1015 to USD 1030; A still lacks day 4, so its adjacent segment remains broken. | Exact source with controlled policy |
| 4. Row accounting | One rendering-only NaN separator is added at the next day coordinate. The six original rows, including their 11 observed account values, remain unchanged. | Exact source data and render arrays |
| 5. Ledger state | Day 2 has 12 shares: the day-1 update persists up to, but not including, the day-3 update. | Supplemental lookup and exact step convention |
| 6. Repeated state | Day 3 and day 4 both report eight shares. The repeated observation is not evidence of a trade. | Exact source ledger |
| 7. Unknown valuation | Persistence is part of the separate ledger contract. It supplies no missing account valuation, so the gap must remain. | Source NaN and semantic review |
| 8. Performance inference | The endpoints are USD 1060 and USD 1025, but the fixture gives no deposits, withdrawals or other performance inputs. Higher ending account value alone does not establish better investment performance. | Conceptual scope review |
