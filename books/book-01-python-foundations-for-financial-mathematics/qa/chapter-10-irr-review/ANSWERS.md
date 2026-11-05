# Section 10.13 — Twelve local answer records

| Prompt | Independently reviewed answer | Evidence |
|---|---|---|
| 1. Definition | IRR is a periodic r>−1 such that the signed-flow NPV is zero | Conceptual |
| 2. One period | 110/100−1=0.10 | Source and exact rational root |
| 3. Negative root | 90/100−1=−0.10, with a bracket including the negative rate | Source and exact rational root |
| 4. Zero root | 100/100−1=0 | Source low-endpoint root |
| 5. Two periods | Set x=1+r; 100x²−60x−60=0 gives r=(√69−7)/10≈13.07% | Source and 100-digit Decimal benchmark |
| 6. Bracket | Opposite nonzero signs or an endpoint root | Conceptual and source endpoint checks |
| 7. Missing sign change | No general no-root conclusion: −100x²+220x−121=−100(x−1.1)² has a tangent root | Exact algebra and source rejection of the bracket |
| 8. Multiple roots | −100x²+230x−132=−100(x−1.1)(x−1.2); r=0.10 and 0.20 | Exact algebra, separate source brackets and residuals; broad bracket rejected |
| 9. Rate versus value | IRR solves for a rate; NPV reports currency at a chosen rate | Conceptual |
| 10. Monthly rate | (1+r_month)^12−1; 1% monthly gives about 12.68250% annual effective | Supplemental exact rational arithmetic |
| 11. Exclusive projects | Absolute modeled value can be more informative than percentage return when scale/timing differ | Conceptual |
| 12. Validation | Check residual, domain, bracket, rate tolerance and alternative roots | Independent residuals and documented solver limits |

The first amount is time zero and subsequent elements are equally spaced. The bracket contract is not an exhaustive root-discovery algorithm. Rate tolerance and currency residual are separate diagnostics.
