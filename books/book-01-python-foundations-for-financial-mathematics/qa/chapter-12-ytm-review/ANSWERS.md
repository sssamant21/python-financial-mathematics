# Section 12.6 — Answer and solver project alignment

| Prompt | Review |
|---|---|
| 1 | YTM discounts the promised remaining cash flows to market price under a specified convention. |
| 2 | Yield is unknown; observed price is supplied. |
| 3 | 1,000 × 0.06 / 2 = 30 per half year. |
| 4 | Three years × two payments per year gives six. |
| 5 | At 1,000 the nominal annual yield is 6%. |
| 6 | At 950 the required yield is higher than 6%. |
| 7 | At 1,050 it is lower. |
| 8 | Current yield is 60/1,050 ≈ 5.7143%. |
| 9 | The yield residual is the present value of promised payments less observed price. |
| 10 | Its derivative is negative for this positive-cash-flow schedule. |
| 11 | If trial price exceeds observed price, raise the yield (lower the discount factor). |
| 12 | The single-flow inverse is m[(F/P)^(1/(mT))−1]; the numerical source agrees with an independently priced zero. |
| 13 | Zero yield gives nC + F = 1,180. |
| 14 | A price above that total implies negative yield in this model. |
| 15 | Reprice at the reported yield and check the relative residual. |
| 16 | Frequency changes periodic discounting and nominal annual quoting. |
| 17 | Conceptual: coupon reinvestment at YTM is not guaranteed. |
| 18 | Conceptual: a computed yield does not guarantee payment. |

Save, run and compile the named standalone file. Use the same semiannual frequency for prices, inversions and current-yield comparisons. The runner solves all five project prices; 900 and 950 are discounts, 1,000 is par, and 1,050 and 1,100 are premiums. The sequence is strictly decreasing, relative residuals pass the stated default, and the independent 4.75% price recovers that yield. Current yield is the annual income ratio and does not require compounding. Negative and zero yields are tested separately.
