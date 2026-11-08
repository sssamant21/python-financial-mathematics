# Section 17.7 — scoped portfolio optimization review

Affected baseline: `407c3bed9a3b8eb1fb04f2e957591c9baa34163d`. Finding F164, severity medium (educational numerical correctness), owner Book 1 manuscript maintainers; decision repair exact feasibility/PSD/scale handling and clarify finite report/grid limits. Reviewer: automated source execution and mathematical/prompt/step review, not external independent acceptance. Corrected revision is the containing publication commit.

One workflow,40 local answers,twelve lab steps and twelve separate acceptance-control records are distinguished from four exact-source commands,55 supplemental predicates and twelve existing unittest methods. Zero historical unique methods added. [results.json](results.json) records raw stdout/stderr, actual values/tolerances, lab fixtures, Python/platform/NumPy/SciPy versions and source/listing SHA256.

From repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-portfolio-review/review.py
```

Reproduce unchanged source (expected nonzero exit; requires history):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-portfolio-review/review.py 407c3bed9a3b8eb1fb04f2e957591c9baa34163d
```

[baseline.json](baseline.json) retains eleven failed predicates. The original twelve methods and SciPy snippet already passed. Defects include tiny-scale false nonuniqueness, a singleton marked nonunique, overflowing Sharpe numerator despite a finite ratio, hard-cap/target infeasibility hidden by tolerance for both mean-slope signs, tiny/huge invalid PSD or asymmetry, malformed-input exception contracts and silently erased positive risk. Eleven predicates are not eleven distinct defects. No observer failures occurred. Strict reported-cap/target/interval checks and diagnostic fields are disclosed reporting contracts, not broad financial approval.

## Exact-source execution and independent model

Verbatim reference demonstration/tests, silent import and compilation execute in an isolated temporary directory. A fourth command executes the verbatim NumPy/SciPy SLSQP snippet with printed output retained. A separate unchanged-snippet execution in a namespace supports four supplemental checks against analytic capped weights, rational objective and explicit bounds/budget. No supplemental optimizer replaces reference execution.

Fictional asset order[A,B], compatible single-period means[.08,.04], covariance diag(.04,.09), risk-free return.02. Weights dimensionless, variance squared-return, volatility/means/risk-free same return horizon; no market/as-of observations. Equal-weight mean3/50=.06, variance13/400=.0325 and volatility sqrt(13/400). Independent derivatives give GMV A9/13,B4/13, mean22/325, variance9/325, volatility sqrt(9/325). The40% cap produces A2/5,B3/5, mean7/125=.056 and variance97/2500=.0388; cost of cap is361/32500 squared-return units.

Target.07 requires A≥(.07−.04)/(.08−.04)=3/4, giving variance9/320=.028125. Targets.04/.06 retain GMV; targets.07/.08 select.75/1. Reversing mean order reverses the target inequality; equal means require an explicit feasibility decision. Exact rational comparisons reject targets even slightly above the capped maximum, with no policy tolerance.

For positive-excess-return fixture, independent rational enumeration maximizes squared Sharpe over i/1000,i=0..1000. Winner871/1000 has score sqrt(((.04+.04w−.02)^2)/(.04w²+.09(1−w)²)); compare source score with100-digit Decimal sqrt. Continuous tangency normalizes Σ^-1(μ−rf1), giving A27/31,B4/31 and squared Sharpe17/180. Finite winner.871 is distinct from27/31. The grid is full long-only and has no caps/targets, so it does not inherit the lab's earlier40% mandate. A separate singular covariance case tests skipping one zero-risk endpoint; all-zero-risk grids reject rather than divide by zero.

Exact/displayed-decimal rational arithmetic precedes finite float reports. PSD/symmetry, target/cap feasibility and nonuniqueness have no absolute tolerance. Decimal100 square roots support volatility and grid score ordering; this is scoped numerical approximation, not arbitrary-conditioning/correct-rounding proof. Required nonzero report values must remain finite/nonzero or reject. Exact weights sum1; `reported_budget_residual` discloses float-display roundoff. Risk/return fields concern exact model weights. Rounded weights/intervals that violate hard caps/target reject conservatively; rejection need not mean mathematical infeasibility.

## Forty worked-answer records

