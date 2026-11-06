# Section 13.4 — Worked answers and project

| Prompt | Review |
|---|---|
| 1–4 | ln(1.10)≈0.09531018, ln(0.90)≈−0.10536052, ln(1)=0, and 110/100 gives ln(1.10). |
| 5–6 | The inverse gives +8% and −5% respectively. |
| 7–8 | Product 0.99 gives ln(0.99)≈−0.01005034 and −1% simple. |
| 9–10 | Three factors give 1.089 and ln(1.089)≈0.085260 at six decimals. |
| 11 | A −100% return has zero gross and no finite log; the source rejects it. |
| 12 | ln(1.000001)≈0.0000009999995. |
| 13–14 | ln(1.21)/2=ln(1.10); the annual-effective equivalent is 10%. |
| 15 | Consistent domestic-per-local FX factors give ln(1.08×0.98). |
| 16–17 | Supplemental: the equal-weight portfolio gross factor is one, but averaging the asset logs gives 0.5ln(0.96)<0. |
| 18 | The exact contextual expression uses `math.log1p(R)`; the standalone lab also preserves input decimal precision with a rational factor before taking logs. |

Save, run and compile the named standalone listing. The observer checks all four project rows for +3%, −3%, +5% and −2%, evaluates each contextual expression with the required variable and `math` supplied, and reconciles the log sum to ln(1.0280739) and 2.80739% simple. Arithmetic mean simple return is 0.75%, distinct from the mean log return. A zero terminal price gives −100% simple but is rejected by the log series. No prior lab or data file is required.
