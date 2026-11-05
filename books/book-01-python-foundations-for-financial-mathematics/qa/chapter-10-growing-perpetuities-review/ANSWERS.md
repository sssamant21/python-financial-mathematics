# Section 10.9 — Twelve local answer records

| Prompt | Independently reviewed answer | Evidence |
|---|---|---|
| 1. First payment | C1 is paid at the end of period 1 | Conceptual timing |
| 2. PV | With q=103/108, 100/(1.08×(1−q))=2000 | Source and rational geometric sum |
| 3. Next payment | 100×1.03=103 | Supplemental exact arithmetic |
| 4. Updated valuation | 103/(1.08×(1−q))=2060 | Source and rational geometric sum |
| 5. Convergence | Given growth greater than −1, discount greater than growth gives 0<q<1 | Conceptual series argument and source domain checks |
| 6. Equal rates | Nonzero payments have nondecaying discounted terms; reject | Conceptual argument and source rejection |
| 7. Declining stream | 100/0.07=10000/7≈1428.57 | Source and rational value |
| 8. Due | C0=100 immediately; q=103/108 gives 100/(1−q)=2160 | Source and rational geometric sum |
| 9. Deferred | First payment at 3 means delay 2; 2000×(25/27)²≈1714.68 | Source and rational benchmark |
| 10. Inverse | 2000×(1.08)×(1−q)=100 | Supplemental inversion and source reconstruction |
| 11. Sensitivity | Fixed positive first payment: PV increases as spread shrinks. Fixed negative first payment: PV decreases, with growing absolute magnitude. Zero remains zero. | Conceptual sign analysis and selected signed source values |
| 12. Audit | Sum terms over each finite horizon; exact omitted tail equals infinite PV×q^n | Source finite values, independent finite sums and exact tail bound |

The initial P11 answer said “The model value increases sharply” without specifying the first-payment sign. The correction holds the payment fixed and distinguishes all three signs. The ordinary formula uses the next payment, not the last payment. Rates are periodic and consistent; the finite convergence helper checks the infinite model's domain without assuming its monetary PV fits a float. These are deterministic calculations, not forecasts.
