# Project 19 — Liability Cash-Flow Matching and Funding-Gap Stress

**Business question:** Can a hypothetical fixed-income cash-flow schedule cover promised annual liabilities, and how sensitive is the discounted funding gap to assumed interest rates?

This lab is different from Project 15 (bond duration and convexity): it emphasizes **asset-liability cash-flow timing and funding sufficiency**, not bond price risk. All amounts are synthetic currency units. No market data, broker actions, or financial recommendations.

## Mathematics

For cash flow `C_t` at the end of year `t` and a constant annual effective discount rate `r >= 0`, `PV = sum(C_t / (1+r)^t)`. The discounted funding gap is `PV(assets) - PV(liabilities)`. A positive present-value gap **does not imply** that every year's liabilities can be paid: cumulative undiscounted balances reveal intermediate shortfalls.

The example assumes annual periods, a single nonnegative flat discount rate, deterministic promised cash flows, no reinvestment interest, no defaults, no taxes, no inflation and no financing. This is **not** a self-financing immunization strategy or a duration-matched hedge.

## Reproduce

Requires Python 3.11+ standard library only (no additional dependencies).

```bash
cd quant-projects/19-liability-cashflow-matching
python cashflow_matching.py
python -m unittest -v test_cashflow_matching.py
python -m compileall -q cashflow_matching.py test_cashflow_matching.py
```

The seeded-free fixture has assets of 600 each year for three years and liabilities of 500, 650 and 550. It prints cumulative annual balances and funding gaps under predeclared 2%, 4%, 6% rates. Results are hypothetical.

## Guardrails and validation limits

Inputs must have positive integer year keys (1–100), nonnegative finite cash amounts and nonnegative finite discount rates; empty schedules are rejected. The model reports negative cumulative balances instead of assuming financing is available. Tests cover discounting identities, exact matching, temporary shortfall, rate stress, invalid inputs and immutability.

Synthetic tests do not validate yield-curve construction, reinvestment, credit risk, liability uncertainty, real-world pension/insurance obligations, independent review, or production readiness. No third-party market data is bundled.

**Next:** add constrained cash-flow matching using predeclared synthetic bond candidates, an explicit feasibility diagnostic and out-of-sample interest-rate stress; avoid presenting solver outputs as actionable allocations.

## Constrained integer-lot extension

A finite set of hypothetical bond cash-flow candidates has a purchase cost, annual promised cash flows, and a maximum available number of whole lots. The model chooses the **least-cost feasible combination** under a budget and the requirement that cumulative undiscounted cash receipts cover liabilities at each due date. If no combination satisfies every constraint, it reports infeasibility and the smallest maximum cumulative shortfall among budget-admissible combinations (not a recommended trade).

Mathematically, minimize `sum(cost_i * lots_i)` with `lots_i` nonnegative bounded integers, `sum(cost_i * lots_i) <= budget`, and for every liability year `t`, `sum_{s<=t} (asset_receipts_s - liabilities_s) >= 0`. This enumerative solver is deliberately capped at 100,000 combinations, with deterministic tie-breaking; it is **not** a scalable mixed-integer optimizer. No fractional holdings, borrowing, defaults, inflation, reinvestment interest or trading are modeled. Zero-coupon-like synthetic fixtures are not market quotes.

```bash
cd quant-projects/19-liability-cashflow-matching
python constrained_matching.py
python -m unittest -v test_cashflow_matching.py test_constrained_matching.py
python -m compileall -q cashflow_matching.py constrained_matching.py test_cashflow_matching.py test_constrained_matching.py
```

The synthetic example requires one short and one long lot at a total purchase cost of 185 units to cover 100 units due in each of years 1 and 2. Budget 180 is infeasible. Fixed-holdings 2%, 4%, 6% parallel-rate stress changes **discounted** cash-flow gaps only; it does not change contractual payments or solve for new holdings. Actual bond price changes, issuer risk, liquidity and stochastic liability changes are not modeled. The deterministic fixture has matching asset/liability flows, so its PV gap is zero at every tested rate. This is educational model validation, not independent review or production certification.
