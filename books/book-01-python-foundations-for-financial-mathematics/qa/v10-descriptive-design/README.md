# V10 — Section15.1 descriptive measurement/sampling assumptions

Pin: `8e2cd8aee2f7497e8da34be3f86c22ce28da3c85`. [Runner](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-descriptive-design/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-descriptive-design/review.py replay
```

**171 predicates pass twice**, identical rows. Final pair: four exact-source demonstration/compilation commands;24 invocations of twelve existing methods. No new historical methods, workflow, local-answer or step totals. Source/listing hashes match [F127 prior evidence](../chapter-15-descriptive-review/README.md); its five baseline failures,32 supplemental predicates,24-answer/six-deliverable records and scope remain preserved.

Initial [observer](observer-initial.py)/[traceback](observer-initial.json) retain an oracle failure: singleton pairwise sum began as integer0 and division yielded a float, incompatible with the rational-root helper. Starting the sum at Fraction(0) fixes the observer. A second [observer](observer-drawdown.py), [first170/1](observer-drawdown-first.json) and [replay170/1](observer-drawdown-replay.json) retain a wrong expected minimum drawdown .109; [-.1,.1,.1,-.1] has maximum drawdown.1. Corrected external expectation.1 passes. A third [observer](observer-metadata.py) and observer-metadata-first/replay.json retain171 passing predicates with a malformed source_path metadata field: the wealth-path list reused that variable. Pre-publication identity verification caught it; the corrected runner separates wealth_path and retains the source-path string. These are observer mistakes, not manuscript defects; source remained unchanged. Archived failed attempts are separate from final execution totals.

| Predicates | Source execution / independent expectation |
|---|---|
|88 | All11 summary fields for eight disclosed fixtures: original decimal returns, percent units, shifted values, omitted/zero-filled observation conventions, untrimmed/trimmed extremes and singleton. Pairwise-difference variance uses a different algebraic form from native centered squares; Fraction/100-digit Decimal roots supply expectations. |
|14 | Location/range/SD scale100, variances10000, negative-frequency invariant; constant shift preserves dispersion. Numeric invariances do not authenticate units or economic comparability. |
|4 | None rejection; zero-fill changes mean; descriptive summary accepts finite−200% observation, while unlevered compounding rejects it. Numeric summaries do not establish the exposure model/domain. |
|44 | Six orderings of two−10% and two+10% returns share native summaries, cumulative−.0199 and geometric mean, with all24 native prefix products checked against external rational wealth. Supplemental temporal max drawdown spans.1 to.19 despite identical full-period summary/product. Source has no drawdown API. |
|18 | Four equiprobable n2 IID fair-sign histories: mean, sample variance, sample SD, negative frequency plus aggregate expectations. E[s²]=.01 equals population variance, while E[s]=sqrt(.02)/2≈.07071 differs from population SD.1. Explicit finite law, not an arbitrary bias correction or an assertion that real returns are IID. |
|3 | Prior source/listing identities and native absence of a date field. |

Relative5e−14 / absolute1e−15 tolerances cover float reporting. Exact path/probability and policy checks remain separate. Original fixture [.02,−.01,.03,0] has no supplied dates, currency, adjustment data or source authenticity; these remain unspecified. Omission, zero-fill and trimming are caller policies, not native imputation/outlier classification or approved data cleaning.

## Prompt/project assumption crosswalk

Answers1–18 retain prior arithmetic/quantile/shape/outlier/gross-product scope; new measurements test unit/shift/selection sensitivity without re-counting prompts. Answers19–22 retain explicit missing/singleton/scale/shift semantics and are exercised here. Answers23–24 distinguish cross-sectional/time-series units and annualized arithmetic approximation; identical numeric arrays cannot establish chronology, representativeness, stationarity or future return/loss calibration. No annual trading-calendar or forecasting claim.

The six mini-project deliverables retain the prior exact report/cumulative/geometric benchmarks and source/fixture/environment log. Numeric report export and an alternative extreme-value fixture exist; genuine instrument/date/adjustment provenance and rare-event adequacy do not. Prior test/workflow/answer totals remain historical and distinct from these predicates. No source fix was needed.

**Next:**15.2 location/quantile-definition/selection assumptions, then remaining15.3–15.7 descriptive/sampling obligations. V10/Book1 IN PROGRESS. F28 notebook/platform,F32 broader shared-input parsing/context/integration,F209/F165/F185 and resource/data/model/platform/release/independent/canonical acceptance remain open.
