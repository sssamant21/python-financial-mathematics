# Section 16.13 — scoped mandate feasibility and answer review

Baseline manuscript: `9b91f08a557c5eee6c10596fa5420b77ae97cbfb`. One core workflow, all 30 local answers and twelve lab steps reviewed. Predicates, workflows, answers and historical unique methods are separate inventories.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-constraints-review/review.py
```

Reproduce unchanged-source failures (requires baseline in Git history; intentionally exits nonzero and writes `baseline.json`):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-constraints-review/review.py 9b91f08a557c5eee6c10596fa5420b77ae97cbfb
```

The observer extracts the exact Python reference fence, runs its printed demonstration and twelve existing unittest methods, checks silent import and executes printed compileall in isolation. Final `results.json`: three successful commands, 51 passing supplemental predicates, hashes, runtime/platform, raw output and independent rational references/comparison tolerances. No new historical unique methods.

## Baseline and corrections

`baseline.json` retains 15 failed predicates against unchanged source; all twelve original methods already passed. F154 corrects Exercise15's factor-of-two cost error, default tolerance acceptance of small real position/group/turnover/independent-bound breaches, integer expectation/cancellation loss, intermediate product overflow, nonzero output underflow, malformed group/name exception contracts and unreportable gross-exposure handling. Two failing probes labelled `policy extension` add explicit approximate-rule control and recorded budget residual; the old API did not expose those features. These are scope extensions rather than failures of a previous explicit interface guarantee. No observer crash or failed corrected-source transition occurred here.

Exercise15 quoted a .002 cost rate on traded notional but returned .0002 NAV, contradicting Section11's `Cost=2*c*T` convention. The corrected answer is `2*.002*.1=.0004` NAV, four basis points: total buys plus sells=.2 NAV when one-way turnover=.1. The observer checks source answer text alignment and independently derives the fee using the exact-source turnover. This is a supplemental fee calculation, not an exported source cost function, trade engine or realized cost estimate.

Default rule tolerance is zero. Optional finite nonnegative `tolerance` explicitly relaxes position/group/turnover and independent-bound comparisons. Budget admission separately defaults to 1e-10 and is recorded with the actual residual; weights are audited as supplied, not normalized. A near-unit budget does not erase an individual strict breach. A positive tolerance means approximate feasibility under that numerical policy, not permission to alter an actual mandate.

Integer/displayed-decimal rational intermediates retain sums, thresholds, trade differences and cancellation; required float outputs must stay finite and preserve nonzero exact values or raise ValueError. Internal vectors retain rational values. Group containers/names/indices have explicit schema checks before use; overlaps across named groups are intentional, duplicate members within a group are not. General expected-return/gross helpers do not themselves establish investment feasibility.

## Independent mathematics and all 30 answers

The observer derives budgets/exposures and thresholds by rational sums, turnover as half the exact L1 difference, fees as rate times total traded notional, and expectation as rational products. Constraint classification comes from exact inequalities for the explicit proposal/reference. Joint disjoint-group contradiction is a supplemental algebraic proof, not a source joint-feasibility solver.

| Answers | Review and executed boundary |
|---|---|
| 1–6 | Supplemental budget1; source asset-cap/floor and group-floor/cap checks. Position .7 against .6 exceeds by .1, .05 against .1 falls short .05, equity exposure .8 exceeds .7 by .1 while satisfying floor.5. |
| 7–9 | Source general gross([1.2,−.2])=1.4; supplemental net1; source long-only proposal audit rejects signed allocation. Gross is not margin or derivative-equivalent risk. |
| 10–12 | Source independent-bound screen rejects lower sum1.2 and upper sum.8, accepts [0,0]/[.6,.6]. Exact default is necessary and sufficient only for independent valid long-only bounds and budget; it is not a joint solver. |
| 13–15 | Source one-way turnover .1 and .05-cap breach; supplemental violation .05 and corrected cost .0004 NAV at .002 per total traded notional. Source exports no cost function. |
| 16–20 | Source expected return .059; supplemental return-floor gap .001, liquidity excess .1, cash shortfall .03 and gross-limit excess .2. Expected-return/liquidity/cash/gross examples are arithmetic/design records, not additional checker limit types. |
| 21–23 | Source overlapping groups [A,B] and [A,C] give .8 and .7 independently. Look-through issuer overlap remains conceptual. Supplemental simplified duration=.5*2+.5*8=5 years; no duration/issuer exposure engine exported. |
| 24–27 | Carbon metric/vintage, integer lots, cardinality and covariance-dependent contribution limits reviewed conceptually. No metric feed, integer/mixed-integer solver, cardinality or covariance risk-limit implementation. |
| 28 | Source independent bounds can pass while a proposal fails disjoint group floors .7/.7. Their sum1.4 proves joint impossibility under budget1, separately from source checking one proposal. |
| 29–30 | Drift breaches require mandate-governed action/exception; deposits need trade-only turnover separate from external flows. No actual mandate exception, trade, external-flow accounting or monitoring service created. |

## Twelve lab-step contracts

Prerequisites: synchronized common-NAV proposal/reference weights, nonnegative independent bounds, named integer-index groups, one-way turnover convention and feasibility versus optimization. Fixture has fictional A/B/C in common USD at synthetic t0, no actual dates/classification provenance, no external flows/trades/cost execution.

| Step | Result and source boundary |
|---|---|
| 1–2 | Proposal [.5,.3,.2], explicit asset order and unit budget. Budget residual recorded; near-unit residual probe is not silently normalized. |
| 3–4 | Lower [0,0,0], upper [.6,.6,.4], strict default long-only/position rules; original proposal passes and [.7,.2,.1] violates A maximum. |
| 5–6 | Equity indices [0,1], exposure .8, group bounds [0,.85], source passes. |
| 7 | Cap tightened to .7: source records equity violation, independent excess .1. This is a synthetic alternate mandate, not a change to an actual account rule. |
| 8–9 | Reference [.4,.4,.2], source turnover .5*(.1+.1+0)=.1. Common NAV/no external flow assumptions explicit. |
| 10 | Turnover limit .1 passes; .05 fails. Supplemental symmetric traded-notional fee=.0004 NAV at c=.002; one-way rate quoting would be a separate convention, not assumed here. |
| 11 | Source lower [.6,.6]/upper [.8,.8] screen rejects. Separate overlapping/disjoint group examples illustrate scope and joint conflict without a solver. |
| 12 | Labels, bounds, group definition, synthetic mandate-version placeholder, tolerances, input/listing/source hashes, raw output/runtime retained. Corrected source revision is containing commit. No actual exception approval or live mandate integration. |

## Limits and resume checkpoint

Local Linux CPython standard library only. Source checks/helpers are separate from supplemental fee/gap/duration formulas and conceptual governance/optimization designs. No joint-feasibility/optimization, actual classifications/look-through, as-of NAV/FX, covariance risk or tracking error, integer execution, external-flow turnover, production monitoring, platform coverage, independent reviewer acceptance or certification. F28 notebook/platform, F32 broader shared-input integration and newer unresolved findings remain open.

Chapter16 now records thirteen core workflows and 366 local answers within scope. Next: Section16.14 — Rebalancing Mathematics.
