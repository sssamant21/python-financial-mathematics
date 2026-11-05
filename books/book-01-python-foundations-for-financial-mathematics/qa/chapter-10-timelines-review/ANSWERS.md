# Section10.2 — Ten local answer records

| Prompt | Reviewed answer and units | Evidence |
|---|---|---|
| 1. Borrower perspective | +10000 at year0;−11000 at modeled year1, under the borrower's sign convention | Complete source schedule inspected |
| 2. Time-zero payment | −250; discount factor1 independently of the valid annual rate | Source NPV and exact integer reference |
| 3. ACT/365F | 2026-01-01→2027-01-01 has365 days, hence365/365=1 | Source date calculation and exact rational reference |
| 4. ACT/360 | Same dates give365/360=73/72≈1.013888889 | Source and exact rational reference |
| 5. Leap year | 2024-01-01→2025-01-01 has366 days, hence366/365≈1.002739726 | Source and exact rational reference |
| 6. Same-day receipts |100+150=250 PV; both rows remain separate | Source NPV and rational reference; stable-label inspection |
| 7. Discount |110/(11/10)=100 in one modeled year | Source NPV and rational reference |
| 8. NPV |−100+110/(11/10)=0; cost entered once | Source and rational reference |
| 9. Reordering | Date-assigned valuation is invariant to event order aside from floating summation effects | Source reversed fixture and all six permutations of a nonzero stream; independent reference300/121 |
| 10. Audit | Separate same-day rows retain event traceability; net PV alone does not identify constituent receipts | Conceptual rationale and direct stable source schedule inspection |

The leap-span receipt110 is worth about99.973891… at10% EAR under ACT/365F, rather than100; the exact Decimal reference is retained in results.json. The analogous365-day ACT/360 discount also differs from one-year annual valuation. Day-count denominators and annual effective compounding are distinct choices. Calendar dates are supported; datetime timestamps are now explicitly rejected rather than truncated to whole days. No business-day or contractual accrual rules are inferred.
