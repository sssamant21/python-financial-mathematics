# Section 8.10 — Worked answer review

| Prompt | Reviewed answer | Evidence |
|---|---|---|
| 1. Simple year ten | 1000×(1+0.05×10) = USD 1500. | Exact source and rational expectation |
| 2. Annual recurrence | Each credited annual balance is its predecessor multiplied by 1.05. No intermediate cent rounding is modeled. | Exact source recurrence comparison |
| 3. Effective annual rate | Monthly nominal 5% yields gross annual factor (1+0.05/12)^12. Its annual rate is approximately 5.116190%, because interest is compounded during the year. | Independent high-precision computation |
| 4. Equivalent rates | Monthly nominal rate 12×(1.05^(1/12)−1), approximately 4.888949%, gives the same 5% effective annual growth. The common year-end balances agree within tolerance; credited intra-year states can differ. | Decimal reference and source comparison |
| 5. Credited state | At half a year annual frequency has not completed a whole credit period. Monthly frequency has completed six; its balance is 1000×(1+0.05/12)^6. | Source rejection/acceptance and rational six-period reference |
| 6. Log scale | Display scale changes, not the monetary balances or terminal value. Both panels use identical arrays. | Exact artists |
| 7. Negative simple rate | The factor 1+r×t may reach zero or become negative. At r=−0.5 and t=2 it reaches zero and the helper rejects the path under its strictly positive contract. | Exact source rejection |
| 8. Forecast scope | Probabilistic uncertainty requires a separate model, data, horizon and validation. The deterministic curves contain no distribution from which to infer a confidence band. | Conceptual review |
