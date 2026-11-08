# Section 16.15 — scoped portfolio engine project review

Baseline manuscript: `a9ba6216c0791e017ac255744772c68fbf95a4ee`. One project/core workflow, all 30 local worked answers, twelve lab steps and twelve separate project-checklist records reviewed within the limits below. These inventories are separate from test predicates and historical unique methods.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-engine-review/review.py
```

Reproduce unchanged-source failures (requires baseline in Git history; intentionally exits nonzero and writes `baseline.json`):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-engine-review/review.py a9ba6216c0791e017ac255744772c68fbf95a4ee
```

The runner extracts the exact reference Python fence, runs the printed demonstration and twelve existing unittest methods, checks silent import and executes printed compileall in isolation. Final `results.json`: three successful commands, 80 passing supplemental predicates, source/listing/input hashes, raw output, runtime/platform and independent rational/Decimal expectations and comparison tolerances. No new historical unique methods.

## Initial failures and corrections

`baseline.json` retains 25 failed predicates against unchanged source; all twelve original methods already passed. F156 corrects the three marginal-variance answers (factor two), implicit relative budget tolerance and residual amplification, integer expectation/sample centering loss, moment overflow, tiny drift-return loss, large-NAV turnover denominator overflow, stress multiplication overflow/zero-multiplier masking, tiny cap breach acceptance, missing cap-weight validation, malformed/huge-input contracts and unreportable/false-total-loss output handling. One predicate explicitly labelled PSD extension adds full-matrix screening beyond the original correctly disclosed limitation. No observer crash or failed corrected-source transition occurred in this batch.

Exercises13–15 had called Sigma-w components [.0218,.03,.00008] marginal variance. The unconstrained derivative of V=wᵀSigma*w is twice Sigma-w: [.0436,.06,.00016]. The corrected prompts distinguish this from a budget-preserving directional derivative, and retain Sigma-w coefficients for the unchanged variance-contribution calculations. Text alignment and independent derivatives recovered from source VC/weight are both checked; no source gradient export is claimed.

Integer/displayed-decimal rational intermediates and 80-digit Decimal roots precede float output. Every required field must be finite and preserve nonzero exact values or ValueError is deliberate. Required report fields include variance and all applicable contributions, even if another field alone would be representable. Displayed VC and RC vectors must reconcile to variance/SD within relative1e-10 without absolute floor. At zero risk, volatility attribution remains None.

Arithmetic weights within absolute1e-10 of unit budget normalize before use. Cap auditing validates the supplied long-only near-unit budget but checks those supplied weights without normalization under strict cap comparisons, matching Section16.13's auditing convention. Portfolio return is formed directly, and positive wealth that would round to a −100% return rejects. Frictionless turnover is formed from weight changes before dollar conversion; reported trade cash sums must reconcile within1e-12 times gross volume.

The full rational Schur-complement screen tests covariance plus delta*I, delta=1e-10 times maximum diagonal, symmetrizes accepted within-tolerance pairs and rejects negative diagonals/nonzero zero-variance rows. Requested negative exact forms reject, not clip. Stress validates the original model before scaling covariance by k². This is numerical screening, not exact PSD/model or economic certification.

## Independent mathematics and all 30 local answers

Weighted means, quadratic expansion and contributions use independent rational formulas. Historical covariance uses the pairwise-difference identity `sum(i<j)(x_i−x_j)*(y_i−y_j)/(T*(T−1))`, separately from source centering. Roots and signed contribution magnitudes use 80-digit Decimal expectations. Fixture means, covariance-weighted exposures, derivative reconstruction, dollar NAV and metadata are supplemental, not additional engine exports.

| Answers | Review and execution boundary |
|---|---|
| 1–6 | Budget1; source expected return .059; supplemental mean contributions [.04,.015,.004]; matching3x3 dimensions, symmetry and diagonal [.04,.09,.0004] reviewed. Real asset-ID inference is not implemented. |
| 7–12 | Supplemental diagonal [.01,.0081,.000016] and cross .0018 reconcile to source variance .019916 and SD≈.1411240589. |
| 13–15 | Corrected unconstrained partial variance derivatives [.0436,.06,.00016]; Sigma-w=[.0218,.03,.00008] remains the half-gradient. Not derivatives through normalization or a constrained rebalance direction. |
| 16–20 | Source VC=[.0109,.009,.000016] and RC=VC/sqrt(.019916) checked individually and reconciled to total variance/SD. Zero-risk RC remains undefined (None). |
| 21–23 | Written [1,2,3]/[2,4,6] source sample covariance2; explicit three-asset common-sample estimator checked separately. Timestamp/horizon alignment and missingness rules reviewed; no actual join/imputation engine. |
| 24–25 | Separate source 50/50, returns [.1,0] yields .05 return and weights[11/21,10/21]; supplemental NAV100→105. |
| 26–28 | Separate written source [.4,.6]→[.5,.5] at NAV100 gives trades[10,−10], turnover.1, gross20. The source-executed drift-to-rebalance chain instead uses NAV105 and gives trades[−2.5,2.5], turnover1/42, gross5. |
| 29–30 | Source original caps[.6,.4,.3] pass; caps[.4,.4,.3] fail. Common SD multiplier2 keeps mean unchanged, multiplies source variance/VC by4 and SD/RC by2. No correlation-breakdown or nonlinear stress claim. |

