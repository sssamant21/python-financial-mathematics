# Section 9.1 — Worked practice review

| Prompt | Reviewed answer | Evidence |
|---|---|---|
| 1. Three years at 4% | The factor is (26/25)^3. Future equivalent is 2000×(26/25)^3 = 2249.728; dividing the full result by the same factor returns 2000. Display 2249.73 only after calculation. | Exact source and rational oracle |
| 2. Common-date offers | 500×21/20 = 525, so the two claims are equivalent under the model. Different default, liquidity, currency or tax assumptions require another model; the arithmetic alone does not decide a practical investment choice. | Source plus conceptual assumptions |
| 3. Negative rate | Forward equivalent is 1000×49/50 = 980. Present equivalent of a future1000 is 1000÷(49/50) ≈ 1020.408163, larger than1000. | Exact source and rational oracle |
| 4. Rate units | Input5 means500%, giving gross factor6; .05 means5%, giving1.05. The numeric validator cannot infer the author's intended units. | Exact source with both numeric inputs |
| 5. Monthly periods | A term of two years must be expressed as24 model months before using a monthly effective rate in this whole-period model. An annual quote needs a separate conversion convention; actual date/day-count treatment is outside this helper. | Contract/units review only |

The original worked offer comparison is also reconciled: A gives1102.50 at year2 while B is1080, or B discounts to1080/(21/20)^2 ≈979.591837 today versus A's1000. The separate inflation example is1050/(51/50) ≈1029.411765 in today's purchasing-power units; discounting1050 at5% gives financial present value1000. Neither is an extra cash flow.