| Exercise | Alignment and execution boundary |
|---|---|
| 01 | Budget complement B=.6 for A=.4 in source capped result. |
| 02 | Source equal mean3/50=.06. |
| 03 | Source equal variance13/400=.0325. |
| 04 | Source volatility versus independent Decimal sqrt(13/400)≈.18027756. |
| 05 | Supplemental exact covariance(.2)(.3)(.5)=.03. |
| 06 | PSD determinant implies covariance magnitude≤.06; source ordinary/extreme PSD rejections. |
| 07 | With zero covariance, fixture GMV variance9/325 is below.04 and.09; this depends on mixing and model. |
| 08 | Perfect positive correlation limits benefit; conceptual, not zero-risk claim. |
| 09 | Negative correlation can reduce risk; conceptual, not a forecast of stress behavior. |
| 10 | Source GMV A9/13 independently derived. |
| 11 | Source complement4/13. |
| 12 | Source GMV expected return22/325=.88/13. |
| 13 | Source GMV variance9/325. |
| 14 | Source GMV volatility sqrt(9/325)≈.16641006. |
| 15 | Source capped A.4; unconstrained9/13 violates cap. |
| 16 | Source capped variance.0388. |
| 17 | Source capped mean.056. |
| 18 | Source target.07 gives A.75 from exact affine inequality. |
| 19 | Source target variance9/320=.028125. |
| 20 | Source unreachable.10 target rejection; full-investment long-only average cannot exceed available means. |
| 21 | Source four-target frontier weight records retained, not a rendered frontier or complete empirical efficient set. |
| 22 | Equal risk/higher mean dominates under mean-variance preference; conceptual. |
| 23 | Source Sharpe(.08,.2,.02)=.3, plus finite ratio with overflowing naive numerator. |
| 24 | Source zero-volatility Sharpe rejects; zero-risk grid candidates explicitly skipped. |
| 25 | Compatible horizon required; no automatic annual/monthly conversion export. |
| 26 | TE²=(w−benchmark)^TΣ(w−benchmark) correct; conceptual, no tracking-error export here. |
| 27 | Supplemental exact information ratio.02/.04=.5. |
| 28 | Supplemental gross traded-notional.2×fee.001=.0002=2bps of NAV. Convention must be gross turnover for this answer. |
| 29 | Supplemental gross turnover.2; one-way convention.1 remains distinct. |
| 30 | Sector cap sums all sector weights; conceptual, source has only two individual caps. |
| 31 | [1.2,−.2] net1/gross1.4; conceptual, long-only model excludes it. |
| 32 | Source weight domain[0,1] encodes long-only. |
| 33 | Symmetric nonnegative-eigenvalue matrix is PSD; source exact two-asset determinant/symmetry checks. |
| 34 | Source identical-assets interval nonunique; singleton with caps.4/.6 correctly unique. |
| 35 | Mean-estimation sensitivity remains model risk; no actual estimation/backtest. |
| 36 | Shrinkage changes risk model and may stabilize estimation; conceptual, no estimator export. |
| 37 | Stressed covariance requires recomputation; scale probes here are numerical, not empirical stress analysis. |
| 38 | Prices cause drift; conceptual, no holdings/rebalance engine. |
| 39 | Future-return inputs create look-ahead; conceptual, no out-of-sample data exercise. |
| 40 | Ordered fixture, covariance/means/caps, versions, status, grid counts and checks retained; external approvals absent. |

## Twelve lab-step records

Prerequisites: Python, finite typed means/risk-free/weights, exactly symmetric two-asset PSD covariance, compatible period, valid long-only caps, reachable target, positive integer grid size. NumPy/SciPy installed for separate example. No notebook/platform installation or market-input acceptance is implied.

| Step | Actual evidence and scope |
|---|---|
| 1 | Exact reference saved/hashed in isolated directory; runtime recorded. |
| 2 | Source equal-weight mean/variance/volatility independently checked. |
| 3 | Independent derivative gives9/13 and4/13. |
| 4 | Source GMV weights/moments versus rational/Decimal expectations. |
| 5 | Source capA=.4 specified explicitly. |
| 6 | Source capped-minus-continuous-GMV variance versus361/32500. |
| 7 | Source target.07. |
| 8 | Source required A.75, negative-slope/equal-mean branches separately probed. |
| 9 | Source target risk.028125 versus GMV9/325; both records retained. |
| 10 | Source1000-subinterval full-grid maximum Sharpe versus rational finite-grid enumeration and distinct continuous bound; zero-risk candidate cases separate. |
| 11 | Invalid PSD/asymmetry, infeasible caps, unreachable targets and output limits reject as recorded. |
| 12 | Four commands,55 supplemental predicates and twelve existing methods pass; eleven baseline failed predicates retained. |

## Twelve acceptance-control records — not independent sign-off

| Control | Scoped disposition |
|---|---|
| 1 Universe/order | Fictional fixed[A,B] recorded; no real security-master reconciliation. |
| 2 Horizon/timestamps | Compatible hypothetical single period disclosed; no actual timestamps. |
| 3 PSD/symmetry | Executed two-asset exact checks, ordinary/extreme invalid cases. |
| 4 Mean assumptions | Explicit .08/.04 and reverse/equal cases; forecast validity unaccepted. |
| 5 Budget/bounds/sector | Budget model, caps and target exercised; sector rules absent; displayed budget residual disclosed. |
| 6 Independent moments | Rational/Decimal return/risk checks executed; exact and rounded-holding interpretations distinguished. |
| 7 Risk-free units | Same horizon.02 fixed; no conversion/data approval. |
| 8 Costs/turnover | Supplemental arithmetic only; no actual trade execution/cost model. |
| 9 Stress | Numerical scale/invalid-input probes only; economic correlation/mean stress remains pending. |
| 10 Out-of-sample | Conceptual leakage review only; no backtest or performance acceptance. |
| 11 Diagnostics | Exact source statuses, grid counts/spacing, commands/hashes; SciPy snippet status/assertions executed. |
| 12 Approvals/limits | Evidence and limits retained; external review/approval absent, not inferred from execution. |

## Limits and resume checkpoint

Local Linux CPython/NumPy/SciPy only; two assets and specialized covariance validation. No robust estimation, general multivariate/sector/turnover constraints, capped maximum-Sharpe solver, tracking-error export, trading-cost optimizer, market/calibration/backtest acceptance, arbitrary conditioning guarantee, production performance, platform/notebook or external reviewer certification. Exact source, supplemental derivations and conceptual controls are separate above. F28/F32 and all unresolved findings remain open.

Chapter17 has seven core workflows and275 local answers scoped. Next: Section17.8 — Numerical Integration; resume from fresh main without duplicating this batch.
