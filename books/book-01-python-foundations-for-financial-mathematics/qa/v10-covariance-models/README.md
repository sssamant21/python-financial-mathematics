# V10 — Section15.5 covariance/joint-law/pairing assumptions

Source pin: `83322aff81c8a0fa62a1cd0787e6cad96acf56e0`. [Runner](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-covariance-models/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-covariance-models/review.py replay
```

**283 predicates pass twice**,identical rows. Final pair:four exact demonstration/compilation commands /24 invocations of twelve existing methods. No source failure/change or new historical method/workflow/answer/task totals. Source/listing match [F131 prior review](../chapter-15-covariance-review/README.md);eight baseline failed predicates,44 corrected predicates,24 answers and ten project tasks retain their original scope.

| Predicates | Native execution / independent expectation |
|---|---|
|270 |All30 distinct permutations of Y=[.04,.01,0,.01,.04] against X=[−.02,−.01,0,.01,.02]. Each has two covariance denominators,correlation,two direct portfolio comparisons (weights.5 and1.5),and four matrix entries. Rational raw cross-products supply covariance independently of source centered products;direct portfolio observations supply variance independently of the expansion. |
|6 |Exact minimum/maximum sample covariance−11/40000,+11/40000;native zero covariance/correlation under nonlinear Y=100X²;external joint-event probability and non-independence check. |
|5 |Three native scalar covariances on different two-row subsets,external indefinite-matrix quadratic,and selected common-row native matrix quadratic. |
|2 |Prior source/listing identities. |

All30 pairings preserve the marginal samples/variances but change the joint sample. Equal length is a positional contract,not timestamp alignment or an accepted historical pairing. Fictional dates/calendars,availability,corporate actions and data authenticity remain upstream obligations. Signed portfolio weights are permitted by the source;they are not validated holdings/exposure provenance.

Under the disclosed five-point uniform joint law,Y=100X² gives zero covariance and correlation,while P(X<−.01,Y>.03)=.2 differs from P(X<−.01)P(Y>.03)=.08. This extends prior arithmetic zero-covariance examples into an explicit event-factorization check;it does not add a causal or independence-test API. No real market law or forecast is accepted.

External pairwise-subset assembly uses AB on hypothetical dates1–2,AC on3–4 andBC on5–6. Each source scalar covariance is valid on its own supplied pair:2,2,−2. Combining them with diagonal2 yields [[2,2,2],[2,2,−2],[2,−2,2]],whose quadratic at w=[−1,1,1] is−6. This matrix is indefinite. The source covariance_matrix does not assemble missing-data pairs or certify this matrix;its selected common-row counterpart has quadratic2. A scalar feasibility check or symmetric appearance does not establish compatible joint observations. No general floating-point PSD guarantee or shrinkage/missing-data estimator is invented.

Relative5e−14/absolute1e−15 tolerances cover float reports. Portfolio and event calculations are supplemental exact oracles;source scalar/matrix execution remains distinct from conceptual timing,missingness,exogeneity and model acceptance.

Prior24 answers/ten project tasks retain formula/denominator/unit/matrix/portfolio benchmarks,declared positional prerequisites and synthetic provenance. New work qualifies nonlinear dependence,matching marginal samples and common-row matrix assumptions without recounting records. No source fix was needed.

**Next:**15.6 correlation/nonlinear dependence/selection assumptions,then15.7 sampling/estimation. V10/Book1 IN PROGRESS;F28 notebook/platform,F32 broader parsing/context/shared-input integration,F209/F165/F185 and numerical/resource/data/model/platform/release/independent/canonical gates remain open.
