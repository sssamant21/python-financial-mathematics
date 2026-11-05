# Section10.5 — Twelve local answer records

| Prompt | Independently reviewed answer | Evidence |
|---|---|---|
| 1. Due timing |Three payments at periods0,1,2 | Conceptual contract; source due timeline separately summed over these exponents |
| 2. Ordinary timing |Three payments at1,2,3 | Conceptual comparison and source ordinary-PV benchmark |
| 3. Due PV |100[1+10/11+(10/11)^2]=33100/121≈273.553719008…; rounded273.55 | Exact source and rational finite sum |
| 4. Due FV |100[(11/10)+(11/10)^2+(11/10)^3]=364.1 at period3 | Exact source and rational finite sum |
| 5. Shift identity |Due PV=ordinary PV×(1+i), using the same periodic rate and count | Source values and independent ordinary/due sums |
| 6. Zero rate |5×200=1000 | Source and integer reference |
| 7. Negative rate |100+100×10/9=1900/9≈211.111111111 | Source and exact rational sum |
| 8. Nominal monthly |.06/12=.005, or.5% monthly | Supplemental exact rational conversion |
| 9. Effective monthly |exp(ln1.06/12)−1≈.004867550565; annual factor reconstructed at precision100 | Supplemental Decimal derivation; no source converter |
| 10. Inverse |Target divided by the due PV factor; ten-payment factor independently sums discounts at0…9 | Source payment, Decimal direct-sum reference and source reconstruction |
| 11. Empty stream |PV0, FV0; inverse at zero payments is not identifiable | Source value and exception checks |
| 12. Audit |Discount each payment at0…n−1 and compare the sum, retaining unrounded values | Source timeline at24 periods compared with exact rational series |

The terminal FV date is period n, one period after the final due payment. This differs from valuing at period n−1. A single payment's due PV equals the payment even at a negative rate, since its date is0. Signed outflows follow the selected viewpoint. Ordinary/due identities are mathematical comparisons; implementation order matters at float-range boundaries. Contractual cent rounding and calendar timing remain separate specifications.
