# Section 16.9 — scoped two-asset opportunity-set review

Baseline manuscript: `5736591d5e2ca387e983362c1a2556398c5ee913`. One core workflow, all 30 local answers and twelve lab steps reviewed. Predicate, workflow, answer and historical unique method counts are separate.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-two-asset-review/review.py
```

Reproduce unchanged-source failures (baseline must exist in Git history; expected nonzero exit writes `baseline.json`):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-two-asset-review/review.py 5736591d5e2ca387e983362c1a2556398c5ee913
```

The observer extracts the exact Python reference fence, executes the printed demonstration and twelve existing unittest methods, checks silent import and executes the printed compileall command in isolation. `results.json` records three successful commands, 85 passing supplemental predicates, runtime/platform, hashes, raw output and independent rational/Decimal expectations and tolerances. No new historical unique methods.

## Initial failures and correction

`baseline.json` retains 16 failed predicates against unchanged source; the twelve original methods already passed. F150 corrects absolute floors that erased small positive optimizer denominators or distinct means, large-scale squared overflow, falsely nonunique near-identical models, the both-zero-volatility degenerate case, integer expected-return/target precision, huge exact hedge intermediate overflow, nonboolean policies, nonfinite/zero-underflow output handling, unreconcilable displayed budgets and huge integer exception contracts. No observer crash or failed final-source transition occurred in this batch.

Integer/displayed-decimal rational intermediates precede 80-digit Decimal roots and final reporting. Exact zero denominator/equality decides mathematical degeneracy under this input policy; no fixed absolute cutoff turns a small but distinct model into identical assets. Both zero volatilities are degenerate for any allowed rho. Economic conditioning remains poor for nearly indistinguishable estimates despite exact arithmetic.

Inputs require nonnegative finite SDs and rho in [-1,1], which defines a valid two-asset PSD covariance model. Policy controls must be booleans. All required float fields must be finite and preserve exact nonzero values. Since `portfolio` returns both variance and volatility, an unreportable variance rejects the entire result even if SD alone is representable. Optimizer/target APIs return only their requested weight/note, so their weights can be reportable when a subsequent portfolio's variance is not. Reported w and 1−w must reconcile to one within absolute 1e-10; very large signed weights that destroy displayed unit budget reject rather than imply a fully invested report.

## Independent expectations and all 30 answers

The observer independently expands rational two-asset quadratics, solves first-order conditions and verifies the complete-square identity. For the ideal main rho=1/6, covariance c=.01, `V(w)=7/220 + (11/100)*(w−8/11)^2`; this proves the global unconstrained minimum and, because 8/11 is feasible, the long-only minimum. Roots use 80-digit Decimal. Actual Python input `1/6` is the displayed decimal .16666666666666666; the tiny difference from ideal rational 1/6 is covered by the explicit 1e-12 relative comparison tolerance. Source execution and supplemental algebra/metadata are distinct.

| Answers | Review and executed boundary |
|---|---|
| 1–4 | Source main w=.6 expected return .064, variance .0336, SD≈.1833030278. Supplemental covariance .2*.3/6=.01. |
| 5–9 | Source endpoints recover means/variances; equal-.2-SD 50/50 correlation 0,+1,−1 gives variance .02,.04,0. |
| 10–11 | Source target .07 for means [.09,.05] gives w=.5; target .12 rejects long-only but gives 7/4 with explicit unconstrained policy. |
| 12–14 | Separate rho0 model: source A weight9/13, B4/13, minimum variance9/325≈.0276923077 and SD≈.1664100589. This differs from the main rho1/6 model. |
| 15–16 | Source [.1,.2] SD/rho1 long-only optimum A=1. Identical [.2,.2]/rho1 returns nonunique; both zero SDs also nonunique. Distinct near-equal parameters are not collapsed. Unconstrained [.2,.3]/rho1 weight3 is separately tested. |
| 17–20 | Source correlation sensitivity .03, explicit signed expected return .11 before costs, complementary weight .7 for w=.3, and 11 inclusive grid points. |
| 21–22 | Efficient-branch answer clarified for unequal means, interior minimum and feasible set. With μA>μB, w<w* has lower expected return and greater variance than w*, so is dominated; w≥w* has increasing risk/return. Boundary/equal-mean cases differ. Dominance and full-curve conclusions are mathematical reviews, not a source efficiency-classification export. |
| 23–24 | Zero correlation does not imply independence, and estimated moments make the frontier uncertain. No distribution/estimation calibration accepted. |
| 25–27 | Current-weight drift, consistent return horizon and annualization assumptions, and net-cost effects reviewed conceptually. No rebalance, cost or annualization engine implemented here. |
| 28–30 | Linear covariance may omit option nonlinearities; common base-currency returns required; small-sample estimation can destabilize optimizer. No full revaluation, FX adapter or empirical uncertainty analysis executed. |

## Twelve lab-step contracts

Prerequisites: fixed beginning weights, consistent asset order/horizon/base currency, means/variance/covariance, differentiation, constrained versus unconstrained allocations and ideal population-moment inputs. Fixtures are fictional A/B in one shared hypothetical period and common USD, using decimal simple-return means/SDs. No dates, sample size or actual estimate availability are invented.

| Step | Executed result and limit |
|---|---|
| 1 | Main means [.08,.04], SDs [.2,.3], rho displayed `1/6`; synthetic shared units/horizon/currency fixed. |
| 2 | Supplemental ideal covariance .01. |
| 3–4 | Source main w=.6 return .064, variance .0336, SD≈.1833030278. |
| 5–6 | Source 11-point w=0,.1,…,1 grid; every expected return and variance checked against independent rational expressions. |
| 7 | Main source discrete minimum w=.7, variance .0319. |
| 8 | Main source analytical A weight≈8/11, B3/11, variance7/220≈.0318181818. No confusion with the separate rho0 worked example. |
| 9 | Discrete risk no lower than analytical risk; independent complete-square identity verified for all grid points, with its algebra proving the continuous minimum. |
| 10 | Source main-means target .06 gives A=.5. Separate exercise target .07 uses means [.09,.05], also A=.5 for different inputs. |
| 11 | Repeated source rho0,+1,−1 profiles: analytical weights9/13,1,.6; grid minima .7,1,.6; corresponding analytical variances9/325,.04,0. All retain original means and SDs. Ideal rho−1 hedge has no guarantee of real persistence. |
| 12 | Labelled fixtures, policies, input/source/listing hashes, runtime and actual outputs retained. Corrected source revision is containing publication commit; baseline above. |

## Limits and resume checkpoint

Local Linux CPython standard library only. Exact source commands/functions are separated from supplemental covariance/complete-square formulas, independent numerical expectations, synthetic metadata and conceptual financial designs. No actual source timing/FX/NAV integration, estimation accuracy, turnover/costs/financing, production conditioning/performance, platform coverage, independent reviewer acceptance or certification. F28 notebook/platform, F32 broader shared-input integration and newer unresolved findings remain open.

Chapter 16 now records nine core workflows and 246 local answers within scope. Next: Section 16.10 — Multi-Asset Portfolios.
