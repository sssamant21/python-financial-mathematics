# V10 — Section14.7 discrete-variable/binomial assumptions

Pin: `d2e0b72758c3bb81321b0786021d28ff70ed25d0`. [Observer](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-discrete-variable-models/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-discrete-variable-models/review.py replay
```

**1283 predicates pass twice**,identical rows. Four exact-source demonstration/compilation commands pass across the final pair,including24 invocations of twelve existing methods. Source/listing match [F116 formal review](../chapter-14-discrete-review/README.md):seven failures,48 predicates,24 local answers and ten project tasks retain scope. No financial source change,new historical methods,workflows,answers or steps.

| Predicates | Native execution / independent expectation |
|---|---|
|1260|35 binomial parameter cases:n0–6,p0/.1/.5/.9/1. External binary-sequence enumeration replaces the source comb/power formula as PMF oracle;direct weighted counts and pairwise-distance variance check moments.385 half-integer thresholds each check inclusive CDF,strict tail and reported complement. Finite atom boundaries are explicit.|
|9|IID6,p.5,heterogeneous independent probabilities[0,.1,.2,.8,.9,1],and a common-shock count all have mean3. Variances are1.5,.5,9 and P(N>4) is7/64,9/625,1/2. Equal means/marginals do not establish a binomial count law.|
|3|Mixing four conditionally independent loans at p.1/.9 with equal regime weights gives mean2,variance2.92 and P(N>3)=.3281. A common regime creates unconditional dependence.|
|6|Fixed1000-loss-per-default mappings preserve mean3000 while variance scales by1000² across the three six-loan laws. Random severity/heterogeneous exposures are not represented by this fixed multiplier.|
|3|Actual128-draw seed19 replay,count and support checked;no empirical-frequency or rare-tail calibration claim.|
|2|Prior whole-source/listing identities.|

Sections1–10 and formal count/CDF/default-model prerequisites are crosswalked to these finite laws. A binomial constructor encodes fixed n,equal p and independent trials;it does not infer those conditions from a portfolio. The source tail helper uses strictly greater than threshold,while CDF includes equality. Prior24-answer/ten-task records remain formal evidence. Actual borrower dependence,default horizons,regime stability,probability calibration,loss severity,exposure weights and decision suitability need caller/data/model evidence. F116 full-support construction/resource and floating rare-tail sampling limits remain;this small exhaustive enumeration does not resolve production-scale support or platform acceptance.

Next:14.8 continuous-variable assumptions,then14.9–14.17 and other marked interfaces in the [V10 scope index](../v10-scope-probability-models/README.md). V10/Book1 remain IN PROGRESS. F28/F32/F209/F165/F185 and broader numerical/resource/data/model/platform/release/independent/canonical gates remain open. Local Linux CPython only.
