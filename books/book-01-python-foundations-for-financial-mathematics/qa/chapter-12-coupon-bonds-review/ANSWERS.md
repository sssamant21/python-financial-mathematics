# Section 12.3 — Worked answers and project alignment

| Prompt | Review |
|---|---|
| 1 | Conceptual: fixed coupons and one redemption are promised, not guaranteed. |
| 2 | Periodic coupon equals face × annual coupon rate / frequency. |
| 3 | 1,000 × 0.06 / 2 = 30. |
| 4 | 3 × 2 = 6 periods. |
| 5 | 30 + 1,000 = 1,030 at maturity. |
| 6 | 6 × 30 = 180 lifetime coupons. |
| 7 | 180 + 1,000 = 1,180 nominal promised total. |
| 8 | Nominal 6% / 2 = 3% per period. |
| 9 | Matching the yield and coupon rates under the same convention gives 1,000. |
| 10 | A 4% yield gives a premium. |
| 11 | An 8% yield gives a discount. |
| 12 | Annual coupon income is 1,000 × 0.06 = 60. |
| 13 | 60 / 1,050 ≈ 5.7143%; this income ratio is not yield to maturity. |
| 14 | The positive-yield annuity factor is [1 − (1+i)^−n] / i; its zero-yield limit is n. |
| 15 | With no discounting the example price is 1,180. |
| 16 | The only nonzero flow is redemption, worth 1,000 / 1.03⁶ at the specified yield. |
| 17 | 2,000 × 0.08 / 4 = 40. |
| 18 | The direct and annuity routes agree at every matrix yield and match the separate backward valuation. |

Save and run the named script, then compile it. Build the matrix by calling both source pricing functions at 3% through 8% nominal annual yield and dividing each rate by two for the periodic rate. All six prices decrease, 6% is par, and the reported method difference is zero in the checked cases. The runnable observer drives the full matrix; the exact demo covers only three entries.
