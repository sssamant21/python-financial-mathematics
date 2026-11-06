# Section 11.9 — Worked answers and lab steps

| Prompt | Review and scope |
|---|---|
| 1. Definition | An extra amount applied to principal after the regular payment. An amount held for a future installment is outside the model. |
| 2. Original payment | Dividing principal by the sum of discount factors gives the stated positive-rate formula and L/n at zero. The answer now includes both branches. |
| 3. Modified recurrence | Opening plus accrued interest less scheduled and extra amounts. The oracle independently computes the opening from remaining payments and past extras. |
| 4. First interest | 10,000 × 0.005 = 50. |
| 5. First total | The unrounded installment plus 100 displays as 543.21. |
| 6. First principal | First payment less 50 displays as 493.21. |
| 7. First balance | Original principal less that unrounded reduction displays as 9,506.79. |
| 8. Interest effect | Next opening is 100 lower, so next interest is 0.50 lower. |
| 9. Term effect | Recurring 100 reduces the example from 24 to 20 periods. A smaller extra need not save a full period; it can reduce the final payment. |
| 10. Recast | Conceptual only. Recasting can lower the payment while keeping the remaining term. |
| 11. Savings | Subtract prepayment interest from baseline interest before rounding; the recurring 100 fixture saves 119.85. |
| 12. Timing | A principal reduction avoids accrual on that amount in later periods. The source checks an earlier versus later start for recurring extras. It does not isolate a one-off prepayment or hold the total count of extras fixed. |
| 13. Last payment | Scheduled and extra payments together may not exceed principal plus that period's interest. The large-extra case pays exactly 1,010 on the first period. |
| 14. Contract | Conceptual only. Verify posting, timing and fees separately; lender rules are not exercised. |

Save the standalone listing, run the three demo scenarios and embedded tests, then compile the same file. The lab assumes a constant effective periodic rate, end-of-period posting after interest, and recurring extras from the specified start. Starting after maturity is equivalent to baseline. Row identities and total principal were checked, with no cent rounding or lender acceptance implied.
