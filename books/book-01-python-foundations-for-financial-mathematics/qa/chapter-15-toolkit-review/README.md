# Section 15.14 — scoped toolkit project, labs and answer review

Baseline manuscript: `ee09d3a84d42421e2559efef36db1fe17dfdb867`. Scope: one core workflow, 24 local answers, six lab phases / 32 step records, seven project-deliverable records and twelve readiness-domain records. These are not unique test-method counts.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-15-toolkit-review/review.py
```

The observer extracts both Python fences and the exact CSV fence. It executes the unchanged main demonstration and twelve existing unittest methods, the unchanged CSV usage script against that fixture, a silent import and the printed compilation command in an isolated directory. Four command checks pass; the CSV example is separately recorded, not silently rewritten. The numerical observer imports the main fence for 62 supplemental predicates, all passing. No historical unique methods added. `results.json` retains Python/platform, source/main/helper hashes, raw output, expectations, tolerances and scope metadata. `prices.csv` preserves the exact fixture; `report.json` is the source report.

`observer-initial.py` and `observer-initial.json` retain an observer failure before any manuscript changes: Fraction(float_numerator,float_denominator) is invalid. The corrected oracle independently parses displayed decimal floats to individual Fractions and divides them. The corrected observer was rerun on unchanged baseline source; `baseline.json` retains nineteen failed predicates. They are reproducible with the same runner and baseline manuscript above. All twelve existing methods and all four commands already passed on baseline. The observer error is not a manuscript defect.

F140 corrects lost integer price increments and sample/regression spread, moment/Pearson overflow or underflow, decimal constants accepted as variable, wrong decimal tail count, false total-loss rounding, nonfinite compound outputs, collapsed positive-width CIs and rounding a valid near-one confidence request to a CDF endpoint. The loader now rejects invalid/noncanonical calendar dates, missing/duplicate schema columns, ragged/extra-value rows and invalid prices with explicit ValueError. Canonical integral CSV prices retain integers; nonintegral decimal prices convert to representable floats. Calendar validation does not establish actual exchange-session alignment or as-of availability.

Rational intermediates use integers or displayed decimal floats; roots and CI arithmetic use 80-digit Decimal before float reporting. Every nonzero reported output must remain finite/nonzero, and false −100% wealth rounding is rejected. OLS uses an explicitly documented R²=1 perfect-fit convention for constant responses, where the usual variance fraction is undefined. The report is deliberately fail-fast for undefined required dependence/regression, not an independently accepted partial-report API. Educational policy only; no binary-float compatibility or performance claim.

## Independent numerical expectations and all local answers

Return expectations use rational price ratios. Sample moments use pairwise differences, independently of source centered sums. OLS expectations use covariance/variance identities with independent rational sums and residual reconstruction. CI endpoints use independently evaluated Decimal SE and the declared 95% normal critical value; the near-one confidence probe checks construction/range, not independent critical-value accuracy.

The five-price fixture yields four asset returns, mean .012376251759956122, SD .016720680640921515, cumulative .05 and correlation .9544585794527587. Regression alpha≈−.0016242215226564846, beta≈.9472792795880587, R²≈.9109911798909782 and SSE≈.00007465556782151252. Normal CI≈[−.004009714166645016,.02876221768655726]; alpha=.05 tail count one gives signed VaR=ES≈.009708737864077669. None of these tiny-sample diagnostics establishes forecasting or tail coverage.

| Local answers | Review and scope |
|---|---|
| 1–6 | Source mean .02, SD .01, covariance 2, Pearson 1, return .1 and compound −.01 checked. |
| 7–11 | All fixture w=2 means/CI endpoints, perfect example alpha=1, beta=2 and R²=1 checked. Source's twelve methods also retain CI-center and exact rolling-example coverage. |
| 12–14 | Source declared VaR .1 at alpha=.25 and ES .075 at alpha=.5 checked; n=20,w=5 gives 16 full windows by direct count. |
| 15–18 | Constant correlation rejected; nominal 95% critical and n=3 approximation limits reviewed. Positional pairing cannot prove matching market-session timestamps. |
| 19–21 | Split adjustments, feature availability and Bonferroni .05/20=.0025 reviewed conceptually; toolkit has no corporate-action/as-of/multiplicity implementation. No false source execution claim. |
| 22–24 | Conditional annualization .01√252, net-of-cost economic relevance and reproducibility records reviewed. No actual capacity, execution-cost or independent acceptance evidence. |

The tail estimator remains negative nearest-rank left-return quantile with ceil-count ES; it is not necessarily direct nearest-rank loss quantile at 1−alpha. Signed thresholds are unfloored. Quantile definition and small-sample instability remain explicit.

## All 32 lab steps

| Phase/steps | Executed work and limits |
|---|---|
| A1–A3 | Exact CSV fixture retained and loaded by exact usage fence. Five canonical increasing unique ISO dates verified; fictional USD/raw prices, no dividends/splits supplied. |
| A4–A6 | Zero price and duplicate date rejection executed; nine CSV invalid-input cases include invalid dates/schema/row shape/nonfinite prices. Adjustment convention documented, not validated against a feed. |
| B1–B2 | Both return arrays and asset mean/SD recomputed through source, compared with rational benchmarks. |
| B3–B4 | Cumulative source return .05 versus mean .01237625 per observation; these have different horizons. Reference now uses rational gross products rather than claiming log1p/expm1 implementation. |
| B5 | Separate stress [.01,.02,−.50,.03] gives source cumulative −.469447, independently rational. It does not replace or corrupt the price fixture. |
| C1–C3 | Source covariance/Pearson and OLS exercised; all regression report fields independently checked. |
| C4–C5 | R² is association, not causation; serial dependence invalidates naive classical inference. Conceptual review only, no robust/HAC estimates. |
| D1–D3 | Both source normal CI endpoints, signed VaR/ES/count checked. Four returns do not justify a generic asymptotic model. |
| D4–D5 | alpha=.05, ceil-count left-return convention and one-observation tail documented; no rare-event model adequacy accepted. |
| E1–E2 | All three w=2 means and both w=3 means checked; lengths 3/2 equal n−w+1. |
| E3–E5 | Warm-up and trailing ending labels reviewed; close-t data cannot support an earlier decision. Actual feed release/venue execution timing unavailable. |
| F1–F2 | Corporate actions and historical constituent/delisting requirements recorded; synthetic fixture provides no actual reconciliation or universe reconstruction. |
| F3–F4 | Publication/availability, missing data and quote freshness remain external-data requirements. No invented timestamps or audit completion. |
| F5–F6 | Complete variant ledger and chronological untouched holdout/net-of-cost evaluation are required designs. This tiny provided fixture is not real research evidence or an executed operational backtest. |

Input prerequisites: standard-library Python, at least four prices/three returns, variable benchmark/asset for required dependence outputs, explicit units, adjustment policy and upstream timing alignment. Exact numeric helper/CSV execution is separated from supplemental report assembly and conceptual audit/inference design.

## Seven deliverables and twelve readiness domains

| Deliverable | Evidence |
|---|---|
| 1 CSV | `prices.csv`, exact source fence hash. |
| 2 implementation | Canonical manuscript main listing and `review.py` extractor; exact transient runnable file executed, not a second independently authored implementation. |
| 3 report | `report.json`, exact source results. |
| 4 assumptions/data-quality register | Lab and limits tables here plus metadata in `results.json`. |
| 5 test log | `baseline.json`, `results.json`, retained observer failure and exact commands. |
| 6 interpretation | Descriptive mean/volatility/dependence/OLS above; no investment/causal conclusion. |
| 7 unresolved risks | Limits below and readiness-domain table. |

| Readiness domain | Scoped status |
|---|---|
| Provenance | Fictional source hash retained; real source/adjustments unresolved. |
| Alignment | ISO/row validation executed; exchange clocks/calendars unresolved. |
| Mathematics | Rational/Decimal scoped benchmarks passed; independent acceptance pending. |
| Reproducibility | Exact fences, input hashes, runtime and commit retained. |
| Numerical stability | Recorded edge cases passed; no exhaustive proof. |
| Security | Schema rejection exercised; production storage/security review unperformed. |
| Performance | No representative-data benchmark. |
| Observability | Command logs/errors retained; no deployed monitoring. |
| Bias control | Design review; no real-universe/feed acceptance. |
| Inference | Assumptions explicit; no model/coverage calibration. |
| Change management | Atomic publication/checkpoint; named independent approvals absent. |
| Acceptance | Scoped execution evidence only; NOT_CERTIFIED. |

## Limits and resume checkpoint

Local Linux CPython only. F28 notebook/platform, F32 broader shared-input integration and other unresolved findings remain open. One source end-to-end fixture does not establish book-wide integration. No external-platform execution, real-data/production acceptance, independent reviewer acceptance, exhaustive branch proof or certification. Chapter 15 now records fourteen workflows and 336 local answers reviewed; chapter-wide assessment remains pending. Next: Section 15.15 — Exercises and Applied Problems.
