# Section 12.13 — Answers and project mapping

| Prompt | Review |
|---|---|
| 1–4 | Conceptual: a curve relates a specified rate to tenor. Spot rates discount zero-coupon flows, par rates price standard coupon instruments at par, and forwards are implied future-interval rates. |
| 5–6 | Endpoint comparison distinguishes upward and downward. Interior shape is not inferred from the label. |
| 7 | 4.5% − 3.0% = 150 bp. |
| 8 | Linear interpolation halfway between 3.0% and 3.5% gives 3.25%. |
| 9 | Halfway between 4.0% and 4.5% gives 4.25%. |
| 10 | Annual-effective discount is (1+r)^−t. |
| 11 | At two years and 3.5%, discount is 0.93351 to five decimals. |
| 12 | Multiply the unrounded factor by 1,000 to obtain 933.51 to cents. |
| 13 | Conceptual: discount each flow at its own date, then sum. The lab implements single-payment zero prices. |
| 14 | Conceptual: a single bond YTM is not a maturity-indexed spot curve. |
| 15 | The factor ratio raised to 1/(t₂−t₁), minus one, gives the annual-effective forward. |
| 16 | Exact growth ratio gives approximately 4.00% for 1y–2y. The project also checks the 2y–3y forward. |
| 17–18 | Conceptual: interpolators can differ; interpolation is not instrument calibration. |

Save, run and compile the named listing. Use the four supplied annual-effective spot nodes and the six requested tenors. The observer executes the exact source for base and stressed zero prices. For the supplemental stresses, parallel adds 50 bp throughout; steepening adds 0 to 100 bp from years one to five, and flattening adds 100 to 0 bp across the same interval. Intermediate shifts vary linearly with tenor. Neither the source nor this project bootstraps market data.
