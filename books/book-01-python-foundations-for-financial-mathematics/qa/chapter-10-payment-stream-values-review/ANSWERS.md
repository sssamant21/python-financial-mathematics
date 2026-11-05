# Section 10.10 — Twelve local answer records

| Prompt | Independently reviewed answer | Evidence |
|---|---|---|
| 1. General PV | Signed amount × (1+i)^(−t) | Source single dated payment and exact rational benchmark |
| 2. Horizon value | Signed amount × (1+i)^(T−t), including discounting if T<t | Source at three horizons and rational values |
| 3. Time zero | −500 is unchanged | Exact source |
| 4. Ordinary dates | 1,2,3 | Source generated pairs and direct sum |
| 5. Due dates | 0,1,2 | Source generated pairs and direct sum |
| 6. Deferred dates | d=2, n=3 gives 3,4,5 | Source generated pairs and direct sum |
| 7. Repeated date | 75/1.1=750/11≈68.18 | Exact source and rational value |
| 8. Zero rate | 100+200=300 | Exact source; dates still validated |
| 9. Negative rate | 100/0.9=1000/9≈111.11 | Exact source and rational value |
| 10. Mixed stream | −500+200/1.1+400/1.1³=−23500/1331≈−17.66 | Source demonstration and rational sum |
| 11. Reconciliation | V(3)=−23.50, also PV×(11/10)³ | Exact source and both rational expressions |
| 12. Audit | Generate dated payments and compare an individually discounted sum with the closed form | Conceptual audit procedure and executed exact timeline versus rational sum |

The lab takes (period, amount) pairs even when the prose introduces a payment before naming its date. Repeated dates need not be consolidated. Horizon and payment dates are nonnegative integers and rate units must match the date units. Valuation is deterministic and does not itself decide whether a project should proceed.
