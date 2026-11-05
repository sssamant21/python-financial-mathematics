# Section 8.9 — Worked answer review

| Prompt | Reviewed answer | Evidence |
|---|---|---|
| 1. Call at 103 | Per-unit payoff is max(103−100,0)=3. One contract with multiplier 100 pays USD 300; subtracting USD 600 initial premium gives simplified profit USD −300. | Exact source and rational oracle |
| 2. Strike | At 100 the call has zero terminal payoff, so simplified profit is −600 USD. Strike is the kink, not break-even after premium. | Exact source |
| 3. Premium eight | Break-even is 100+8=108 with no carry. Raising premium by two per unit lowers per-position profit by USD 200; payoff is unchanged. | Exact source alternate premium |
| 4. Put at zero | Payoff is (100−0)×100 = USD 10000; subtracting USD 400 gives simplified profit USD 9600. | Full scenario oracle |
| 5. Multiplier ten | Monetary payoff, premium cost and simplified profit become one tenth as large. Strike and per-unit break-even coordinates do not change. | Exact source alternate multiplier |
| 6. Kink | Connecting call payoff at 90 and 110 implies per-unit payoff five at 100, whereas the true payoff there is zero. Include the strike to retain the piecewise-linear kink. | Supplemental midpoint arithmetic and plotted grid |
| 7. Terminal identity | max(S−K,0)−max(K−S,0)=S−K holds for each supplied scenario. It is a per-unit terminal algebraic identity, not a present-price relation or a probability model. | Exact source per-unit calculation |
| 8. Before expiration | A terminal payoff chart does not price an option one month earlier. That requires a separately specified valuation model, appropriate inputs and validation. | Conceptual scope review |
