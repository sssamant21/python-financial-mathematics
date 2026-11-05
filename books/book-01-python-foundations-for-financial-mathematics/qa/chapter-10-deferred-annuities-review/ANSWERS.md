# Section10.6 — Twelve local answer records

| Prompt | Independent answer / contract | Evidence |
|---|---|---|
| 1. Dates |d2,n3 gives periods3,4,5: first is d+1, last is d+n | Conceptual convention and source timing method; no schedule-generator API |
| 2. Zero delay |d0 reduces to ordinary end-of-period PV | Source and rational ordinary sum |
| 3. Deferred PV |100Σ(10/11)^k for k3…5≈205.524958…; rounded205.52 | Source and exact rational sum |
| 4. Factor identity |Ordinary PV×(1+i)^(−d), using the same periodic quote | Source and independent rational product |
| 5. Zero rate |5×200=1000 for any finite modeled delay | Source delay100 fixture and integer benchmark |
| 6. Empty stream |PV0; no inverse payment can be uniquely inferred at n0 | Source value and exception checks |
| 7. Negative rate |100[(10/9)^2+(10/9)^3]=190000/729≈260.631001372; rounded260.63 | Source and rational benchmark |
| 8. Extra delay |At10%, multiply previous PV by10/11 | Source and exact rational sum; negative-rate additional delay also checked |
| 9. Monthly nominal quote |.06/12=.005 per month | Supplemental exact rational derivation; no source converter |
| 10. Inverse |Target divided by deferred unit-PV factor; at n>0 and zero rate, target/n | Source inverse and independent Decimal sum over4…13; source reconstruction |
| 11. Outgoing payments |Negative from the payer's perspective | Source signed-PV call and negative rational reference |
| 12. Audit |Discount each payment at d+1 through d+n and sum without early rounding | Source timeline with24 payments/delay7 against exact rational series over8…31 |

The deferral count is not the first payment date: d3 means the first payment is at4. At positive rate, an additional delay reduces PV; at negative rate it increases PV for positive receipts; at zero rate it has no effect. The source's model periods are not calendar dates. Fees, receipt uncertainty, taxes and contractual rounding remain outside the model. Factor-first evaluation supports a large payment with finite deferred PV even when ordinary monetary PV is not representable, without claiming all mathematically finite cases are supported.
