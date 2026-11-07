# Section 16.4 — scoped expected-return lab and answer review

Baseline manuscript: `30b37cbd7f4f3d845978a420b988f19aee799504`. One core workflow, 24 local answers and twelve lab-step records reviewed. Predicate, workflow, exercise and historical unique method counts remain separate.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-expectation-review/review.py
```

The observer extracts the single exact Python fence, executes the printed demonstration and twelve existing unittest methods, checks silent import and runs the printed compilation command in isolation. Three commands and 47 supplemental predicates pass in `results.json`; no historical unique methods added. Runtime/platform, hashes, raw command output, rational/Decimal expectations/tolerances and model outputs are retained.

`baseline.json` retains twelve failed predicates against unchanged baseline source above, reproducible with this runner and that revision. All twelve original methods passed before correction. `reference-test-transition.json` retains the numerical-correction rerun: all 47 supplemental predicates passed, while embedded test_08 still expected the float artifact .30000000000000004 for historical mean [.2,.4]. Under the declared displayed-decimal policy the correct reported mean is .3; that expected value was corrected within the same existing method. Restoring its old expected list in corrected source reproduces the transition failure. No new historical test method was counted.

F145 corrects overflow before signed weighted cancellation, integer forecast errors lost by coercion, historical averaging overflow, probability residuals biasing constant means/variances, zero-mass/rare-large scenario second moments overflowing before weighting, and silently nonfinite forecast-error/variance outputs. Accepted weight budgets and nonnegative probability masses within the 1e-10 tolerance are explicitly normalized; invalid sums remain rejected. This restores unit mass, exact constant-scenario variance zero and consistent scenario routes. Rational intermediates use integer/displayed-decimal inputs; roots use 80-digit Decimal before final float reporting. Every required output field must remain finite and nonzero if its exact value is nonzero; otherwise ValueError is deliberate, even if a different field such as SD would be reportable.

Scenario distributions now default consistently to long-only weights; signed distributions require explicit allow_short=True and still do not establish financing/margin treatment. The recorded default-rejection probe covers that policy boundary; it is not generic signed-strategy acceptance. Invalid policy flags and malformed scenario outer shapes now have explicit ValueError contracts. These educational policies are not binary-float compatibility or performance claims.

## Independent benchmarks and all local answers

Weighted means are independently rational sums. Scenario variance uses the pairwise identity Σ(s<t)p_s*p_t*(R_s−R_t)² for normalized probability mass, independently of the source centered-square algorithm. The rare-large-scenario probe demonstrates that a weighted variance can be finite even when an unweighted squared deviation exceeds float range; zero-probability rows still require finite data but contribute no second moment.

| Answers | Review and source boundary |
|---|---|
| 1–7 | Source expected returns .064,.05,.058,.03,.048,.11,.07 checked for the declared weights/means, including explicit signed one-period permission. |
| 8–13 | Probabilities [.25,.75], source asset means .05/.075, separate equal-weight portfolio mean .0625, symmetric ±.10 scenario variance .01 and SD .10 checked. Scenario variance is probability-weighted population variance, not n−1 sample variance. |
| 14–15 | Source historical mean .20 and forecast error .02−.05=−.03 checked. Integer-offset forecast errors additionally tested without coercion loss. |
| 16–19 | Survivorship, uncertain forecasts, fixed-weight linearity and covariance not being needed for the mean reviewed mathematically/conceptually. No empirical expectation or independence calibration accepted. |
| 20–22 | Random/dynamic weights need conditional modeling; arithmetic .12 differs from deterministic (1.01)^12−1≈.1268250301. This annualization is a supplemental derivation, not an exported source function or random-return product-expectation forecast. |
| 23–24 | Cash-like mean requires common horizon/currency, and training/untouched evaluation must be chronological. No risk-free certification, actual timestamped forecast or market holdout supplied. |

The lab now distinguishes three models rather than implying different inputs must give identical results: original [.08,.04,.02] forecast, alternative three-asset economic scenarios, and a separately labelled historical-A substitution. Linearity is checked only between two routes within the same scenario model.

## Twelve lab steps and model/timing contracts

| Step | Executed evidence and limit |
|---|---|
| 1–3 | Fictional A/B/cash-like C, common USD, hypothetical one-period simple returns; initial weights [.5,.4,.1], original means [.08,.04,.02]. Synthetic t0 forecast/t1 outcome labels; real dates/availability unknown. |
| 4 | Source original expected return .058; independent contributions [.04,.016,.002]. No source contribution function exported here. |
| 5 | Separate scenario model fixed as probabilities [.25,.75], rows [[.20,0,.02],[0,.10,.02]], retaining the third cash-like column. |
| 6 | Source scenario-implied asset means [.05,.075,.02] checked. |
| 7–8 | Source scenario portfolio returns [.102,.042] give .25(.102)+.75(.042)=.057; source weighted asset-mean route also .057. Independent scenario variance .000675 and SD≈.0259807621 checked. Original .058 forecast and separate two-asset Section 4 .0625 example retain their distinct assumptions. |
| 9 | Source historical A mean of [.10,.30] is .20. Retaining B=.04/C=.02 yields separately labelled source weighted estimate .118. Two observations do not establish forecast stability. |
| 10 | Hypothetical realized portfolio return .02 compared only with preserved original .058 forecast; source error −.038. No post-hoc switch to another model. |
| 11 | Estimation uncertainty, regime change, survivor/as-of leakage and dynamic weights reviewed conceptually. No empirical forecast-error distribution, SE calibration or actual source-timing audit. |
| 12 | Input hash, units, probabilities, model labels/versions, source/listing hashes, runtime, baseline failures, transition failure and results retained. Corrected revision is the containing commit. |

Prerequisites: Python sequences/functions, expectation/variance, a complete fixed-weight budget, valid scenario mass and common return horizon/currency. Exact source functions/commands are execution evidence. Model assembly, rational contributions, pairwise variance, annualization and synthetic timing metadata are supplemental; forecast suitability, data provenance, financing and economic/independent acceptance remain conceptual/unexecuted. Standard library only.

## Limits and resume checkpoint

Scoped local Linux CPython only. F28 notebook/platform, F32 broader shared-input integration and other unresolved findings remain open. No external-platform run, exhaustive branch proof, actual market calibration, independent reviewer acceptance or certification. Chapter 16 now records four workflows and 96 local answer records reviewed. Next: Section 16.5 — Covariance Matrices.
