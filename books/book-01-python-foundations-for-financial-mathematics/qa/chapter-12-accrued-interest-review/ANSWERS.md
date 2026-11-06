# Section 12.8 — Answer and project mapping

| Prompt | Review |
|---|---|
| 1–4 | A clean quote excludes accrual. In consistent currency units dirty = clean + accrued, and clean = dirty − accrued. |
| 5 | 1,000 × 0.06 / 2 = 30. |
| 6 | Explicit month lengths sum to 181 days. |
| 7 | January, February and March total 90 days in 2026. |
| 8 | The worked fraction is 90/181. |
| 9 | 30 × 90/181 = 14.917127… . |
| 10 | 1,020 plus the unrounded accrual displays as 1,034.92. |
| 11 | The period start has zero elapsed days and zero accrual. |
| 12 | 2,000 × 0.08 / 4 = 40. |
| 13 | Supplemental conversion: 101.25 / 100 × 250,000 = 253,125. |
| 14 | Converted clean holding value plus 3,750 = 256,875. |
| 15 | Actual/360 uses 90/360, not 90/181 here. This is a convention comparison, not an alternate pricing implementation. |
| 16 | Conceptual: discounted remaining flows at settlement are compared to full price under matched conventions. |
| 17 | Conceptual: round at settlement as prescribed by the contract; this lab reports unrounded floats. |
| 18 | The next coupon starts a new accrual period. Tested exclusion from the old period and reset in the new one. |

Run and compile the named standalone listing. The runner checks all project columns or their numeric inputs for elapsed days 0, 31, 90, 151 and 180, with the same 181-day denominator. It reconstructs clean 1,020 from reported dirty and accrual within tolerance for each. Calendar dates, not timestamps, are required. The scope excludes irregular periods, quote dissemination and actual settlement rules.
