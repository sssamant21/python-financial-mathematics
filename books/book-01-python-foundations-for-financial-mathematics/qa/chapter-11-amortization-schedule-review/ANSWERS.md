# Section 11.7 — Worked-answer and lab-step alignment

| Prompt | Review and evidence |
|---|---|
| 1. Columns | All six named fields are returned in both policies: period, opening, payment, interest, principal, closing. |
| 2. First interest | 10,000 × 0.005 = 50. The independent recurrence and source agree. |
| 3. First principal | Payment less 50 gives approximately 393.21, calculated before display rounding. |
| 4. First closing | 10,000 less unrounded first principal displays as 9,606.79. |
| 5. Second interest | The unrounded opening times 0.005 displays as 48.03; using the displayed opening is only an estimate. |
| 6. Payment identity | Payment equals interest plus principal; checked across exact rows with float tolerance and compared to the integer-cent oracle. |
| 7. Balance identity | Closing equals opening less principal; checked across exact rows and via the cent recurrence. |
| 8. Total principal | The exact-model principal components sum to 10,000 within tolerance; the cent ledger also retires its booked principal. |
| 9. Total interest | Total payments less original principal; the exact-model total is checked using the rational payment. |
| 10. Zero rate | 1,200 / 12 = 100 each period with zero interest, checked on all 12 source rows. |
| 11. Last rounded installment | Period rounding leaves a residual under a constant cent payment; the cent demo adjusts the last installment from 443.21 to 443.11. |
| 12. Maturity | Both policies end at zero for the standard fixture; the rounded balance is exactly zero cents. |
| 13. Interest timing | Each period accrues interest on its opening balance, then the payment reduces that balance. Checked with the fixture and cent oracle. |
| 14. Real payoff | Conceptual only. An external payoff amount can depend on accrued interest, fees and contract rules outside this periodic schedule. |

Save the Python block to the named file, run the demo and embedded suite, then compile it. No earlier lab or fixture file is imported. The printed rows are the **cent-rounded** demonstration; the worked table displays **unrounded-model** amounts rounded for presentation. Both workflows share the stipulated periodic rate, end-of-period timing and fixed term. The checklist's fees, day-count or irregular dates, prepayments and actual contract convention are applicability checks; this listing does not implement those cases.
