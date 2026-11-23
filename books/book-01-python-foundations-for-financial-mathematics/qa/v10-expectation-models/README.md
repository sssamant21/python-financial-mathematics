# V10 — Section14.9 expected-value/factorization assumptions

Pin: `2d5f2c8ccaffe737a199d7270a4bc048ca420dee`. [Observer](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-expectation-models/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-expectation-models/review.py replay
```

**52 predicates pass twice**,identical rows. Four exact-source demonstration/compilation commands pass across the final pair,including24 invocations of twelve existing methods. Source/listing match [F118 formal review](../chapter-14-expected-value-review/README.md):nine failures,37 predicates,24 local answers and ten project requirements retain scope. No financial source change,new historical methods,workflows,answers or steps.

| Predicates | Native execution / independent model expectation |
|---|---|
|12|Fixed exposure10000/default probability.5 and three default/LGD joint laws have the same unconditional LGD mean.5,but direct expected losses2500,4000,1000. Using appropriate conditional LGD.5/.8/.2 with fixed exposure reproduces each loss. Native expected_loss multiplies supplied scalar factors;it does not infer their conditional meaning.|
|12|When every state defaults,three exposure/LGD couplings retain mean exposure20000 and mean LGD.5,but expected products10000,13000,7000. Even conditional means do not factor a random product without justification.|
|9|Signed affine expectation identities;linearity needs matching measure/units and integrability,not independence.|
|6|Common-state independent/shared/offset payoff mappings all preserve E[X+Y]=E[X]+E[Y]. This does not establish equal risk.|
|4|Hypothetical physical/pricing-teaching measures give different expectations80/30 and deterministic periodically discounted results. The helper does not identify an appropriate pricing measure or establish an arbitrage-free market price.|
|1|110 discounted at10% effective periodic rate for one period is100;this input convention differs from a continuously compounded rate.|
|4|Certain100 and fair50/150 have identical expected wealth,but different expected dimensionless log-relative-wealth utility. This is a model/preference counterexample,not a recommendation.|
|2|Matching regime weights reconstruct expected payoff−33;incorrect equal weights change the question and produce−67.5. Conditional composition is external,not a new native conditional-expectation API.|
|2|Prior whole-source/listing identities.|

The fixed-loss helper is valid as scalar arithmetic. The counterexamples deliberately test whether a caller can substitute unconditional/conditional marginal means for a joint expected product. They do not claim that an appropriately defined fixed-factor credit convention is inherently invalid. Actual PD/LGD/EAD definitions,default horizon,conditional dependence,pricing measure,discount convention,probability calibration,data provenance and decisions require external evidence. Continuous/infinite-support integrability and broader resource/platform acceptance are not established by these finite cases.

Two preparatory observer attempts stopped on the same missing-space SyntaxError before importing financial source. [Failure record](initial-observer-failure.json) and [original observer](initial-observer-syntax.txt) remain. The corrected runner passes twice;the parse failures add no source commands or historical methods.

Next:14.10 variance/SD assumptions,then14.11–14.17 and remaining marked interfaces in the [V10 scope index](../v10-scope-probability-models/README.md). V10/Book1 remain IN PROGRESS. F28/F32/F209/F165/F185 and broader numerical/resource/data/model/platform/release/independent/canonical gates remain open. Local Linux CPython only.
