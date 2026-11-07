# Section 16.3 — scoped portfolio-return lab and answer review

Baseline manuscript: `625dd60efdc301f75bf4328d45c076081ab465e7`. One core workflow, 24 local answers and twelve lab-step records reviewed. Predicate, workflow, answer and historical unique method counts remain separate.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-return-review/review.py
```

The observer extracts the single exact Python fence, runs the printed demonstration and twelve existing unittest methods, verifies silent import and runs the printed compilation command in isolation. Three commands and 49 supplemental predicates pass in `results.json`; no historical unique methods added. Python/platform, raw outputs, hashes, independent references/tolerances and project outputs are retained.

`baseline.json` preserves sixteen failed predicates against the unchanged baseline source above, reproducible with this runner/source revision. All twelve existing methods originally passed. After numerical correction, `reference-test-transition.json` retains the first rerun where all 49 numerical predicates passed but one embedded method failed: test_03 had hardcoded −.020000000000000004 instead of the mathematically expected −.02 contribution. Under the now-declared displayed-decimal input policy, [.6,.4]×[.1,−.05] reports [.06,−.02]. Only that expected value was corrected; the same twelve historical methods then passed. Restoring its old expected list in corrected source reproduces the retained transition. This is distinct from the original source's numerical/contract failures and is not a new test method.

F144 corrects tiny/integer NAV returns disappearing, overflow before net-return cancellation, tolerated weight-budget residuals producing spurious zero-market gains, rounded gross growth erasing tiny gains, oversized intermediate wealth becoming NaN even before an eventual true bankruptcy, inconsistent contribution return-domain validation and invalid policy flags. Accepted near-one weights are now explicitly normalized to exact unit budget for return/wealth computations; the validator itself preserves declared inputs and rejects invalid budgets. Rational intermediate arithmetic uses integer/displayed-decimal float inputs; nonzero unreportable outputs and nonzero ending wealth falsely rounded to total loss raise ValueError.

Terminal total depletion is allowed. Further periods after depletion are rejected by both engines. Buy-and-hold leaves extinct positions at zero; constant-mix refuses to restore a positive target in an extinguished asset before another period without an explicit replacement policy. Both engines remain cost-free and long-only; the signed one-period exposure function does not model funding/collateral. Individual contribution fields must each be reportable, even when an offsetting net return is reportable. Educational conventions only, not binary-float compatibility, execution feasibility or independent acceptance.

## Independent benchmarks and all local answers

References use exact rational weighted sums, beginning/end position values and wealth ratios. For initial [.5,.5], period 1 [.2,0] gives positions [.6,.5], then period 2 [0,.2] gives [.6,.6]. Therefore buy-and-hold period returns are [1/10,1/11], terminal wealth 6/5 and final weights [.5,.5]. Constant mix restores [.55,.55] between periods: returns [1/10,1/10], terminal wealth 121/100. These are independently derived accounts, not another full implementation of the path functions.

| Answers | Review and source boundary |
|---|---|
| 1–5 | Source weighted .04, contributions .06/−.02, equal-weight zero, zero-allocation zero and signed exposure .11 checked. |
| 6–10 | Price .10 and simplified dividend-inclusive .07 independently derived; source no-flow NAV return .04 checked. External deposit rejected by source, since timing-adjusted performance is not implemented. 5% gross less 1% of initial NAV cost gives 4% only under the stated period-end additive convention. |
| 11–15 | Source drift 11/21,10/21, partial loss −.5 and compounded .1/−.1=−.01 checked. Arithmetic mean zero and geometric √.99−1 are separate mathematical derivations; no geometric-mean function is exported here. |
| 16–18 | All source two-period path returns, cumulative .20/.21 and final BH weights checked; difference .01 is a path-specific percentage-point difference. |
| 19–20 | Beginning weights required; explicit cash scenario below checked. Cash zero-return assumption is nominal, not risk-free certification. |
| 21–23 | FX 1.1×.95−1=.045 independently derived; nonzero external flows rejected; $1/$1000=.001 return cost under specified end timing. No FX feed, time-/money-weighted flow engine or real cost reconciliation executed. |
| 24 | Appropriate tolerance and explicit rounding reviewed. Underflow/nonfinite/depletion cases now have recorded error contracts; these probes are not exhaustive branch proof. |

The value_return helper uses a positive starting NAV and a finite ending NAV; it is an algebraic no-flow return, not a margin/solvency approval. Asset-return rows retain the modeled unlevered simple-return floor −1. Other leveraged instrument P&L conventions require a separate specification.

## Twelve lab steps and timing/cost contracts

| Step | Executed evidence and limit |
|---|---|
| 1–3 | Initial [.5,.5], aligned rows [[.2,0],[0,.2]], source period-1 return .10. Synthetic period labels, real dates unavailable. |
| 4 | First-period values [.6,.5] imply weights [6/11,5/11]. Equal-weight .1/0 drift exercise is separately checked as [11/21,10/21]. |
| 5–6 | Source BH period-2 return 1/11 and cumulative .20 checked; compounding reconciles to final wealth 1.20. |
| 7–8 | Source constant-mix returns [.10,.10], cumulative .21; pre-cost difference .01 for this constructed path only. |
| 9 | Supplemental cost account funds fees between periods. Equal-target trade absolute notional=.10 of initial unit wealth; at rate c, post-rebalance wealth=1.10−.10c and terminal=(1.10−.10c)×1.10. For c=0,.001,.10, net cumulative returns are .21,.20989,.199. The last rate is an intentionally extreme sensitivity, not a realistic fee recommendation. Source value_return confirms each independently derived terminal account; source path engines are not claimed fee-aware. |
| 10 | Period-1 observations assumed available before between-period rebalance, with period 2 starting after it. Actual source release, fills, latency, lots, taxes and liquidity unverified. |
| 11 | Separate cash weights [.45,.45,.10], cash return zero and corresponding 3-column rows give source BH .18 and constant mix .1881. Full initial budget includes cash. |
| 12 | Input hash, units, policy, source/listing hashes, runtime, outputs, original failures and test transition retained. Corrected revision is the containing commit. |

Prerequisites: Python sequences/functions, beginning value weights, total-return/FX conventions, no-flow account assumptions and feasible rebalancing. Source function execution is separated from rational reference accounts, supplemental cost/cash designs and conceptual timing/funding review. No real trades, venue operations, external feed, margin or portfolio suitability accepted. Standard library only.

## Limits and resume checkpoint

Scoped local Linux CPython only. F28 notebook/platform, F32 broader shared-input integration and other unresolved findings remain open. No external-platform run, exhaustive proof, independent reviewer acceptance, actual trading or certification. Chapter 16 now records three workflows and 72 local answers reviewed. Next: Section 16.4 — Expected Portfolio Return.
