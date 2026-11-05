# Section 10.11 — Twelve local answer records

| Prompt | Independently reviewed answer | Evidence |
|---|---|---|
| 1. Why not level annuity | Arbitrary dates or amounts cannot be represented by equal payments at regular intervals | Conceptual contract |
| 2. Negative flow | An outflow from the selected perspective | Conceptual sign convention and exact time-zero value |
| 3. Actual/365 Fixed | Actual calendar-day difference divided by the fixed denominator 365 | Conceptual rule and verified offsets |
| 4. 365 days | 365/365=1 | Calendar count and one-year source discount |
| 5. 366 days | 366/365, even across a leap year | Calendar count and 100-digit Decimal PV benchmark |
| 6. 110 one year later | 110/1.1=100 | Exact source and rational value |
| 7. Time-zero receipt | 100 | Exact source |
| 8. Time-zero outflow | −100 | Exact source |
| 9. Ordering | Mathematical PV is invariant; finite precision and range limits apply | Source reordered and generator fixtures versus independent sum |
| 10. Repeated date | 10+20=30 at the same date; when one year later the PV is 300/11 | Source separate/consolidated flows and rational sum |
| 11. Zero rate | Sum signed amounts; worked stream sums to 150 | Exact source and integer sum |
| 12. Review controls | Verify date/anchor, currency, signs, rate, day count and transaction completeness | Conceptual audit, not external data validation |

The worked offsets follow from 31+28+31+14=104 days to April 15, 304+29=333 to November 30, and 365+31+28=424 to the following March 1. The lab defaults to the earliest date; an earlier or later explicit anchor changes the offsets, not the payments. A pre-anchor flow has a negative year fraction and is accumulated to the anchor. Empty schedules are not a substitute for missing production data.
