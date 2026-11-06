# Section 12.1 — Worked answers and mini-project

| Prompt | Review |
|---|---|
| 1. Issuer | Conceptual: the entity borrowing by issuing the debt security. |
| 2. Face value | 1,000 is promised principal, distinct from the maturity coupon. |
| 3. Coupon | 1,000 × 0.05 / 2 = 25. |
| 4. Periods | Three years × two coupons per year gives six. |
| 5. Final payment | Last coupon plus principal gives 1,025. |
| 6. Promised total | 5 × 25 + 1,025 = 1,150. |
| 7. PV | Conceptual: discount the promised payments; the lab does not model default risk. |
| 8. Periodic yield | Nominal 0.06 / 2 gives 0.03 per half-year. |
| 9. Par | Matching nominal coupon and yield under the same convention gives a price of 1,000. |
| 10. Premium | Below-coupon yield raises price above face; checked at 3% and 4%. |
| 11. Discount | Above-coupon yield lowers price below face; checked at 6% and 7%. |
| 12. Zero coupon | One maturity cash flow; 1,000 / 1.03⁶ at 6% nominal with two periods per year. |
| 13. Rate risk | The fixed flows are unchanged but discounted values change. The project exercises the price mechanism, not market risk. |
| 14. Credit risk | Conceptual: a contractual schedule does not guarantee receipt. |
| 15. Reinvestment | Conceptual: coupon reinvestment and early sale may change realized return. |
| 16. Perspective | Conceptual: borrower receives proceeds and pays; investor pays the purchase price and receives the promised flows. |

Run the standalone listing and compile it. For the mini-project, reuse its pricing and classification functions at all five yields; its demo prints only three. The runner checks the complete monotone price sequence, six flows, the regular and final coupons, positive finite prices, par, and the zero-coupon variant. The independent benchmark values each payment directly. No curve, settlement adjustment or regulatory quotation convention is involved.
