# V10 — Section15.11 historical-tail stability and caller selection

Executed source pin: `d0162ccb04b8a3fd97fe3928de6a5c1a597f1ab7`. [Runnable review](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-historical-tail-selection/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-historical-tail-selection/review.py replay
```

**267 predicates pass twice with identical rows:**256 native VaR/ES comparisons over64 ordered six-observation paths and two alpha settings;eleven exact law/weighted estimator/selection comparisons. Cached native metrics feed an exact4096-pair caller selection law; these pairs are not4096 extra source tests or independent simulations. Native numeric comparisons use rtol5e-14,atol1e-15. Exact path weights, binomial probability identities and selection counts use fractions. No PRNG, real strategy search, or empirical market coverage is claimed.

Declare IID returns R=−.5 with probability.1 and R=.02 with probability.9, six training observations, and an independent future observation. At alpha.05, ceil(alpha×6)=1: native signed left-return VaR and ceil-count ES both use the minimum return. With k bad observations, VaR=.5 iff k≥1, otherwise−.02; ES is identical. At alpha.25, count2: VaR=.5 iff k≥2, while ES averages min(k,2) bad and the remaining good returns. These closed binary-order/count identities are independent of sorting implementation. The count2 estimator uses2/6 observations, not a fractional25% tail; its expected ES822089/6250000 is compared to its own declared estimator, not silently to a different population ES definition.

|Exact quantity under the specified IID law|Single predeclared candidate|Caller chooses lower in-sample5% VaR of two identical independent candidates|
|---|---:|---:|
|Probability fitted tail contains no bad return|.531441|.780452463519|
|Expected empirical5% VaR/ceil-one ES|.22365068|.09416471897012 (selected VaR)|
|Independent future loss strictly exceeds selected fitted signed threshold|.0531441|.0780452463519|

The no-bad probability is q=.9^6; selection probability1−(1−q)^2. The exact weighted source estimates match. Both candidates have the same known future bad-return probability.1, independent of training, so selection does not reduce their population risk. Population95%-loss quantile and fractional5% ES both equal.5 under this particular binary law. Strict exceedance at threshold.5 is0 because of the atom; at−.02 it is.1. Thus the reported future strict-exceedance numbers are calculations under explicit atom/tie conventions, not a general calibrated backtest or an assertion of equality with nominal.05. Historical estimator arithmetic is correct; finite-sample instability and data-dependent selection are model/procedure limits, not source bugs.

The six-observation tail warning and signed/ceil-count conventions in the existing exercises/project align with these examples. These records do not create new local answers, workflows, project tasks or historical test methods. The source implements metrics only; pair selection, probability weighting, population references and future-observation modeling are supplemental. Each run executes the complete verbatim demo/twelve existing methods and compilation:four command records/24 invocations of twelve existing methods total. Whole-source/fence identities match F137 corrected evidence; its twelve initial failures/46 arithmetic predicates and earlier168 scaling predicates retain their own scope.

No source change/defect. Section15.11 remains partial:next upstream return basis/corporate-action/alignment and supplied-project provenance boundaries before15.12. No real corporate actions, quote staleness, calendar joins, benchmark feed or tail-model acceptance is inferred. V10/Book1,F28/F32/F209/F165/F185 and broader numerical/resource/data/model/platform/release/independent/canonical gates remain open.
