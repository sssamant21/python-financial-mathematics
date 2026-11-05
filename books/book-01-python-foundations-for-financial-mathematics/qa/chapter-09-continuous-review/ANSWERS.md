# Section 9.12 — Worked exercise review

| Prompt | Reviewed answer | Evidence |
|---|---|---|
| 1. FV at 3% continuous for two years | 5000×exp(.03×2) ≈ 5309.18 USD. The exponent uses annual continuous rate times years. | Exact source and Decimal oracle |
| 2. Continuous 5% to EAR | exp(.05)−1 ≈ .0512710964, or 5.12710964%. | Exact source and Decimal oracle |
| 3. Effective 5% to continuous | ln(1.05) ≈ .0487901642, or 4.87901642% continuously compounded annually. | Exact source and Decimal oracle |
| 4. Discount 2000 for 18 months | With 18 months defined as 1.5 model years, PV =2000×exp(−.04×1.5) ≈1883.53 USD. No actual calendar basis is inferred. | Exact source and Decimal oracle |
| 5. Different 6% conventions | A 6% continuous quote produces EAR exp(.06)−1 ≈6.18365465%; a 6% effective annual quote already defines full-year growth6%. | Exact source and convention review |
| 6. Composition | Under the same constant rate, exp(r×t1)×exp(r×t2)=exp(r×(t1+t2)). A changing rate path requires another explicit model. | Exact source factor composition and algebra |

The worked10000 example gives approximately10618.37 after one year at6% continuous. The worked15000 receipt discounted three years at4% continuous gives approximately13303.81. The latter's unrounded value reconstructs15000 within tolerance. Annual factor equivalence is verified for nominal6% across frequencies1,2,4,12,365; the rate quotes themselves are not equal.
