# Section 9.5 — Worked practice review

| Prompt | Reviewed answer | Evidence |
|---|---|---|
| 1. 1210 at10%,two years | PV=1210/(11/10)^2 =1000. Forward accumulation with the same full-precision factor returns1210. | Exact source and rational oracle |
| 2. Signed obligation | −2160/(27/25) =−2000 from the payer's viewpoint. It is an equivalent amount, not an automatically executed time0 purchase/payment. | Exact source and rational oracle |
| 3. Common-date equality | 1000 today and1210 in two years at10% are equivalent at either common date under the same assumptions. | Exact source and rational oracle |
| 4. Higher rate | For the same positive future amount and year3 date, raising the rate from4% to6% lowers PV. A fixed negative obligation moves toward zero instead; sign qualifications matter. | Exact source ordering and conceptual qualification |
| 5. Rounded inverse | Rounding4444.981793… to4444.98 discards information. Compounding that rounded amount gives a different result; using the unrounded output recovers5000 within tolerance. | Exact source plus explicit rounded comparison |

The worked5000 receipt uses factor(26/25)^3 and PV=5000/(26/25)^3. The4500-today alternative is larger by about55.018207 at time0 and61.888 at year3. Those differences have different dates. The wrong subtraction4400 grows to4949.4016, not5000. These are conditional equivalences, not product valuations or recommendations.
