# Section 12.9 — Answer and project mapping

| Prompt | Review |
|---|---|
| 1 | Macaulay duration is average payment time weighted by discounted cash-flow shares. |
| 2 | Its units match payment time; years here. |
| 3 | Each weight is discounted flow divided by total price. |
| 4 | Weights sum to one; checked across all five coupons. |
| 5 | 1,000 × 0.06 / 2 = 30. |
| 6 | Three years × two gives six periods. |
| 7 | At matching coupon and yield, price is 1,000. |
| 8 | Positive interim weights move Macaulay duration below the three-year maturity. |
| 9 | A five-year zero-coupon bond has Macaulay duration five years. |
| 10 | Higher coupon lowered duration in the five-case comparison. |
| 11 | Lower coupon concentrates weight later and increased duration in the same comparison. |
| 12 | Modified duration divides Macaulay duration by 1+y/m. An independent price difference checks the result. |
| 13 | 25 bp is 0.0025 in decimal yield. |
| 14 | −1,000 × 2.7 × 0.0025 = −6.75. |
| 15 | 1,000 − 6.75 = 993.25. |
| 16 | Magnitude of dollar duration is price × modified duration per unit decimal yield. |
| 17 | Scale that amount by 0.0001 for the approximate one-basis-point magnitude. |
| 18 | Conceptual: changing call incentives can change the expected payments; the source holds payments fixed. |

Save, execute and compile the named script. The supplemental observer drives the five source coupon scenarios and checks both exact repricing at 6.5% and the first-order change at 6%. All weights reconcile and Macaulay duration decreases as coupon rises. The reported −6.75 worked arithmetic uses the hypothetical 2.7 duration, not the demo's 2.708596.
