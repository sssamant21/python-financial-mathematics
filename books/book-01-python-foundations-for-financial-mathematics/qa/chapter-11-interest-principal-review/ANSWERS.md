# Section 11.5 — Twelve local answer records

| Prompt | Reviewed answer | Evidence |
|---|---|---|
| 1. Payment | Interest plus principal repayment | Every source row reconciled |
| 2. Interest | I(k)=r times the opening balance | Source and exact recurrence |
| 3. Principal | P(k)=A−I(k), equivalently A times the remaining discount power | Source and exact recurrence |
| 4. Balance | B(k)=B(k−1)(1+r)−A | Checked across rows |
| 5. First interest | 10000×.005=50 | Source and rational benchmark |
| 6. Principal | About 393.21 from displayed amounts | Unrounded exact benchmark and display check |
| 7. Closing balance | About 9606.79 from the 10000 opening principal | Exact source and unrounded benchmark |
| 8. Next interest | About 48.03 at .005 on the first closing balance | Exact source and unrounded benchmark |
| 9. Direction | With positive rate and falling balance, interest falls and principal rises; at zero rate interest is zero | Source monotonic and zero-rate checks |
| 10. Principal sum | L in the ideal schedule | Source and exact reconciliation |
| 11. Interest sum | nA−L in the ideal schedule | Source sum versus rational identity |
| 12. Negative amortization | Payment below accrued interest increases balance if unpaid interest is capitalized | Conceptual, outside the implemented fully amortizing model |

The first three displayed rows must be rounded independently from unrounded amounts: row 2 principal 395.17 and closing balance 9211.62, row 3 closing balance 8814.47. Periodic rates match the payment interval; payments are end-of-period with no fees, resets or prepayments.
