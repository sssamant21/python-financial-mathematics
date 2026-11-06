# Section 11.6 — Twelve local answer records

| Prompt | Reviewed answer | Evidence |
|---|---|---|
| 1. B(k) | Principal immediately after scheduled payment k | Conceptual timing |
| 2. Opening | B(0)=L | Both source endpoints |
| 3. Maturity | B(n)=0 for the fully amortizing model | Both source endpoints and exact recurrence |
| 4. Prospective | PV of n−k installments; A(n−k) at zero rate | Source versus independent recurrence |
| 5. Retrospective | Accumulated original loan less accumulated installments; L−kA at zero rate | Separate exact source calculation versus recurrence |
| 6. Zero rate | 1200−3×100=900 | Both source methods |
| 7. Recurrence | B(k)=B(k−1)(1+r)−A | Exact rational benchmark |
| 8. Remaining count | 24−5=19 | Supplemental integer arithmetic |
| 9. Timing | B(5) is measured after payment 5 | Conceptual |
| 10. Extra principal | 5000−400=4600 with no other adjustments | Exact source; no rescheduling implied |
| 11. Payoff | Contractual charges and accrued interest can differ from principal | Conceptual |
| 12. Validation | Compare both methods with an independently computed recurrence | Six boundaries/intermediate dates executed |

The example uses a 0.5% effective monthly rate, 24 end-of-period payments and unrounded amounts. The balance immediately after payment 12 rounds to 5149.58. The original extra-payment tolerance could accept amounts above the modeled balance; an explicit upper bound now applies without adding a currency rounding tolerance.
