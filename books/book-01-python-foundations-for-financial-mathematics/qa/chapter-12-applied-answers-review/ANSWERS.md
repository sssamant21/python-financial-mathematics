# Section 12.17 — Chapter-wide answers and case

| Exercise | Review |
|---|---|
| 1 | 10,000 × 0.08 / 2 = 400. |
| 2 | Three semiannual years give six periods; final flow is 10,400. |
| 3 | A zero pays only the 5,000 maturity amount. |
| 4 | At matching conventions, coupon above yield means premium; the source premium fixture confirms the direction. |
| 5 | The 30 semiannual coupons plus maturity face value at matching yield price at 1,000. |
| 6 | 1,000 / 1.02⁴ ≈ 923.85. |
| 7 | Raising the discount rate lowers the positive-flow price. |
| 8 | At par the unique matching yield is 6%; this section's lab prices at the known yield and does not implement an inverse solver. |
| 9 | 99.25 + 0.80 = 100.05 per 100 face. |
| 10 | 30 × 40/180 ≈ 6.67 under the stated classroom fraction. |
| 11 | 4.2 / 1.025 ≈ 4.09756. |
| 12 | −50,000 × 4 × 0.0025 = −500. |
| 13 | 50,000 × 4 × 0.0001 = 20 per bp. |
| 14 | −45 + 1.25 = −43.75. |
| 15 | The tangent omits curvature and higher orders; the case scenarios quantify those errors. |
| 16 | 1 / 1.04² ≈ 0.92455621. |
| 17 | 30/1.04 + 1,030/1.05² ≈ 963.09. |
| 18 | 1.035²/1.03−1 ≈ 4.0024%. |
| 19 | 12+18+25 = 55 per bp; +10 bp gives an estimated −550. |
| 20 | Signed net DV01 is +20 per bp. No hedge execution is modeled. |
| 21 | 4.1% − 4.8% = −70 bp at the endpoints. |
| 22 | (1.03)²−1 = 6.09% annual-effective. |
| 23 | 1 / 0.99² ≈ 1.02030, valid for the stated negative spot rate. |
| 24 | Conceptual: an embedded option can alter expected payments and invalidate fixed-flow convexity. |

| Case task | Evidence |
|---|---|
| 1 | Three source timelines match independent coupon counts and principal redemption. |
| 2 | Each position's price matches the backward benchmark on the coupon date. |
| 3 | Macaulay, modified duration, convexity and DV01 agree with centered price differences. |
| 4 | Six common shocks are applied in nominal annual basis points to all three holdings. |
| 5 | All 18 source position scenarios match exact, linear and quadratic benchmarks. |
| 6 | All six portfolio rows reconcile; +100 bp gives −157.77 exact and B contributes the largest loss, −83.08. |
| 7 | Conceptual: a common YTM bump is not an identified arbitrage-free zero-curve shift. |

Save the named standalone file, run it, and compile it. The observer separately verifies the numeric worksheet, whole-case source workflow and conceptual answers. No earlier listing or external input is required.
