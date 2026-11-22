# V10 — Section15.2 quantile/selection/exposure assumptions

Source pin: `3394dadd805cd683c35c4e1232df2b7a1b01aff9`. [Runner](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-quantile-design/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-quantile-design/review.py replay
```

**975 predicates pass twice**, identical rows. Final pair has four exact demonstration/compilation commands /24 invocations of twelve existing methods. No source failure/change or new historical unique methods, workflows, local-answer or task totals. Source/listing match [F128 prior review](../chapter-15-quantiles-review/README.md); its nine baseline failures,49 corrected predicates,24 answers and ten mini-project tasks remain preserved.

| Predicates | Verified scope |
|---|---|
|960 | All64 n3 histories from uniform {−.2,−.1,.1,.2},five probabilities(.05,.25,.5,.75,.95),three native checks each: type7 vs independent rational barycentric order-statistic oracle,nearest rank vs integer ceiling,and type7 loss transformation under negative exposure scaling with reflected probability. |
|2 | Exact next-draw strict-breach probabilities under the disclosed IID four-point law:39/128 for type7 sample Q.05 versus9/64 for nearest-rank minimum. These probabilities are external law aggregation,not source forecasting/calibration outputs. |
|2 | Type7 negative-scale reflection versus a nearest-rank counterexample at a discrete rank boundary. |
|4 | Three hypothetical exposure-weight cases plus beginning/ending-weight difference. Normalizing proportional weights preserves the mean; ending weights describe a different caller aggregation from the beginning-period portfolio return. |
|5 | Extreme-observation mean/median stress,untrimmed/trimmed estimates and native transformed project loss quantile3400. |
|2 | Prior whole-source/listing identities. |

For sample Q.05,n3,type7 h=.1. At any supported future level z, Q>z iff all three samples exceed z or exactly one equals z and the other two exceed z;the.1 interpolation remains below the next supported level. If U=P(R>z), the probability is U³+3(1/4)U². Averaging over four z gives39/128. Nearest-rank Q.05 is the sample minimum;averaging U³ gives9/64. Strict ties are excluded. Neither quantity equals requested.05;these are small-sample estimator behaviors under a specified law,not market predictive probabilities or source defects.

Type7 obeys Q(−V*R,1−p)=−V*Q(R,p) under the displayed-decimal policy for positive V. Nearest-rank does not always obey this identity: values[0,10,20,30],p=.25 give return rank0,while loss Q.75=−10. This does not invalidate either declared convention; it requires an explicit rank/tie/sign contract. The source project uses type7 and gives stylized loss3400 at exposure100000;no approved VaR model.

Beginning weights.75/.25 and returns.02/.08 give portfolio gross1.035. External ending weights are w_i(1+R_i)/1.035;feeding them to the source produces a different weighted mean. The code checks nonnegative finite weights and length,not holdings timestamps,common horizons,FX,corporate actions or exposure provenance. Integer-rescaled weights give the same beginning-weight mean. No native holdings adapter is invented.

## Prompt/project assumptions retained

Answers1–16 retain prior location/rank/trim/weight arithmetic;new exact-law evidence separates conventions and estimands without recounting prompts. Answers17–18 retain translation/positive-scale definitions;new negative-scale reflection requires a complemented probability. Answers19–20 stress mean sensitivity/selected median robustness without claiming arbitrary contamination resistance. Answer21 missingness remains an explicit upstream policy,not automatic zero fill or feed repair. Answers22–24 tiny-sample tail and loss-quantile interpretations remain descriptive,not forecasts.

All ten prior mini-project tasks retain source/fixture/environment records,original and stressed reports,quantile/IQR/downside/weight arithmetic and explicit unspecified dates/frequency/currency/provenance. Selection/trimming changes the estimand;real outlier validation,chronological alignment,stationarity and future coverage are unaccepted. Relative5e−14 / absolute1e−15 tolerances apply to float reports;exact ranks/probabilities remain distinct. No genuine data source,calendar,loss-model or independent acceptance.

**Next:**15.3 variance/denominator/dependence assumptions,then remaining15.4–15.7. V10/Book1 IN PROGRESS;F28 notebook/platform,F32 broader parsing/context/shared-input integration,F209/F165/F185 and numerical/resource/data/model/platform/release/independent/canonical gaps remain open.
