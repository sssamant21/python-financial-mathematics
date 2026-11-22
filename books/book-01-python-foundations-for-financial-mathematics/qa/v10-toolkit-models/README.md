# V10 — Section 15.14 toolkit model/report assumptions

Source pin: `f77f274e9f0f601ad1b950097f38be188baecae5`. [Runnable observer](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-toolkit-models/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-toolkit-models/review.py replay
```

**870 predicates pass twice**, identical rows. Source main fence and compile command pass in each run: four command records /24 invocations of twelve existing reference methods. No new historical unique methods, workflows, exercise/answer/step totals. Source/listing match F140's corrected [prior evidence](../chapter-15-toolkit-review/README.md); its observer failure, nineteen baseline source failures, 62 corrected arithmetic predicates and full24-answer/32-step records remain preserved. The [108-predicate shared-fixture integration](../v10-toolkit-integration/README.md) and its observer date failure remain separate.

| Batch | Actual source execution and independent expectations |
|---|---|
| 92 CI-law predicates | All16 IID fair-sign paths and two perfectly shared-sign paths, four returns each, with marginal P(R=±.1)=1/2. Native mean/SD/two normal-CI endpoints/coverage indicator checked on every path, plus two aggregate coverage predicates. Independent pairwise-difference variance and a fixed normal critical literal supply endpoint expectations. |
| 770 tail-law predicates | All256 histories from IID uniform {−.2,−.1,.1,.2}; each native tail count/VaR/ES checked against exact minimum rank for n4,alpha.05. Two further exact-law checks aggregate independent next-draw strict exceedances. |
| Eight association/identity predicates | Four OLS fields from exact Y=1+2X; two external intervention means under alternative structural equations; two source/listing identity checks. |

For the declared IID-sign law, all-equal samples (2/16) produce zero-width intervals at ±.1, missing the true mean0. Every other sign pattern covers0: exact coverage14/16=7/8. Under the shared-sign joint law every sample is all equal, hence coverage0 despite the same one-period marginal law. The source does not return these probabilities; this observer aggregates source endpoints under explicitly supplied finite laws. Neither law is a market-data estimate or a proof about arbitrary normal intervals. The literal critical value checks the declared normal approximation, not a new independent critical-value algorithm.

For the four-point tail law, the next return is strictly below the observed minimum with probability
`(1/4)[(3/4)^4+(2/4)^4+(1/4)^4]=98/1024=49/512=.095703125`, rather than requested .05. Ties are excluded. Signed VaR/ES and the ceil-count estimator are unchanged; this finite-sample diagnostic is not a source defect or predictive-calibration claim. A one-observation empirical tail does not guarantee a5% future exceedance rate.

Observational X=U,Y=1+2X and X=U,Y=1+2U both yield source alpha1,beta2,R²1,SSE0 for U={−2,−1,1,2}. Externally setting X=3 yields meanY7 in the first structural model and meanY1 in the second. These are supplemental structural equations, not a causal capability of OLS. No native causal or robust-regression API is invented.

## Remaining project assumption and deliverable disposition

| Source obligations | Disposition and limits |
|---|---|
| Answers1–14, LabB/C1–3/D1,3–4/E1–4 | Prior numerical/step review and shared-fixture evidence retained. New work adds selected uncertainty/tail/association diagnostics; it does not recount answers or create another project workflow. |
| Answers15–18, LabC4–5/D2,5 | Undefined dependence/fail-fast report contract recorded previously. New finite-law examples demonstrate small-sample/dependence limits; no IID/normal/OLS inference acceptance, HAC estimates or calibration. A high R² is not causal identification. |
| Answers19–21, LabA/F1–5 | CSV schema/ISO ordering are native checks; corporate actions, exchange sessions, historical constituents/delistings, availability/revisions, missingness/staleness and complete variant ledger require external provenance. No feed, real universe, outlier reconciliation or leakage audit accepted. Multiplicity methods remain in their own section; toolkit adds none. |
| Answers22–24, LabE5/F6 | Annualization needs interval/dependence assumptions; positional windows do not prove signal availability. Chronological holdout, costs/capacity and prospective monitoring remain designs, not an executed strategy. Exact source/fixture/environment/output records exist; independent approval does not. |

| Seven deliverables | Evidence boundary |
|---|---|
| CSV and implementation | Exact source fences and source hashes retained; fictional USD/raw prices. No real split/dividend/FX/calendar adapter. |
| Report | Prior exact helper report and new native demonstrations retain outputs; no partial-report interface or new provenance fields. Undefined required dependence fails explicitly. |
| Assumptions/data-quality register | This crosswalk plus prior32-step/twelve-domain tables distinguish verified numeric behavior from unaccepted data/model prerequisites. |
| Test log | Runnable observer, two actual result files, preserved earlier failures and exact-source command logs. |
| Interpretation | Descriptive fixture statistics and disclosed finite-law diagnostics; no investment, forecast, coverage or causal acceptance. |
| Unresolved risks | Data authenticity/alignment, model dependence/tails, resources/security/performance/observability, installation/platform, independent/release/canonical gates remain open. |

The twelve readiness domains retain prior dispositions: provenance/alignment unresolved for real data; mathematics has scoped benchmarks only; reproducibility has exact artifacts; numerical stability lacks exhaustive proof; security/performance/operational observability unperformed; bias/inference not calibrated; change-management records are not named independent approvals; acceptance remains NOT_CERTIFIED. No production operations or acceptance inferred.

**Checkpoint:** Selected15.14 assumption crosswalk recorded. Next15.15 assessment/model-assumption crosswalk, retaining earlier formal answer/lab records. Section/project and Book1 broader acceptance remain open. V10 IN PROGRESS; F28 notebook/platform and F32 book-wide parsing/context/shared-input integration remain OPEN, as do F209/F165/F185 and numerical/resource/data/model/platform/release/independent/canonical gaps. No source modification was needed.
