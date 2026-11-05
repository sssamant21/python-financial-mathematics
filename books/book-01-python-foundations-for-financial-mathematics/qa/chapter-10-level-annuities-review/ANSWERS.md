# Section10.3 — Ten local answer records

| Prompt | Independently reviewed answer | Evidence |
|---|---|---|
| 1. Definition | Equal payments at regular intervals over a finite term; payment timing still requires specification | Conceptual alignment with ordinary/due/deferred distinctions |
| 2. Schedule | [(1,100),(2,100),(3,100)] for ordinary end-of-period payments | Complete exact source schedule inspected |
| 3. PV | 100Σ(10/11)^k for k1…3=331000/1331≈248.685199098… | Source closed form and independent finite rational sum |
| 4. FV | 100[1+11/10+(11/10)^2]=331 at year3 | Source and exact finite rational sum |
| 5. Zero rate |5×200=1000; no discounting | Source and integer reference |
| 6. Monthly periodic rate |.06/12=.005=0.5% per month; the quote is nominal annual convertible monthly | Supplemental exact rational arithmetic; no source conversion function |
| 7. Negative rate |100×10/9+100×(10/9)^2=19000/81≈234.567901235 | Source and rational discounting |
| 8. Shift one period |100Σ(10/11)^k for k2…4=original PV×10/11≈226.077453726 | Source explicit shifted timeline and independent rational sum |
| 9. Reconcile | FV=PV(1+i)^n at the same periodic quote and terminal date; independent six-payment sum used for benchmark | Source FV/embedded PV-FV test and finite rational sum |
| 10. Fractional count |2.5 is not an integer number of equal payments; define an explicit stub event instead | Source exception and conceptual boundary rationale |

The source demonstrations use five payments100 at8% per period; benchmarks sum individual powers with unrounded intermediates. The ordinary-annuity terminal horizon is period n, when the last payment needs no accumulation. Payment signs follow the selected account/depositor perspective. A negative periodic rate must still have1+i>0. Factors and monetary display are not a production currency-rounding policy; finite periods do not define a perpetuity or a real contractual schedule.
