# Section 9.16 — Eight local answers, static scope

All eight prompts were reviewed against the current source and independently derived mathematical expectations. Python source calls remain unexecuted. Exact benchmark fractions and thirty-place truncated decimals are in [benchmarks.json](benchmarks.json).

| Prompt | Reviewed answer and contract | Evidence status |
|---|---|---|
| 1. Monthly accumulation | 1000 × (201/200)^24 = 1127.159776205391741…; displayed 1127.16 USD. The quote is 6% nominal annually with frequency 12 and time 2 years. | Supplemental exact BigInt rational derivation executed; Python pending |
| 2. EAR | (201/200)^12−1 = .061677811864499568… = 6.1677811864499568…%; 6.1678% rounded as printed. | Supplemental exact rational derivation executed; Python pending |
| 3. Break-even NPV | −1000+1100/(11/10) = 0 exactly; frequency 1 makes the annual nominal input equal the stated EAR. Both events must be supplied, including cost at time zero. | Supplemental exact rational derivation executed; Python pending |
| 4. Reverse rate | (1210/1000)^(1/2)−1 = .10 annually. Positive growth factor and positive two-year horizon select the admissible root. | Exact square identity executed; source inverse pending |
| 5. Reverse time | (11/10)^2 = 121/100, hence two years; a strictly positive nonzero rate gives a unique time for these balances. | Exact integer cross-product executed; source solver pending |
| 6. Frequency zero | Convention must reject frequency 0. Source checks frequency <= 0 before division. The answer is aligned. | Static branch review; exception probe pending |
| 7. Same-date audit | Three distinct rows retain amounts −100, +40, +60 at year zero; discount factor is mathematically 1 for each and total NPV is 0. Aggregating away rows would violate the audit requirement. | Exact net executed; row preservation/source floating tolerance pending |
| 8. Day-count extension | Store valuation date, payment dates, named day-count convention and compounding schedule. Define date validation, calendar/timezone policy where relevant, and stub/credit rules before converting to years. | Conceptual design only; no scheduling implementation |

The demonstration's four CSV events at 8% nominal monthly have independently derived total NPV 31.819158817370702…; its per-event exact rational PVs are retained. This is distinct from the zero-NPV practice fixture. The source's log-space scaling may incur float rounding; the proposed runner uses explicit tolerances rather than requiring exact zero for computed NPV. Amount signs, year units, flat rates, no hidden costs and absence of fees/taxes are consistent across the prose and formulas. None of these observations establishes market-model approval or runtime acceptance.
