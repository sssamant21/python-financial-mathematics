# Section 10.7 — Twelve local answer records

| Prompt | Reviewed answer | Evidence |
|---|---|---|
| 1. Growing payments | 100, 105, 110.25 at periods 1, 2, 3 | Supplemental exact payment list; no source schedule API |
| 2. PV at 10% | 100/1.1 + 105/1.1² + 110.25/1.1³ = 346750/1331, about 260.51840721 | Exact source and rational sum |
| 3. Equal rates | 400/1.05 = 8000/21 ≈ 380.95 | Exact source and rational benchmark |
| 4. Zero growth | Three level payments, each discounted at its own date | Exact source and direct finite sum |
| 5. Zero discount | 100 + 110 + 121 = 331 | Exact source and integer reference |
| 6. Declining payments | 100, 90, 81 | Supplemental payment list and source PV checked |
| 7. Growth above discount | Allowed for finite n; no infinite convergence assumption | Source and rational five-payment example |
| 8. Empty stream | PV and FV are zero | Exact source |
| 9. FV at n | Multiply PV by (1+i)^n mathematically; independently sum C(1+g)^(k−1)(1+i)^(n−k) | Exact source and direct finite sum |
| 10. Payer signs | Negative from the payer's perspective | Source negative PV and rational reference |
| 11. Equal-rate branch | General denominator becomes zero; every discounted term equals C/(1+i) | Conceptual derivation and source equal-rate values |
| 12. Audit | Discount each unrounded payment at k=1…n and sum | Source timeline and independent exact sum |

The payment is C at the first payment date, not a grown amount. Discount and growth must match the payment period. Equal and near-equal rates are distinct numerical cases. The terminal date is the last payment date, with no accumulation on that payment. The model does not imply receipt certainty or an infinite growth assumption.
