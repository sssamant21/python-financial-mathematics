# V-251 — Section10.6 complete fixed report and proof/provenance crosswalk

Executed source pin: `1a5045c7a3c39727737579534f7074051559aa64`. [Runnable review](review.txt), [first](first.json), [replay](replay.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-improper-report-2026-11-22/review.txt first
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-improper-report-2026-11-22/review.txt replay
```

**75 predicates pass twice with identical rows and complete reports:**four global checks,45 ordered row/schema/finite-value checks,24 convergent-row limit/tail/target/decomposition/invariant checks,and two whole-report checks. Each run imports pinned exact source and executes CLI/checker/compilation(three commands,six total); all actual outputs,environment and source/checker Git blob/SHA256 identities retained. No source failure/change was found in this scoped report review.

The fixed assessment uses C1000,r.05,growth0/.02/.04/.049/.05,horizons10/30/100,and tail fraction.01. Every schema/global/scenario field is checked. Independent1800-digit integrated exponential series evaluates finite values, a separate exponential series evaluates tails, and range-reduced atanh-logarithm plus an independent upward report evaluates target horizons. Selected actual float targets satisfy the high-precision dT≥−ln(.01) comparison. Numeric fields/decomposition use rtol5e-14,atol0; rates/convergence/schema/target reports compare exactly. This is not a universal directed-rounding or all-input proof.

Convergent rows alone contain perpetuity/tail/target keys. The g=r row has finite CT values but no improper-limit fields, preserving the convergence gate. Positive finite PV grows with T; convergent finite PV stays below its limit,tail stays positive,and near-critical perpetuity values increase as decay approaches0. Native runtime_certified and independent_review_completed remainFalse. Arithmetic under this fixed model does not validate real infinite-horizon cash flows/default survival or report provenance.

|Proof/manuscript obligation|Independent analytical disposition (not native execution)|
|---|---|
|Exponential improper limit|For d>0, exp(−dT)→0 and limit C/d; d=0 gives CT, d<0 grows for nonzero C. C0 is identically0; negative C changes sign, not convergence criterion|
|Tail and truncation target|Subtract the finite antiderivative from C/d to obtain C exp(−dT)/d. Positive-stream fraction exp(−dT)≤epsilon is equivalent to T≥−ln(epsilon)/d|
|p-integral|Integrate1→M: (M^(1−p)−1)/(1−p),then take M→∞. Finite1/(p−1) only for p>1; p1 gives lnM divergence|
|Finite endpoint singularity|Integral epsilon→1 of t^(−1/2)=2(1−sqrt(epsilon))→2; integral1/t=−ln(epsilon)→∞|
|Interior singularity|Separate one-sided limits; Cauchy-principal-value cancellation does not establish the improper integral. No singular-integrator API is supplied|
|Comparison/regularity|Eventual nonnegative exponential upper bound plus local integrability gives convergent tail; an eventual positive lower bound forces divergence. Local singularities need their own checks|
|Perpetuity sensitivity/model risk|Differentiate C/(r−g): rate sensitivity−C/(r−g)^2,growth sensitivity opposite. No derivative API introduced; rates near equality amplify assumed-model sensitivity|

These are derivations of the specified examples, not independent reviewer signoff or proof of real-source assumptions. All14 exercise dispositions and six earlier lab units are reconciled without new exercise/workflow/step counts. Singular examples and comparison conditions remain explicitly conceptual; the ordinary p-helper numerical contract is in V250.

External QA records the fixed payment/continuous-compounding/time-in-years convention,horizons/fraction,source pin and model limitations. Currency label and real valuation date are unspecified. Native payload lacks a generalized metadata/valuation-date/report-input adapter; this is a fixed illustration reproduced from source, not a self-contained production valuation record. Prior V247–250 failures/corrections and explicit exact-input,upward-report,underflow/cutoff/precision/resource policies retain scope.

Next:finish V252 pinned full runtime,verify executable blobs unchanged by documentation,then10.7 numerical-quadrature lab/source crosswalk if the progression gate passes. Book2 remains IN PROGRESS. All38 selected COV categories remain partial,none closed;these are not defect counts/percentages. Broader numerical/resource/provenance/model/platform/release/independent/canonical acceptance remains open. Book1 separate.
