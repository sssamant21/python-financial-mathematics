# Section 12.14 — Answers and project mapping

| Prompt | Review |
|---|---|
| 1–3 | A factor values one unit at maturity. Multiply each cash flow by its own factor and add the results. |
| 4–5 | Annual factor is (1+r)^−t and inversion is DF^(−1/t)−1. |
| 6–7 | At 4% for two years the factor is about 0.92455621 and 1,000 face is worth 924.56. |
| 8–9 | Nominal m-compounded factor is (1+r/m)^−mt; for 4% and two years with semiannual compounding it is 0.92384543. |
| 10–12 | Continuous factor is exp(−zt), about 0.92311635 for 4% and two years; invert with −ln(DF)/t. |
| 13 | Use z = ln(1+r); the observer converts quotes separately and compares all source factors and prices. |
| 14 | 30/1.04 + 1,030/1.05² is approximately 963.09. |
| 15 | A valid negative spot rate produces a factor above one; source and independent power agree. |
| 16 | The annual-effective forward equals [DF(t₁)/DF(t₂)]^(1/(t₂−t₁))−1. All four project intervals reconcile. |
| 17 | Conceptual: bootstrapping recovers discount factors consistent with instrument quotes; the lab receives already specified rates. |
| 18 | Conceptual: compounding changes the growth factor and must be stated to interpret the numerical quote. |

Save, run and compile the named standalone file. The observer executes all five spot/inverse/zero cases and both coupon valuation routes, with the final 1,050 payment occurring only at year five. Periodic valuation takes a frequency, and a supplied spot is required for each tenor. There is no external data file or preceding lab dependency.
