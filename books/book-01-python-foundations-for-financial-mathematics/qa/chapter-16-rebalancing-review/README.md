# Section 16.14 — scoped rebalancing and post-cost accounting review

Baseline manuscript: `764d0ce9d3a12c8b23947772f9a6e37f3c6e6b5a`. One core workflow, all 30 local answers and twelve lab steps reviewed. Predicates, workflows, answers and historical unique methods are separate inventories.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-rebalancing-review/review.py
```

Reproduce unchanged-source failures (baseline must exist in Git history; intentionally exits nonzero and writes `baseline.json`):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-rebalancing-review/review.py 764d0ce9d3a12c8b23947772f9a6e37f3c6e6b5a
```

The observer extracts the exact Python reference fence, runs its printed demonstration and twelve existing unittest methods, checks silent import and executes printed compileall in isolation. Final `results.json`: three successful commands, 61 passing supplemental predicates, raw outputs, hashes, runtime/platform and independent rational/Decimal expectations and comparison tolerances. No new historical unique methods.

## Initial source failures and separate observer correction

`baseline.json` retains ten failed predicates against unchanged source; all twelve original unittest methods already passed. F155 corrects nonzero bisection floor costs at zero rate/no trade, lost tiny fees/returns, large-NAV arithmetic overflow, tolerated-budget phantom gains, exact band-equality false triggers, false −100% reporting with positive wealth, and unreportable/huge-input exception contracts.

`observer-failure.json` separately retains the initial QA KeyError traceback: the list of fee case results shadowed the predicate accumulator named checks. `observer-initial-report.json` preserves that malformed intermediate report; it is invalid as a predicate inventory and is not counted. Renaming the case list to fee_cases corrected the observer, after which baseline/final reports were regenerated. To reproduce the observer error in a throwaway copy, rename only the fee_cases list/append/report references to checks. This was not a manuscript failure and no complete baseline count was emitted before the traceback.

## Exact model and reporting policy

Normalized long-only current/target budgets define y=post-cost NAV/pre-cost NAV, satisfying `1−y=c*sum(abs(b_i*y−a_i))`. For 0≤c<1, residual `1−y−c*L1(y)` has slope in [−1−c,−1+c], so is strictly decreasing; endpoint residuals bracket a unique positive-y solution. Source enumerates breakpoints a_i/b_i inside [0,1] and solves the linear equation on each segment using rational arithmetic. This replaces a fixed 100-iteration dollar bisection with scale-free exact segment arithmetic. Zero rate or unchanged normalized allocation yields exactly zero cost.

The independent oracle uses 80-digit Decimal bisection of normalized cost for four ordinary two-/three-asset fee cases, including rate .9; this is algorithmically separate from source segment solving. Closed-form symmetric two-asset cases independently check zero/tiny and large-NAV fees. Portfolio return and holding expectations use rational algebra.

Inputs follow integer/displayed-decimal rational arithmetic. Accepted unit budgets within 1e-10 are normalized. Required float outputs must be finite and preserve nonzero exact values or ValueError is deliberate. Portfolio return is computed directly as sum(w*r); positive wealth that would round to a −100% return rejects rather than imply bankruptcy. Tiny separate return/fee fields can be nonzero even if much larger reported gross/post-cost NAVs round away those increments.

Source normalized weight outputs reconcile within 1e-12 of unit mass. Reported dollar-trade cash sums reconcile within 1e-12 times exact gross-trades-plus-fee scale (gross trades for frictionless plans). Exact rational accounting is not a claim that displayed floats retain every tiny fee increment against large holdings/trades. Cost API includes total_traded, so an unreportable gross amount rejects even if another field alone is finite. Absolute-band equality does not trigger; no hidden boundary tolerance is introduced.

## Independent mathematics and all 30 answers

