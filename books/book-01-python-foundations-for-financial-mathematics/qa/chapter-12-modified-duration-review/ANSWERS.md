# Section 12.10 — Answer and project mapping

| Prompt | Review |
|---|---|
| 1–2 | Modified duration is −(dP/dy)/P, per unit decimal yield change. |
| 3 | D_Mod = D_Mac/(1+y/m), verified at base yield. |
| 4–6 | Semiannual 6% gives periodic 0.03, 30 coupon and six periods over three years. |
| 7–8 | At 6% yield the matching-coupon bond prices at 1,000; rising yield lowers its price. |
| 9 | 50 bp = 0.005. |
| 10–12 | With hypothetical duration 2.7, +50 bp gives −1.35% or −13.50 at price 1,000; −50 bp gives +1.35%. |
| 13 | Dollar duration magnitude is P × D_Mod per unit yield. |
| 14–15 | Multiply by 0.0001 for DV01 magnitude; the hypothetical example gives 0.27. |
| 16 | Exact change is P(y+Δy)−P(y). |
| 17 | The centered estimate divides the negative two-price difference by 2hP(y). The benchmark calculates both prices independently. |
| 18 | Conceptual: callable bonds can have yield-dependent expected cash flows; the fixed-flow source does not implement effective duration. |

Save, run and compile the named standalone script. The supplemental observer calls the source at all six signed shocks and checks the exact and linear values against backward valuation and its derivative. Curvature makes the errors positive in this example; the price curve is steeper at lower yields, so equal positive and negative shocks need not give equal errors. The tested holding has 250 times the reference face and 250 times its DV01.
