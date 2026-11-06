# Section 12.4 — Worked answers and project

| Prompt | Review |
|---|---|
| 1–2 | Conceptual: zero coupons, one promised positive payment at maturity. |
| 3 | Discount face by (1+y/m) raised to mT. |
| 4–5 | 6% / 2 = 3% per period, and 3 × 2 = six periods. |
| 6–7 | Exact power gives a displayed price of 837.48 and discount to face of 162.52. |
| 8 | The inverse is m[(F/P)^(1/(mT)) − 1]. If 837.48 is the actual input price, its implied yield is slightly different from the original fixture yield. |
| 9 | Supplemental effective annual calculation: (1.03)² − 1 = 6.09%. |
| 10 | Supplemental continuous annual calculation: 2 ln(1.03) ≈ 5.9118%. |
| 11 | Exact factor 1 / 1.03⁶ displays as 0.83748426 at eight decimals. |
| 12 | Zero yield means price equals face. |
| 13 | A negative periodic yield above −100% can produce a price above face; both signs were executed. |
| 14 | Prices fall as yield rises in every row of the matrix. |
| 15 | Conceptual: all Macaulay PV weight falls at maturity, so duration equals three years. |
| 16 | T/(1+y/m), checked against an independently differenced price curve. |
| 17 | n(n+1)/[m²(1+y/m)²], checked analytically and by centered finite difference. |
| 18 | Conceptual: bill quotes can use different bases. No actual bill quote was evaluated. |

Save, run and compile the named standalone file. The mini-project calls its price, factor, duration and inversion functions for maturities 1, 3, 5 and 10 and nominal yields 2%, 4%, 6% and 8%, all semiannual. Each recovered yield agrees within tolerance, and longer maturities lower price at each of these positive yields. The results JSON retains each row.
