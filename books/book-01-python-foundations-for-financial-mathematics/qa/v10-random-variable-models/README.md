# V10 — Section14.6 random-variable mapping assumptions

Pin: `f4c6b28094883b23c8bf79de51da540e904e3443`. [Observer](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-random-variable-models/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-random-variable-models/review.py replay
```

**679 predicates pass twice**,identical rows. Four exact-source demonstration/compilation commands pass across the final pair,including24 invocations of twelve existing methods. Source/listing match [F115 formal review](../chapter-14-random-variables-review/README.md):six failures,30 predicates,24 local answers and ten project tasks retain scope. No financial source change,new historical methods,workflows,answers or steps.

| Predicates | Native execution / independent model expectation |
|---|---|
|648|All81 mappings from four weighted states to payoffs−1,0,2. Eight checks each:pushforward distribution,direct-state expectation,pairwise-distance variance,negative event,CDF at0,indicator mean,affine mean and affine variance. Oracles sum original-state preimages/raw payoffs rather than source grouped moments.|
|5|Different source-state laws(.5/.5 versus.9/.1) share deterministic payoff1 and zero payoff variance. A many-to-one payoff mapping cannot recover the original state probabilities.|
|2|E[X²]=1 versus(E[X])²=0 for a fair±1 payoff. Nonlinear transforms do not commute with expectation.|
|15|Three common-state two-asset mappings have identical marginal means0/variances1,but equal-weight portfolio variance.5,1,0 under independent/shared/offset mappings. Marginal payoff distributions do not determine the joint state alignment.|
|4|Terminal price,currency payoff and dimensionless one-period simple return are separate mappings. Dollar-payoff variance200 versus return variance.02 verifies their unit scaling;no discounting/annualization or forecast guarantee.|
|3|Actual128-draw seed19 replay,count and shared-state affine transformation agree. Fixed replay reflects the supplied state law/algorithm,not empirical joint-law calibration.|
|2|Prior whole-source/listing identities.|

Sections1–12 and formal transformation/event/unit prerequisites are crosswalked to these finite examples. The CDF check uses the native event predicate on a finite discrete distribution;it does not introduce a continuous CDF API. Prior24 answers/ten tasks remain formal evidence. Real state exhaustiveness,probability/return units,price basis,horizons,coarsening choices,common-state correspondence,provenance and calibration need caller/data/model evidence. F115 rare-tail floating-sampler and cross-runtime limits remain;seed replay does not close them.

Next:14.7 discrete-random-variable assumptions,then14.8–14.17 and other marked interfaces in the [V10 scope index](../v10-scope-probability-models/README.md). V10/Book1 remain IN PROGRESS. F28/F32/F209/F165/F185 and broader numerical/resource/data/model/platform/release/independent/canonical gates remain open. Local Linux CPython only.
