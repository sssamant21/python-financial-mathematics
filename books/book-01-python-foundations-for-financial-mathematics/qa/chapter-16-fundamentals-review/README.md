# Section 16.1 — scoped portfolio-fundamentals lab and answer review

Baseline manuscript: `3bd554d420d7e3d60ca32b3e4b1a48d6f611858a`. Scope: one core workflow, 24 local answers and ten lab-step records, separate from predicates and historical unique methods.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-fundamentals-review/review.py
```

The observer extracts the single source fence unchanged, runs the printed demonstration and twelve existing unittest methods, verifies silent import and runs the printed compilation command in isolation. Three commands and 43 supplemental predicates pass in `results.json`; no historical unique methods added. Python/platform, raw output, source/listing hashes, rational expectations, tolerances and project outputs are retained. `baseline.json` preserves ten failed predicates against unchanged baseline source above, reproducible with the same runner and that revision. All twelve original methods already passed.

F142 corrects an allowed tuple/list combination raising TypeError, overflow/cancellation before reporting portfolio value or signed weighted return, intermediate totals/grown values overflowing before valid normalization, invalid tolerance/policy controls and silently erased positive allocations. Integer/displayed-decimal float inputs use rational intermediate arithmetic. Final nonzero unreportable values are explicit errors; ratios can remain reportable despite oversized intermediate totals. Checked weights preserve the declared values rather than silently normalizing. Absolute budget tolerance must be finite in [0,1), and long_only must be bool. Signed quantities/returns remain an illustrative exposure calculation, not a complete financing/margin model.

## Independent numerical expectations and all local answers

Benchmarks use exact rational position values, beginning-weight return decomposition and end-value reconciliation. They do not call a duplicate implementation of the source functions. Drift ratios derive independently from end values, rather than the source growth-expression path. The no-cost rebalance and funded-cost equation are supplemental designs; valuation of the resulting fractional-share holdings uses the exact source.

| Answers | Scoped review |
|---|---|
| 1–4 | Position definition, source value 350, weights [.6,.4] from [600,400], full investment checked. |
| 5–8 | Sum .9 rejected without cash; [.6,.3,.1] with explicit cash and equal weights checked; source weighted realized return .04. |
| 9–11 | Diversification depends on covariance, .9 position is concentrated, and [.7,.3] is long-only. Constraint validation executed; risk/issuer classifications conceptual only. |
| 12–13 | Signed [1.2,−.2] net=1, gross=1.4 independently summed; source signed return .11 for [.1,.05]. No financing/collateral acceptance implied. |
| 14–16 | Equal-weight drift [11/21,10/21] checked. Rebalance design below and source expected return .064 checked; expectation is not realized return or guarantee. |
| 17–18 | Correlation affects variance; end weights are not start weights. Mathematical/timing review, no covariance estimator or real execution-timestamp adapter in this section. |
| 19–21 | Split quantity/price reconciliation, FX gross-return identity and exclusion of contributions from performance reviewed conceptually. No actual corporate actions, FX feed or external-flow ledger supplied. |
| 22–24 | Leverage/funding, issuer cap and cash inflation/currency/credit considerations reviewed. No margin engine, risk-free acceptance or issuer policy enforcement claimed. |

The helper's deliberate bankruptcy boundary is retained: post_return_weights requires every asset return greater than −1, even for zero-weight positions. It does not implement extinguished-position or signed-leverage drift accounting. portfolio_return permits finite signed inputs under its stated exposure policy; no unlevered-return floor is inferred for all instrument types.

## Ten lab steps and prerequisite contracts

| Step | Executed evidence and limit |
|---|---|
| 1 | Starting quantities [6,8], prices [100,50], fictional USD, synthetic start/end labels; real dates unspecified. No external flows, dividends, FX or funding. |
| 2 | Independent values [600,400], source total 1000. |
| 3–4 | Source weights [.6,.4], budget sum one. Numeric vectors establish positional correspondence only. |
| 5 | Source return .04 for [.1,−.05]; end prices [110,47.5] produce source wealth 1040, independently reconciling start value×1.04. |
| 6 | Separate model expectations [.08,.04] yield source .064; realized .04 differs without implying forecast failure/calibration. |
| 7 | End values [660,380] imply drift [33/52,19/52], checked against source drift helper. |
| 8 | No-cost target [.6,.4]×1040=[624,416]; trades [−36,+36], target shares [312/55,832/95]. Source value of rounded fractional-share representation reconciles to 1040 within recorded tolerance. No trade executed. |
| 9 | Hypothetical cost .001×absolute traded notional must be funded. Solve V'=1040−.001(280−.2V'), giving V'≈1039.9279855971195 and cost=360/4999≈.0720144029. Independent exact budget identity checked; source valuation of target fractional shares reconciles. The naive no-cost turnover estimate .072 omits its own funding adjustment. No actual lot sizes, spreads, taxes or financing accepted. |
| 10 | Concentration, FX, flows, corporate actions and funding are recorded risks; real data unavailable. Hashes, runtime, source revision, units, original failures and output retained. Corrected revision is the containing commit. |

Prerequisites: Python sequences/functions, simple total-return conventions, positive price inputs, declared common valuation time/currency and exposure policy. Source computations are exact-fence executions; rebalance/cost solutions, metadata and independent fractions are supplemental. Market-data provenance, actual trading, margin/financing, taxes and economic suitability are conceptual/unexecuted. Standard library only.

## Limits and resume checkpoint

Scoped local Linux CPython only. F28 notebook/platform, F32 broader shared-input integration and other unresolved findings remain open. No external-platform run, exhaustive branch proof, independent reviewer acceptance, actual trading or certification. Chapter 16 now records one reviewed workflow and 24 local answer records. Next: Section 16.2 — Portfolio Weights.