| Answers | Review and executed boundary |
|---|---|
| 1–4 | Source initial 50/50, returns [.1,0] gives period return .05, gross1.05, ending weights [11/21,10/21]; scaled NAV105. |
| 5–6 | Source equal-zero/equal-.1 returns preserve [.4,.6] weights. |
| 7–10 | Separate source [.4,.6]→[.5,.5] at NAV100 gives buys/sells10 each, one-way turnover.1, total traded20. This differs from the drifted-NAV105 lab. |
| 11–13 | Source zero-rate fee exactly0 and NAV100. Supplemental pre-cost fee estimate .001*20=.02, approximate NAV99.98; post-cost target source case independently matches the full fee equation. |
| 14–17 | Source absolute-band breaches/nonbreaches checked including exact .55/.45 versus .5/.5 at band.05, which does not trigger. Supplemental relative deviation(.24−.2)/.2=.20 exceeds a .10 relative band; source exports only absolute-band trigger. |
| 18–20 | Deposits are external flows, cash dividends depend on reinvestment convention, and split alone does not alter market value. Conceptual records; no external-flow/dividend/corporate-action engine implemented. |
| 21–24 | Tax, spreads, nonlinear impact and frequency-versus-turnover reviewed conceptually. No tax calculation, spread/impact model or strategy-frequency backtest executed. |
| 25–27 | Threshold versus calendar timing, risk drift and policy-target changes reviewed separately. No live scheduler, risk engine or policy approval workflow implemented. |
| 28–30 | Source post-cost targets fund fees via net sales; leverage needs different NAV conventions; fair strategy comparisons need matched paths, information, flows and costs. No leveraged execution or out-of-sample strategy comparison accepted. |

## Twelve lab-step contracts and exact source chain

Prerequisites: consistent asset order/NAV, long-only unit weights, simple total returns≥−100%, positive ending wealth, no external flows/trades during the return period, one common proportional fee rate on total buys plus sells, continuous dollar trading and post-cost target convention. Fictional A/B, common USD, synthetic t0→t1 returns and t1-close fixed-value rebalance; no real price dates/fills supplied.

| Step | Result and source boundary |
|---|---|
| 1 | Initial NAV100, weights [.5,.5], dollar holdings[50,50]. |
| 2–4 | Source drift returns .05 and gross1.05; supplemental ending values [55,50], NAV105. |
| 5 | Source ending weights [11/21,10/21], rounded floats passed directly into source planning functions. |
| 6 | Source frictionless plan at NAV105/target50-50: sell2.50 A, buy2.50 B to reporting tolerance. |
| 7 | Source one-way turnover1/42≈.02380952381; gross frictionless traded5 USD. |
| 8–9 | Source fee equation at c=.001 gives fee .005, post-cost NAV104.995, trades[−2.5025,+2.4975], total traded5. Exact references use [55,50] holdings; small input/reporting rounding is within recorded relative tolerances. |
| 10 | Supplemental reconstruction from original holdings plus source trades yields [52.4975,52.4975]; sum104.995. Source cash/NAV/fee identities and independent Decimal fee oracle pass. |
| 11 | Source absolute band.05 does not trigger: maximum drift1/42≈.0238095. Cost plan is a counterfactual forced rebalance, not an order generated by this band policy. |
| 12 | Timing/fixture/cost labels, input/listing/source hashes, runtime/raw outputs and scoped rounding limits retained. Corrected revision is containing publication commit. No actual trades or independent acceptance. |

The band policy and forced cost-plan example are deliberately separated: under this fixture the band says do not trade, while the hypothetical plan shows accounting if a rebalance is otherwise authorized. No mandated action or real exception is inferred.

## Limits and resume checkpoint

Local Linux CPython standard library only. Source execution is separate from supplemental dollar-holding reconstruction, closed-form expectations, Decimal oracle and conceptual policy designs. No actual source dates/prices/NAV/FX, external flows, fills/lot sizes, taxes, market impact/settlement, strategy backtest, production monitoring/performance, platform coverage, independent reviewer acceptance or certification. F28 notebook/platform, F32 broader shared-input integration and newer unresolved findings remain open.

Chapter16 now records fourteen core workflows and 396 local answers within scope. Next: Section16.15 — Chapter Project — Portfolio Risk and Return Engine.
