# Section10.4 — Twelve local answer records

| Prompt | Independent answer / interpretation | Evidence |
|---|---|---|
| 1. Payment times | End of periods1,2,3; no payment at time0 | Conceptual ordinary-annuity contract; no schedule generator supplied |
| 2. PV |100Σ(10/11)^k,k1…3=331000/1331≈248.685199098…; rounded248.69 | Source and exact rational finite sum |
| 3. FV |100[1+11/10+(11/10)^2]=331 at period3 | Source and rational finite sum |
| 4. Zero rate |5×200=1000 | Source and integer reference |
| 5. Nominal monthly |.06/12=.005=0.5% monthly | Supplemental exact rational conversion; source also asserts this arithmetic |
| 6. Effective monthly |exp(ln1.06/12)−1≈.004867550565; percentage≈.4867550565%, rounding.48676% | Independent100-digit Decimal conversion, not a source conversion function |
| 7. Inverse payment |P divided by the positive ordinary PV factor; for nonzero i, P×i/[1−(1+i)^(−n)], and for i0, P/n with n>0 | Source inverse against independent Decimal finite discount sum; zero/signed branches tested |
| 8. Negative periodic rate |100×10/9+100×(10/9)^2=19000/81≈234.567901235; rounded234.57 | Source and exact rational sum |
| 9. Reconcile |FV=PV(1+i)^n for the same periodic quote and terminal date | Source and independent rational benchmark |
| 10. Negative payments |An outflow from the stated perspective; valuation changes sign | Source signed-PV call against negative rational reference |
| 11. Zero payments |PV=0; zero-count FV also0; inverse payment is not identifiable | Source value/exception checks |
| 12. Independent check |Discount each dated payment and sum unrounded terms; compare against geometric-factor output | Source12-payment PV against direct rational series |

The supplied periodic rate must match payment spacing. Equal nominal and effective annual percentages have different monthly equivalents. Target1000 at5% for10 payments is checked using Decimal's sum of ten discounts, then reconstructed by the source. The direct FV fix is tested at a long negative-rate horizon where PV is outside float range but FV remains finite. Mathematical inversion is distinct from contractual cent-rounded amortization. No external acceptance, production ledger or calendar interpretation is established.
