# V10 — Section15.4 shape/moment-identification assumptions

Source pin: `3c23b8721b0e2fa5a936438fd9cb0fa1aa4e0fbe`. [Runner](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-shape-models/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-shape-models/review.py replay
```

**65 predicates pass twice**,identical rows. Final pair:four exact demonstration/compilation commands /24 invocations of twelve existing methods. No source failure/change or new historical method/workflow/answer/task totals. Whole-source/listing hashes match [F130 prior review](../chapter-15-shape-review/README.md);its ten baseline failed predicates,49 corrected predicates,24 answers and ten project tasks retain their scopes.

Two symmetric finite laws are encoded as deterministic72-observation multisets (not72 independent simulated draws). A uses36 zeros,12 each of±.01 and6 each of±.02. B uses16 zeros,27 each of±.01 andone each of±.03. Both have raw moments(mean,m2,m3,m4)=(0,.0001,0,.00000003),so the **entire native standardized-moments reports agree**,including n72,skew0,kurtosis3,excess0. Yet native strict frequency R<−.02 is0 under A and1/72 under B. The supported maximum loss also differs. Normal-reference kurtosis3 or zero skew does not identify a normal distribution or tail-event probability.

The adjusted excess for both encodings is6*71/(70*69)=71/805,despite unadjusted excess0. The sample-size adjustment is a labelled estimator formula;it does not certify an underlying normal law or general finite-sample unbiasedness. Scaling,reflection and shifts retain their declared measurement meaning.

| Predicates | Native execution / independent expectation |
|---|---|
|18 |Two six-field reports,two adjusted skew/two adjusted excess and two strict downside frequencies. Central moments independently expand raw powers: m2=E[X²]−mu²,m3=E[X³]−3muE[X²]+2mu³,m4=E[X⁴]−4muE[X³]+6mu²E[X²]−3mu⁴. Rational/100-digit Decimal references differ algebraically from source centered-power sums. |
|3 |Equality of first four raw moments and whole native reports,plus zero excess under a nonnormal finite law. |
|24 |Four complete reports:original project,disclosed positive stress,disclosed negative stress,and caller removal of one zero from lawB. The last is a selection/denominator change,not an approved cleaning rule or deletion of a loss. |
|18 |Three complete affine-transformed reports:percent units,loss reflection,constant shift. |
|2 |Prior source/listing identities. |

Relative5e−14/absolute1e−15 tolerances apply to float fields. These examples establish scoped arithmetic and non-identification under supplied finite laws,not empirical future-loss calibration. Finite samples always provide finite sample powers here;they do not establish existence or stability of population moments for an unknown generating process. Serial dependence,regime changes,missingness and data errors remain external model/data questions.

Prior24 answer and ten project-task records remain unchanged: original and separate positive/negative stress copies,formula conventions,constant/short-sample rejections and supplemental m3/m4/median/type7 calculations retain prior scope. This batch adds finite-law/affine/selection assumptions without recounting records. Dates/frequency/source authenticity remain unspecified;no robust-data policy,forecast,causal interpretation or independent acceptance.

**Next:**15.5 covariance/joint-law/pairing assumptions,then15.6–15.7 correlation/sampling. V10/Book1 IN PROGRESS;F28 notebook/platform,F32 broader parsing/context/shared-input integration,F209/F165/F185 and numerical/resource/data/model/platform/release/independent/canonical gates remain open.
