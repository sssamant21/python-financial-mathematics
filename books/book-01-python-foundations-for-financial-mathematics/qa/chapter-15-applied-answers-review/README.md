# Section 15.15 — scoped chapter assessment and applied-case review

Baseline source: `67662441e603db4a369bc117d307facb143bd32c`. Scope: one assessment workflow, 48 chapter-wide answer records, four applied cases B–E, nine capstone checklist records and the 100-point rubric. These do not add local section prompts or become additional unique test-method counts.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-15-applied-answers-review/review.py
```

The observer extracts the single exact source fence, runs the printed twelve-method unittest command, checks silent import and runs the printed compilation command in isolation. Three commands and 49 supplemental predicates pass; no historical unique methods added. `results.json` retains runtime/platform, hashes, raw command outputs, expectations, tolerances and applied outputs. It also imports the exact linked Section 15.14 toolkit and calls OLS, CSV loader and full report once each (three additional source calls, not another twelve-method rerun or extra core workflow). The linked source/listing and CSV hashes are retained.

`baseline.json` preserves twelve failed predicates against unchanged baseline manuscript above, reproducible with the same runner/source revision. All twelve existing methods already passed. F141 corrects mean/SD/correlation precision and range failures, decimal constant correlation, a validation-only averaging step that overflowed before a true bankruptcy return, positive wealth falsely rounded to total loss, unreportable compounded outputs and multiplicity-threshold underflow. Rational intermediate arithmetic follows integer/displayed-decimal inputs, roots use 80-digit Decimal, and nonzero unreportable values are explicit errors. The applied reference answers also now include the requested numeric SD/cumulative result, explicit stress policy and fitted/residual arrays. The perfect-fit R² question now specifies nonconstant response, and overlapping-window dependence is correctly qualified as general rather than unconditional.

## Independent benchmarks and all 48 answer records

Means/gross products use Fraction; SD references use pairwise squared differences divided by n(n−1), independently of source centered squares. Scale-cancelled correlation expectations come from explicit algebraic fixtures. Applied regression uses exact linked source, with independent rational perfect-line expectations. Summary-statistic CI arithmetic uses Decimal with the stated critical value; it is supplemental, not a call on invented n=100 observations.

| Answers | Review and execution boundary |
|---|---|
| 01–07 | Mean 2, median 3, nearest-rank Q75=3, sample variance 1, population variance 2/3, source SD .01, SE .1/√25=.02. Median/quantile/variance/SE are independently derived, not exported by this assessment listing. |
| 08–09 | Left-tail asymmetry's conventional negative skew interpretation and normal-population excess zero reviewed; no empirical shape-distribution acceptance. |
| 10–14 | Sample covariance 2 derived; source correlations ±1 and constant rejection checked. Point-in-time survivor reconstruction remains a real-data requirement, not an executed reconstruction. |
| 15–20 | Normal CI≈[.0004,.0396], t df=4 under iid normal n=5, conditional p interpretation, Type I definition, power .8 and source Bonferroni .0025 reviewed. No calibration/power simulation or generic t CDF executed. |
| 21–24 | Exact linked toolkit slope 2/intercept 1/R²=1/SSE=0 checked. R² prompt now requires SST>0. Market beta is association, not causal proof. |
| 25–30 | Simple .1, log ln(1.1), source compound −.01 and mean 0, geometric √.99−1 and annualized .01√252 reviewed. Assessment source implements only mean/compound among these return functions; other answers are mathematical derivations or earlier-section source scope. |
| 31–35 | Declared left-return nearest-rank VaR .10, ceil-count ES .075 derived; source rolling means checked and n=20,w=5 gives 16. Constant rolling correlation undefined, distinct from zero. |
| 36–40 | Earlier-than-close execution, overlap, survivor/full means, tail reconciliation and stale quote effects reviewed. Source full-universe mean −.15 checked; no genuine market execution, outlier classification or quote audit. |
| 41–44 | 1bp−4bp=−3bp net; compatible CI/test duality, provenance and distinction between included tests and executed logs reviewed. No investment approval or independent certification inferred. |
| 45–48 | VaR not maximum loss, correlation not causation, justified HAC for serial dependence and small-sample limits reviewed conceptually. No HAC, tail calibration or causal model implemented here. |

All forty-eight answers have scoped review records in these ranges. Numeric checks, formula derivations and conceptual reviews are distinguished rather than claiming each exercise is a unique runtime test.

## Applied cases B–E

| Case/tasks | Evidence and limits |
|---|---|
| B1 | n=5, mean=.008, median=.01, min=−.02, max=.03. Independent sample variance=.00037; source SD=.019235384061671346. Original reference omitted the requested numeric SD; now supplied. |
| B2–B3 | Source cumulative=.03988388, independently rational gross product; all three source w=3 means [1/150,1/300,1/60] checked. |
| B4–B5 | Stress now explicitly appends −.20 as a sixth period. Source stressed mean=−2/75, SD≈.08664102184685189, cumulative=−.168092896. Original fixture remains unchanged. No rare-event coverage established from five/six observations. |
| C1–C3 | Independent means 2.5/6, Sxx=5, Sxy=10. Exact linked toolkit alpha=1 and beta=2 checked. |
| C4–C5 | Linked source SSE=0 and R²=1; fitted [3,5,7,9], residuals all zero and prediction 11 assembled from source coefficients. Reference arrays now explicit. x=5 extrapolates beyond observed [1,4]; no predictive acceptance. |
| D1–D2 | H0 mean zero, prespecified two-sided alternative; supplied summaries n=100, mean .02, SD .1 give SE=.01 and CI [.00040036015459946,.03959963984540054]. No raw n=100 sample was supplied or manufactured. |
| D3–D6 | Normal approximation/assumptions, p-value conditioning, Type I/II/power, source Bonferroni .0025, complete registry and chronological holdout reviewed. No actual experiment ledger or untouched financial holdout accepted. |
| E | Hypothetical backtest uses survivors, revisions and unavailable closes: reject it as decision-quality evidence until repaired. Universe reconstruction, as-of/version data, timing, quote freshness, overlap/cost reconciliation and prospective evaluation are design requirements, not performed operational work. |

## Capstone F: nine checklist records

| Checklist | Scoped status |
|---|---|
| Formulas/units | Documented and checked on the synthetic fixture. |
| Adjustments/calendar | CSV dates/schema exercised; actual corporate-action and exchange-session provenance unresolved. |
| Missing/nonfinite values | Assessment rejection probes and linked toolkit's retained evidence; no real-data cleaning. |
| Inference assumptions | Stated; no model/coverage calibration. |
| Selection/survivorship/as-of | Conceptual risk review; real audits remain open. |
| Tail conventions | Explicit signed nearest left-return rank and ceil-count ES; no certification. |
| Reproducibility | Hashes, source revision, runtime and commands retained. |
| Runtime | Three assessment commands plus three linked-source capstone calls executed. Full report mean/SD/cumulative and rolling cardinality independently checked; all other toolkit fields rely on the separately linked Section 15.14 evidence, not a claim of new independent acceptance here. |
| Independent acceptance | Pending; no named reviewer or certification. |

The full linked capstone report is retained in `results.json`, with source dates and hashes. Scope overlap with Section 15.14 is explicit: its original twelve methods are not counted again as new unique tests. The assessment rubric sums to 100 (15+15+15+15+10+15+10+5); no actual learner score or independent grade assigned. The 85-point classroom target is not certification.

## Chapter checkpoint and limits

All fifteen Chapter 15 workflows now have scoped review: fourteen core section/project workflows with 336 local answers, plus this one assessment workflow with 48 chapter-wide answers. These totals are not acceptance percentages or unique method counts. Next pending formal review: Chapter 16 Section 16.1 — Portfolio Fundamentals.

Local Linux CPython only. F28 notebook/platform, F32 broader shared-input integration and other unresolved findings remain open. The linked capstone fixture is limited integration evidence, not book-wide shared-input acceptance. No external-platform run, real-market data/operational approval, exhaustive branch proof, independent reviewer acceptance or certification. Source execution, rational/Decimal derivations, supplemental case assembly and conceptual design reviews remain separate.
