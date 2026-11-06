# Section 12.12 — Answers and portfolio project

| Prompt | Review |
|---|---|
| 1–3 | Sensitivity is value response to rates. For fixed positive flows, a higher yield reduces price; exact P&L is P(y+Δy)−P(y). |
| 4–5 | Dollar linear change is −P × D_Mod × Δy; quadratic correction is 0.5 × P × convexity × Δy². |
| 6 | 50 bp = 0.005. |
| 7–8 | Hypothetical 1,000 price and 2.7 duration give −13.50 and approximate new price 986.50. |
| 9–11 | DV01 magnitude is P × D_Mod × 0.0001; 0.27 per bp in the exercise, or 6.75 estimated loss for +25 bp. |
| 12 | Sum currency sensitivities under matched shock and currency conventions, not raw durations. Portfolio duration and convexity use market-value weights. |
| 13 | Conceptual: parallel means equal shifts at the relevant nodes. This model applies a common bump to individual nominal yields. |
| 14 | Conceptual: steepening increases the long-minus-short rate difference. |
| 15 | Conceptual: key-rate risk measures sensitivity to selected curve nodes. |
| 16 | Conceptual: spread changes can move price without a risk-free change. |
| 17 | Conceptual: matching DV01 leaves convexity, basis, spread and curve-shape risks. |
| 18 | Exact repricing within the specified model is the approximation benchmark. |

Run and compile the named standalone listing. The observer executes the source for every project position, the six signed common shocks and a mixed-frequency case. For +100 bp, exact portfolio P&L is −157.774171, linear is −161.456661 and second order is −157.709162. The QA JSON reports both methods for all scenarios. The demo covers Bond A; call the portfolio functions separately with the three position tuples. No external fixture or later curve model is needed.
