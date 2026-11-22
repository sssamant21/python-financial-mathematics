# V10 — Section15.13 descriptive dependence, data conventions and cost assumptions

Executed source pin: `1a5045c7a3c39727737579534f7074051559aa64`. [Runnable review](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-dependence-diagnostics/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-dependence-diagnostics/review.py replay
```

**175 predicates pass twice with identical rows:**160 native mean/ACF/domain/overlap fields over32 finite mixture paths;eight population/conditional-diagnostic checks;three missingness-convention checks;two project raw/squared ACF fields;one hypothetical-cost mean and one fixture hash. Exact rational expectations/probabilities stay separate from numeric comparisons (rtol5e-14,atol1e-15). The ACF oracle expands raw lagged cross sums around the global mean, independently of source centered products; overlap references use exact gross products. These are no independent real data, PRNG runs or inferential acceptance tests.

Declare common amplitude A=.1 or.2 with equal probability, shared across four periods, and independent fair signs conditional on A. The32 paths have exact weight1/32. Each marginal mean is0,variance1/40; adjacent raw-return covariance is0, but squared-return covariance is9/40000>0. Thus uncorrelated raw returns do not establish independence. This is an explicit finite common-amplitude mixture, **not** a fitted dynamic volatility-clustering or forecasting model.

Source raw sample ACF is undefined on constant paths(probability1/8) and is compared to exact expanded sums on the other28 paths. Its conditional mean is−1/4 despite zero population lag covariance. Independent sign-pattern counts give ACF values−1/12(four),−5/12(four),1/4(two),−3/4(two),−1/4(two), conditional on nonconstant signs. Within each path squared returns are constant, so source correctly rejects all squared ACF calls; across the population law squared returns remain dependent. A short path's undefined/low diagnostic does not prove process independence or validate iid standard errors. The source has no HAC, conditional-volatility or independence-testing API.

Caller zero-filling[.1,0,−.1,0] versus compacting[.1,−.1,0] gives different native ACFs checked independently. Source rejects None rather than silently imputing; that does not identify a correct missingness policy. The prescribed24-period strategy/20-variant ledger/universe fixture hash matches earlier project evidence. Raw and squared-return ACFs match independent formulas. Subtracting a disclosed hypothetical.001 per-period cost gives native mean−.001; this is a supplied-cost sensitivity, not measured fees/slippage/financing/capacity.

|Remaining Section15.13 assumption topic|Scoped disposition and limit|
|---|---|
|Membership, selection, multiplicity|[170 retention/ledger predicates](../v10-selection-ledger/README.md), including F219; historical constituents/complete real trials remain external|
|Timing, revisions, calendars|[68 boundary predicates](../v10-asof-boundaries/README.md); source flags do not authenticate metadata or prove execution readiness|
|Dependence and overlap|Current finite-law/source metrics and prior rolling crosswalk; descriptive ACF is not calibrated uncertainty|
|Nonstationarity|Project amplitude change after period12 is specified synthetically; no structural-break test or fitted regime acceptance|
|Outliers/heavy tails|No actual price/action records classify an extreme as an error; automatic deletion of genuine losses is not justified by these diagnostics. Conceptual review, no deletion/audit claimed|
|Spurious association/causality|Prior regression counterexamples retain their scope; this listing has no causal or stationarity solver. Differencing alone is not accepted as a cure|
|Costs/economic relevance|Current hypothetical net-mean sensitivity; actual execution, liquidity and scale remain unresolved|
|Project disposition/provenance|Retain synthetic hashes, conventions and limits; recommend no real-strategy acceptance from this evidence. Earlier24 answers/twelve tasks not recounted|

Source metrics, exact-law/cost/imputation assembly and conceptual review are explicitly distinct. Each run executes the complete verbatim demo/twelve existing methods and compilation:four command records/24 invocations of twelve existing methods total. F219 corrected whole-source and F139 fence identities match; F139 fifteen baseline failures/42 arithmetic predicates and prior170/68 V10 predicates retain their scopes. No source change/defect or new workflow/answer/step/historical-method totals.

Selected15.13 V10 assumption crosswalk recorded; next15.14 toolkit shared-input/integration and model/report assumptions, retaining earlier arithmetic evidence. Broad real-data, model, robust-inference, resource, supported-platform, release, independent and canonical acceptance remains open; V10/Book1 and F28/F32/F209/F165/F185 are not closed.
