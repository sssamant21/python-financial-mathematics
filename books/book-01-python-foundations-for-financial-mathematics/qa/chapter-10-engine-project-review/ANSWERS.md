# Section 10.14 — Local answers and project acceptance

| Prompt | Independent review | Evidence |
|---|---|---|
| 1. Record | Period 0, amount −100; an immediate outflow | Exact source record |
| 2. Ordinary | 50 at periods 1, 2, 3 | Source schedule and rational valuation |
| 3. Due | 50 at periods 0, 1, 2 | Source schedule and rational valuation |
| 4. Deferred | ordinary(50,3,4) gives periods 4, 5, 6 | Source schedule and rational valuation |
| 5. Growing | 100, 105, 441/4 at periods 1, 2, 3 | Source schedule and rational valuation |
| 6. NPV call | value_at(flows,.1) with default period zero | Exact source and independent sum |
| 7. Horizon call | value_at(flows,.1,5) | Exact source and independent sum |
| 8. Reconciliation | V(5)=V(0)×(11/10)^5 with constant rate | Rational benchmark and source value |
| 9. Worked NPV | −100+600/11+6000/121=500/121≈4.13 | Exact source demonstration and rational sum |
| 10. One-period IRR | 110/100−1=0.10 | Source root and independent residual |
| 11. Multiple IRRs | −100(x−1.1)(x−1.2)=0 with x=1+r | Separate source brackets and residuals |
| 12. Date scope | Calendar dates require a date-aware convention; this engine takes integer periods | Conceptual boundary and source rejection |

The two-period worked IRR follows from 100x²−60x−60=0, hence r=(√69−7)/10. Rate units must match the payment periods. The first generated growing payment is the supplied amount, not the amount after one growth step. A later horizon accumulates earlier payments and discounts any still-later ones.

| Project criterion | Scoped disposition |
|---|---|
| 1. Typed signed record | Executed valid initial outflow and invalid period/record paths |
| 2. Schedule timing | Executed ordinary, due, deferred and growing dates and amounts; due is one period earlier than ordinary |
| 3. Value at an explicit period | Executed time zero, periods one and five, repeated dates and signed flows |
| 4. PV/FV identity | Independent rational reconciliation against exact source |
| 5. Bracketed IRR | Executed endpoints, separate roots, no bracket, scaled stream and identically zero NPV; checked independent residuals |
| 6. Repeatable tests and assumptions | Both commands passed with raw outputs retained; limitations reviewed conceptually |

Checklist requirements for complete real transaction data, per-period rate documentation, application-specific range limits and independent acceptance remain external to these fixtures. The proposed dated-cash-flow, rounding, scenario and CSV extensions are design ideas only; none was added or executed.
