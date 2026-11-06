# Section 11.10 — Worked answers and lab steps

| Prompt | Review and scope |
|---|---|
| 1. Definition | Conceptual: the new loan replaces the old obligation at the comparison date. |
| 2. Old payment | 200,000 divided by the sum of 240 old-rate discount factors displays as 1,432.86. |
| 3. New payment | Financing the stated 3,000 fee increases the principal to 203,000 and increases the new installment. |
| 4. Monthly savings | Old less new using unrounded amounts is 167.56 when displayed. |
| 5. Simple break-even | 3,000 / 100 = 30 periods in the heuristic. This assumes the difference lasts; the separate worked offer gives 18. |
| 6. No savings | Positive upfront cost with a higher new payment gives no positive payment-savings break-even. |
| 7. Term reset | Same-rate 360 versus 240 periods lowers the installment but raises total scheduled interest. This is a worked counterexample to payment-only comparison. |
| 8. Common horizon | Include the remaining principal after the horizon installment. At maturity it is zero. |
| 9. PV components | Upfront cost, discounted installments and discounted residual; checked separately against the recurrence. |
| 10. Financed costs | Upfront zero is compatible with a higher principal and installment; it does not remove the financing obligation. |
| 11. Discount rate | A separate valuation input; the example uses 0.003 per month, distinct from either loan rate. |
| 12. APR | Conceptual only. Regulatory APR is not computed by the lab. |
| 13. Holding period | Selling early changes the number of payments and requires settling remaining principal. Model horizons 12, 36 and 60 illustrate the difference. |
| 14. Decision | Positive keep-minus-refinance PV means lower modeled refinance cash outflows. At 12 months the sign is negative, despite the lower installment. |

Save the listing as the named standalone Python file, run its demo and embedded tests, then compile it. Compare loans at the same valuation date with matching periodic units. For the modeled common horizon, stop at or before the shorter term and include remaining principal after that period's scheduled payment. The checklist's regulatory, contractual, tax and product details require separate evidence.
