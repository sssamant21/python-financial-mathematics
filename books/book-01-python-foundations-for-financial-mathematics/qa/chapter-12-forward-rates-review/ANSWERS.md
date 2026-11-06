# Section 12.15 — Answers and project mapping

| Prompt | Review |
|---|---|
| 1–2 | An implied forward describes an interval; spot discounting starts at the valuation date. |
| 3–5 | Interval discount factor is DF(t₂)/DF(t₁), growth is the reciprocal, and τ=t₂−t₁. |
| 6 | Annual-effective forward is the growth factor to 1/τ, minus one. |
| 7–8 | Node factors are 1/1.03 and 1/1.035². |
| 9 | Their implied 1y–2y forward is about 4.0024%. |
| 10 | The 1y–3y interval lasts two years, so the exponent is 1/2. |
| 11–12 | Continuous forward is log-growth divided by τ. With continuous spots 3% at 1y and 4% at 2y, the interval rate is 5%. |
| 13 | Nominal periodic forward is m times the excess of growth^(1/(mτ)) over one; checked with quarterly input. |
| 14 | Multiply starting factor by the interval discount, (1+f)^−τ. Every base and shifted node reconstructs within tolerance. |
| 15 | The 3y–5y interval lasts two years, even though its quote is annualized. |
| 16 | A factor increase implies a negative forward; the source agrees with the independent growth ratio. |
| 17 | Conceptual: the implied rate is not a guarantee. |
| 18 | Conceptual: an index projection curve can differ from the collateral discount curve; no multi-curve implementation is supplied. |

Run and compile the named standalone listing. The observer calls the source for all four base and shifted intervals and derives both annual-effective and continuous expectations. Adding 50 bp to every spot quote changes each interval forward slightly differently because the growth factors are nonlinear in those spot quotes. Exact source reconstruction consumes the reported rates and factors, so comparison uses float tolerance.