## Twelve project lab steps

Prerequisites: consistent asset order/base currency/return horizon, long-only beginning budget, means/covariance, complete asset-major historical samples, risk attribution, simple-return/no-flow drift and frictionless trades. Synthetic original forecast, historical estimator and separate two-asset realized-return models are labelled rather than equated.

| Step | Result and boundary |
|---|---|
| 1 | Exact Python listing executed with retained runtime/platform; standard library only. |
| 2–4 | Original fictional A/B/cash-like C: w=[.5,.3,.2], mu=[.08,.05,.02], covariance[[.04,.006,0],[.006,.09,0],[0,0,.0004]], common hypothetical period/USD. No actual dates/estimator vintage. |
| 5–7 | Source report .059 mean, .019916 variance, .1411240589 SD with individually verified/reconciled variance/volatility contributions. |
| 8 | Separate histories A=[.01,−.01,.02,0], B=[.02,0,.03,−.01], C=[.001]*4 at four common fictional labels, no missingness/imputation. Source sample covariance=[[1/6000,1/5000,0],[1/5000,1/3000,0],[0,0,0]]. Supplemental means [.005,.01,.001] plus source sample covariance feed source report, giving mean .0057 and variance79/600000. This is not original forecast .059 or original nonzero C variance .0004. |
| 9 | Separate two-asset source drift fixture starts NAV100, [.5,.5], [.1,0]; source returns .05 and weights[11/21,10/21]. |
| 10 | Source drift output directly feeds source rebalance at NAV105 to target50/50. Trades[−2.5,2.5], gross5, turnover1/42, within reporting tolerance. No fees, orders or fills. |
| 11 | Deliberate original-model cap breach detected; original static model stressed with k2, variance .079664 and SD≈.2822481178. These are counterfactual model checks, not new forecasts inferred from historical/drift fixture. |
| 12 | Three command checks, twelve existing tests, all predicates, hashes, raw outputs and limits retained. Corrected revision is containing publication commit. |

## Twelve separate project-checklist records

These map manuscript criteria to scoped local evidence; the broad acceptance checkboxes are not treated as enterprise or independent approval.

| Criterion | Scoped result and limit |
|---|---|
| 1 IDs/dimensions | Fictional ordered A/B/C labels and3x3 input checked; actual security mapping/source provenance unexecuted. |
| 2 budget/long-only | Original unit budget and nonnegative weights executed; malformed/budget/cap-weight probes recorded. |
| 3 expectation | Source .059 and independent weighted sum agree. |
| 4 variance/SD | Source .019916/sqrt(.019916) agree with independent expansion/root. |
| 5 VC sum | Source VC individually and in sum checked. |
| 6 RC sum | Source RC individually and in sum checked; zero-risk None separate. |
| 7 sample covariance | Source T−1 estimator agrees with independent pairwise oracle on explicit common fixture; no real timestamp audit. |
| 8 drift weights | Source positive-NAV drift sums to unit budget; exhausted/false-total-loss cases tested. |
| 9 rebalance | Source frictionless signed trades/gross/turnover reconcile; no cost/fill/settlement accounting in this engine. |
| 10 caps | Source ordinary and deliberately breached caps checked; no real mandate approval. |
| 11 stress | Source2x SD scaling and4x variance/VC scaling checked, mean fixed. |
| 12 actual results | Commands/output/runtime/hashes retained for containing revision; independent reviewer/platform acceptance remains open. |

## Limits and resume checkpoint

Local Linux CPython standard library only. Source implementation is separate from supplemental algebra/metadata and conceptual production-hardening items. No actual asset IDs/timestamps, market ingestion/as-of estimate vintage, FX/NAV/financing, costs/taxes/external flows, constrained optimizer, settlement/orders/fills, unseen-period strategy evaluation, production conditioning/performance, platform coverage, independent reviewer acceptance or certification. Local historical-moment→report and drift→rebalance chains do not close F32 broader shared-source integration. F28 notebook/platform and newer unresolved findings remain open.

Chapter16 now records fifteen core workflows and426 local answers within scope, including this project. Next: Section16.16 — Exercises and Applied Problems.
