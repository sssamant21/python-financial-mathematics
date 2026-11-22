# V10 — Section15.3 variance/denominator/dependence assumptions

Pin: `f19f4218adbf94b9e6c33e5b5e8ae2a1d3024e9d`. [Runnable observer](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-variance-models/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-variance-models/review.py replay
```

**303 predicates pass twice**,identical rows. Four exact demonstration/compilation commands across final runs /24 invocations of twelve existing methods. No source failure/change,new historical unique method,workflow,local-answer or project-task totals. Source/listing hashes match [F129 prior review](../chapter-15-variance-review/README.md);its stress-variance observer error,twelve baseline source failures,47 corrected predicates,24 answers and ten project tasks retain their scopes.

| Predicates | Actual source execution and independent expectations |
|---|---|
|280 |20 paths:16 IID-sign,four-period histories plus two perfectly shared-sign and two alternating-sign histories. Every six-field moments report at ddof0 and1 is checked against exact pairwise-difference variance;two all-observation downside deviations per path use thresholds0 and.05. |
|15 |Five exact-law/native-scaling checks per temporal model:expected native sample variance,true variance of the four-period arithmetic sum,one-period marginal variance,supplied square-root4 scaling and actual horizon-sum SD. |
|6 |Three cross-asset joint laws:explicit portfolio outcomes/covariance versus native two-asset covariance formula. |
|2 |Prior source/listing identities. |

For each temporal law P(Rt=±.1)=1/2,so the same one-period marginal variance=.01. Under the declared IID law,Var(sum)=.04 and SD=.2;shared-sign dependence gives Var(sum)=.16,SD=.4;alternating signs give Var(sum)=0,SD=0. The source scaled_volatility(.1,4) returns.2 in every case because it evaluates the caller-supplied scaling formula;it does not validate serial independence or forecast volatility.

Expected native sample variance (ddof1) is.01 for IID,0 for shared-sign and1/75 for alternating-sign paths. Pairwise sample variance describes each supplied path;its unbiasedness claim depends on the sampling law. No arbitrary bias correction or real IID/stationary model is asserted. The sum-variance examples concern arithmetic period-return sums,not compounded wealth variance. Covariance terms explain the different horizon risks.

Downside deviation uses every observation in the denominator,including observations above the target. The reference computes exact lower partial squares and then a100-digit Decimal root;it is not the SD conditional on negative returns or an empirical tail-calibration claim. Native reporting uses its documented80-digit Decimal policy;relative5e−14 /absolute1e−15 tolerances apply to floats.

For equal portfolio weights and marginal variances.01/.01,independent asset outcomes have variance.005;perfectly matching outcomes variance.01;opposite outcomes variance0. Marginal SDs alone do not determine covariance or diversification. These are explicit finite joint laws,not empirical covariance estimates or accepted portfolio inputs. Native covariance feasibility is arithmetic support,not authenticity/model approval.

## Existing prompt/project contract disposition

Prior24 answers and ten mini-project tasks retain exact sums,ddof,SD/downside/scale/portfolio arithmetic and the declared hypothetical daily-return fixture [.02,−.01,.03,0]. New work qualifies denominator/unbiasedness,annualization/covariance and downside interpretation;it does not recount those records. Dates/prices/adjustment histories remain unspecified. Equal observed values do not prove zero future risk;clustered outcomes,changing variance and outlier reconciliation remain data/model obligations. Scalar routines do not join timestamps,estimate a time-varying volatility process or validate daily-calendar/exposure provenance.

**Next:**15.4 skewness/kurtosis finite-moment/shape assumptions,then15.5–15.7 covariance/correlation/sampling. V10/Book1 IN PROGRESS. F28 notebook/platform,F32 broader parsing/context/shared-input integration,F209/F165/F185 and resource/data/model/platform/release/independent/canonical acceptance remain open.
