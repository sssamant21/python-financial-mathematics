# Section 12.5 — Answers and project

| Prompt | Review |
|---|---|
| 1 | Price equals the sum of discounted promised flows. |
| 2 | 1,000 × 0.06 / 2 = 30. |
| 3 | 3 × 2 = 6 periods. |
| 4 | Last payment equals 30 + 1,000. |
| 5 | Nominal 6% gives 3% per half year. |
| 6 | At 6% nominal, the example prices at par. |
| 7 | Coupon PV is C[1 − (1+i)^−n]/i for nonzero i; the zero-yield limit is nC. |
| 8 | Principal PV is F/(1+i)^n. |
| 9 | At zero yield, 6 × 30 + 1,000 = 1,180. |
| 10 | At 4%, price is above face. |
| 11 | At 8%, price is below face. |
| 12 | Derivative is negative for positive future payments. Checked by monotonic scenarios and the negative shocks. |
| 13 | The flat factor is (1+y/m)^−k. Using these factors in the curve method gives par at 6%. |
| 14 | The supplied nonflat array gives the sum of row amounts times factors, or 1,057.90. |
| 15 | For zero coupon only face times the maturity factor remains. |
| 16 | Deliberately doubling redemption adds exactly one discounted face in the benchmark. The generic tuple has no independent face metadata to infer the intent. |
| 17 | Conceptual: dirty equals clean plus accrued interest under the appropriate convention. |
| 18 | Conceptual: default and actual settlement dates are excluded. |

Run and compile the named standalone script. The supplemental runner calls its functions at all six yields, derives each +100 bp shock independently and checks the curve factors in date order. Direct and annuity prices agree within tolerance. Project classification follows comparison to face; it is not a separate source API in this listing.
