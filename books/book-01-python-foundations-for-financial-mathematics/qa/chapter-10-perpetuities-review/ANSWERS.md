# Section 10.8 — Twelve local answer records

| Prompt | Reviewed answer | Evidence |
|---|---|---|
| 1. Definition | Equal payments at periods 1, 2, 3, and onward, with no last payment | Conceptual ordinary timing |
| 2. Ordinary PV | With q=20/21, first term 100q and infinite sum 100q/(1−q)=2000 | Exact source and rational reference |
| 3. Inverse payment | 4000×.05=200 per year | Supplemental rational inversion and source PV reconstruction |
| 4. Inverse rate | 120/2400=.05 per year, consistent signs and nonzero PV | Supplemental division using source PV; rational expected rate |
| 5. Convergence | For i>−1 and nonzero payment, 1/(1+i)<1 requires i>0 | Conceptual geometric-series reasoning |
| 6. Zero rate | Nonzero equal payments do not sum to a finite PV | Conceptual divergence and source rejection |
| 7. Due PV | Add the immediate 100 to ordinary PV 2000, giving 2100 | Source and rational reference |
| 8. Deferred PV | First payment at 3 gives 100q³/(1−q)=2000q²≈1814.06 | Source and rational first-term/ratio reference |
| 9. Finite comparison | Positive payments discounted at positive rates leave a positive omitted tail | Source n=20 and exact finite sum |
| 10. Negative rate | At −2% the discount ratio exceeds one and terms do not decay | Conceptual divergence and source rejection |
| 11. Payer signs | Obligation is negative from payer's perspective | Source negative PV and rational reference |
| 12. Audit | Compare direct finite sums to the limit; tail after n is (100q/(1−q))q^n | Source finite values and exact direct sums/tail bound |

A due stream begins at zero. Deferral d counts periods before the ordinary annuity begins, so d=2 means first payment at 3. A zero stream has zero mathematical value, while the lab consistently requires positive rates even for zero payments. The finite-annuity helper uses that same positive-rate contract. There is no terminal FV date for an infinite stream. The model does not guarantee real receipts.
