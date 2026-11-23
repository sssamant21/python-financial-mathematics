# V10 — Section14.8 continuous-variable assumptions

Pin: `bf827d7f8351c0d99cfe5760540964dd31fbbe0b`. [Observer](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-continuous-variable-models/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-continuous-variable-models/review.py replay
```

**303 predicates pass twice**,identical rows. Four exact-source demonstration/compilation commands pass across the final pair,including24 invocations of twelve existing methods. Source/listing match [F117 formal review](../chapter-14-continuous-review/README.md):six failures,31 predicates,24 local answers and ten project requirements retain scope. No financial source change,new historical methods,workflows,answers or steps.

| Predicates | Native execution / independent expectation |
|---|---|
|140|35 rate/time cases check density,CDF,survival and complement,including negative support and small positive survival. Independent100-digit Decimal exponentials;zero absolute tolerance prevents a false zero passing for small survival.|
|18|Support-clipped intervals checked against high-precision endpoint survival differences.|
|48|24 quantiles checked against100-digit logarithms and separate native CDF roundtrips.|
|27|Exponential memoryless identity across selected rates/intervals. This is a model property,not evidence observed waiting times are memoryless.|
|54|Time/rate unit conversion preserves CDF while density scales inversely.|
|5|A density can exceed1 while continuous singleton mass is0. External censoring Y=min(T,1.5) adds a positive atom at1.5;the source still models uncensored T. Censored mean composition is labelled external.|
|6|A1/3–2/3 mixture of rate.5/2 exponentials has mean1 and variance2,unlike rate1's variance1. Native component survivals are assembled externally;conditional mixture survival differs from its unconditional survival,so the mixture is not memoryless.|
|3|Actual128-draw seed19 replay,count and support. No frequency/rare-tail calibration claim.|
|2|Prior whole-source/listing identities.|

Sections1–11 and formal density/probability/units/model prerequisites are crosswalked to these examples. The source has no mixture or censored-data estimation API;those counterexamples are external compositions. Prior24 answers/ten requirements retain their scope. Actual settlement/queue hazard calibration,dependence,regime changes,right-censoring,clock conventions,provenance and operational acceptance remain external or conceptual. F117 extremely small probability output can still round to0;this selected moderate-range review does not close that limit or cross-platform/rare-tail sampling gaps.

Next:14.9 expected-value assumptions,then14.10–14.17 and other marked interfaces in the [V10 scope index](../v10-scope-probability-models/README.md). V10/Book1 remain IN PROGRESS. F28/F32/F209/F165/F185 and broader numerical/resource/data/model/platform/release/independent/canonical gates remain open. Local Linux CPython only.
