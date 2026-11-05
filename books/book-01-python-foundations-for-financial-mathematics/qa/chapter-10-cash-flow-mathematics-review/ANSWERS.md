# Section10.1 — Eight local answers

| Prompt | Independent answer and contract | Evidence |
|---|---|---|
| 1. Signs and dates | [(0,−500),(1,550)]; valuation reference is year0, cost negative and receipt positive | Complete exact source CashFlow objects inspected |
| 2. Discount1210 | 1210×(10/11)^2=1000 | Exact source and rational reference |
| 3. Multiple flows | 100×10/11+200×(10/11)^2=31000/121=256.198347107… ≈256.20 | Exact source and rational reference |
| 4. NPV | −1000+600×10/11+600×(10/11)^2=5000/121=41.3223140496… ≈41.32 | Exact source and rational reference; cost included once |
| 5. Shift date | V2=100×(21/20)^2=110.25 under the same constant effective quote | Exact source valuation at year2 and rational reference |
| 6. Zero rate | 80−30=50 despite differing dates | Exact source with both events and rational reference |
| 7. Negative rate | 81/(9/10)^2=100; negative rate has positive periodic factor | Exact source and rational reference |
| 8. Audit | Representing initial investment as a negative year0 event retains timing and signs and prevents subtracting cost twice | Conceptual contract review; source NPV fixture executes one initial cost |

The worked121-at-year2 example is100 today. With100 at year1 and200 at year2, valuation at year3 is100×(11/10)^2+200×11/10=341, also V0×(11/10)^3. Thus the shift test does not rely on a zero sum. Currency display rounding is deferred; fractions are benchmarks, not source currency accounting. Deterministic scheduled receipts and rates are assumptions rather than guarantees. No day-count/scheduling layer is implemented.
