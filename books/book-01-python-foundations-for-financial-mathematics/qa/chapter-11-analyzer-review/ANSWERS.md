# Section 11.13 — Worked answers and project acceptance

| Prompt | Review |
|---|---|
| 1. Rate | Nominal 0.06 / 12 = 0.005 per month, the rate used by the demo. |
| 2. Count | 30 × 12 = 360 baseline periods. |
| 3. Formula | Divide principal by the sum of periodic discount factors; the answer now states the zero-rate branch too. |
| 4. Zero rate | 1,200 / 12 = 100. Checked on every source row. |
| 5. Interest | 240,000 × 0.005 = 1,200 before applying payments. |
| 6. Extra | With 200 extra, the first uncapped payment displays as 1,638.92. |
| 7. Savings | Baseline interest less accelerated interest gives 85,085.34 from unrounded totals. |
| 8. Periods | 360 − 265 = 95 payments saved. |
| 9. Payment identity | Interest plus principal equals paid amount; every reference row agrees. |
| 10. Balance identity | Opening less principal equals closing, verified against the recurrence. |
| 11. Payoff | The model closes at zero; tolerance applies to arithmetic on reported floats. |
| 12. Refinance | At equal term and principal, the lower rate reduces the modeled installment from 1,432.86 to 1,265.30. |
| 13. Break-even | 3,000 / 100 = 30 periods under constant savings. The actual project fixture yields 18. |
| 14. Limits | Conceptual: simple break-even ignores discounting and residual balances. The capstone does not implement common-horizon PV. |

The six phases use a standalone script and a fixed monthly rate. Phases A and B generate baseline and accelerated schedules; C audits both; D calculates an intermediate balance; E compares the stated cash-fee refinance scenario; F runs the tests. The README and JSON retain command and output evidence.

| Acceptance record | Evidence |
|---|---|
| Standard payment | Direct discount sum and full baseline rows. |
| Zero interest | Twelve equal principal payments. |
| Baseline | 360 rows and zero final balance. |
| Extra payments | 265 rows, smaller interest total and capped payoff. |
| Row composition | Reference schedule, valid audit and malformed composition rejection. |
| Continuity | Every opening and closing checked against the recurrence. |
| Principal | Source audit and exact reference principal sum. |
| Outstanding balance | 60-period recurrence, first-period existing test, endpoints. |
| Refinance | Independent payments, savings and ceiling. |
| Invalid inputs | Range, extra start and audit mutation probes. |
| Unit tests | Twelve existing tests in the exact listing. |
| Compilation | Documented compile command on the extracted script. |
