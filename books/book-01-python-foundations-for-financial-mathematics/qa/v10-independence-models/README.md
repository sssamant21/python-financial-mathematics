# V10 — Section14.5 independence/joint-law assumptions

Pin: `ff67ac399441099d09200fd6cd26f65390cb32a3`. [Observer](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-independence-models/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-independence-models/review.py replay
```

**281 predicates pass twice**,identical rows. Four exact-source demonstration/compilation commands pass across the final pair,including24 invocations of twelve existing methods. Source/listing match [F114 formal review](../chapter-14-independence-review/README.md):six failures,41 predicates,24 local answers and eight project tasks retain scope. No financial source change,new historical methods,workflows,answers or steps.

| Predicates | Native execution / independent model expectation |
|---|---|
|216|36 Bernoulli parameter pairs check constructor mass,marginals,joint,exact independence and assumed union. The constructor imposes a product law;it does not infer independence from observed assets or loans. Union references use two-event inclusion-exclusion.|
|24|IID three-bit and four-atom even-parity/XOR models both have marginals.5 and pairwise joints.25. All pairs are natively independent,but triple probability is1/8 versus0 and actual union7/8 versus3/4. The marginal-only independent-union helper returns7/8 in both;pairwise independence is insufficient for its three-event assumption.|
|20|Four loan joint laws retain default marginals.02/.03 while joint defaults vary0,.0006,.01,.02. Exact independence holds only at.0006;actual union ranges.05 to.03,while the assumption-based helper stays.0494.|
|4|X uniform on−1,0,1 and Y=X² have external exact covariance0,but native events X=0/Y=0 are dependent (joint1/3 versus product1/9). No native covariance API or causal conclusion is invented.|
|10|Two regimes with within-regime independent Bernoulli rates.1/.9 mix equally. Native conditional marginals/joints match those models;unconditional joint.41 and union.59 differ from independent marginal union.75. Conditional independence does not establish unconditional independence.|
|2|A rare event of exact mass1e−80 is dependent with itself under exact equality,but an opt-in1e−12 tolerance accepts approximate independence. This is a tolerance-policy distinction,not a calibrated statistical decision.|
|3|Unknown labels,empty probability lists and bool tolerance reject.|
|2|Prior whole-source/listing identities.|

Sections1–10 and formal worked-example assumptions are crosswalked to the finite models. The native helper evaluates the supplied joint distribution;it does not discover actual tail dependence,measure independence from data or validate the product assumptions used by the constructor/union helper. Prior24 answers/eight tasks remain formal evidence. Actual default horizons,common shocks,conditional regimes,data provenance,calibration,stress probabilities and model/decision acceptance remain conceptual or external obligations. Finite examples do not prove an empirical independence assumption or an exhaustive probability theorem.

Next:14.6 random-variable assumptions,then14.7–14.17 and other marked interfaces in the [V10 scope index](../v10-scope-probability-models/README.md). V10/Book1 remain IN PROGRESS. F28/F32/F209/F165/F185 and broader numerical/resource/data/model/platform/release/independent/canonical gates remain open. Local Linux CPython only.
