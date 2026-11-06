# Section 12.7 — Answer and mini-project review

| Prompt | Review |
|---|---|
| 1 | Prices fall as yield increases in all seven checked cases. |
| 2 | Discount factors fall while the promised cash flows remain fixed. |
| 3 | 1,000 × 0.06 / 2 = 30. |
| 4 | 3 × 2 = six periods. |
| 5 | Matching 6% nominal coupon and yield produces par. |
| 6 | At 4% the price is above 1,000. |
| 7 | At 8% the price is below 1,000. |
| 8 | Analytical first derivative is negative and agrees with the independent numerical slope. |
| 9 | Analytical second derivative is positive and agrees with the independent numerical curvature. |
| 10 | Positive curvature means the falling curve bends upward. |
| 11 | Modified duration is the negative price derivative divided by price. |
| 12 | −2.7 × 0.01 gives approximately −2.7%. |
| 13 | 50 basis points is 0.005 in decimal units. |
| 14 | The quadratic correction is 0.5 × convexity × yield change squared; it improved every fixture approximation. |
| 15 | The central slope divides the difference between bumped prices by twice the step. |
| 16 | Conceptual: when more value is paid later, the timing can increase sensitivity. |
| 17 | All Macaulay weight is at year five for the zero; the lab reports modified duration, 5/1.03 in the checked case. |
| 18 | Conceptual: a call can change future flows, outside the fixed-flow model. |

Save and run the standalone file, then compile it. The observer runs the full 3–9% matrix, reconciles analytical derivatives with independently derived centered differences, and checks exact repricing plus both approximations for ±25, ±50 and ±100 bp. These shocks are changes to nominal annual yield under the same semiannual convention.
