# Section 12.16 — Worked answers and project deliverables

| Prompt | Review |
|---|---|
| 1–4 | 1,000 × 0.06/2 = 30; three semiannual years give six flows; final cash is 1,030 and matching yield prices at par. |
| 5–6 | YTM inverts the flat price equation. Bisection resolves a supplied bracket; the relative residual checks the reported yield. |
| 7–9 | Macaulay is ΣkPV/(mP), modified divides by 1+y/m, and convexity weights k(k+1)PV and divides by m²P(1+y/m)². Centered differences independently check both sensitivities. |
| 10 | One basis point is 0.0001. |
| 11–12 | Linear P&L is −P D_Mod Δy; add 0.5 P Convexity Δy². Checked on all six project shocks. |
| 13–14 | Spot factor is (1+s)^−t. Nominal 6% semiannual equals annual-effective 6.09%, not 6%. |
| 15 | A zero-coupon bond has one nonzero maturity cash flow. |
| 16 | Aggregate P&L sums position-level dollar changes; verified for each scenario. |
| 17 | Conceptual: common YTM bumps do not by themselves identify a parallel zero-curve shift. |
| 18 | Tests must be executed; the run record captures the interpreter and observed results. |

| Deliverable | Scoped evidence |
|---|---|
| Implementation | Exact sole source listing extracted from the manuscript; no supplemental engine substituted. |
| Test transcript | Results JSON records demo, suite, isolated import and compile outcomes. |
| Analytics table | Three positions' prices and metrics match the independent benchmark. |
| Six-shock stress report | All position and aggregate changes reconcile and appear in the retained results. |
| Compounding demonstration | Flat-equivalent and nonflat spot values are separately checked. |
| Limitations | Educational equal-period, fixed-flow model; no actual settlement, embedded options, production curves or independent acceptance. |

Save the named script, execute it, then compile it. Position face represents the entire holding in common currency; periods are counts rather than years. The observer calls the source with held face, nominal YTM and explicit frequency, and evaluates the spot equivalence under annual-effective quoting.
