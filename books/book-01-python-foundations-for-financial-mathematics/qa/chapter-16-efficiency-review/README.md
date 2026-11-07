# Section 16.12 — scoped efficient-grid and answer review

Baseline manuscript: `d6aaa30ae7fc8fd5fc2749d65d5e68a17f60b73b`. One core workflow, all 30 local answers and twelve lab steps reviewed. Predicates, workflows, answers and historical unique methods are separate inventories.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-efficiency-review/review.py
```

Reproduce unchanged-source failures (baseline must exist in Git history; expected nonzero exit writes `baseline.json`):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-efficiency-review/review.py d6aaa30ae7fc8fd5fc2749d65d5e68a17f60b73b
```

The observer extracts the exact Python reference fence, executes the printed demonstration and twelve existing unittest methods, checks silent import and executes the printed compileall command in isolation. Final `results.json`: three successful commands, 77 passing supplemental predicates, hashes, runtime/platform, raw output and independent rational/Decimal expectations and tolerances. No new historical unique methods.

## Baseline, policies and scope

`baseline.json` retains 15 failed predicates against unchanged source; the original twelve methods already passed. F153 corrects default tolerance erasure of small improvements/tradeoffs, implicit below-target acceptance, budget-residual amplification, integer expectation/Sharpe loss, overflow before a finite Sharpe ratio, invalid tolerances/candidate risks, malformed container exceptions and nonfinite/zero-underflow report contracts. One predicate labelled `PSD extension` adds full-matrix screening beyond the old correctly disclosed arbitrary-matrix limitation. No observer crash or failed corrected-source transition occurred in this batch.

Default dominance/target tolerance is now zero, with rational comparisons of supplied finite candidate metrics under a displayed-decimal policy. A candidate slightly below a requested return is not silently feasible. Explicit nonnegative positive tolerance retains an approximate option: it can allow a slight worsening of one criterion, is not necessarily transitive, and does not establish strict Pareto efficiency. Dominance's numerical tolerance applies separately in return and squared-return units; a business interpretation requires justified tolerances for those quantities. Target tolerance explicitly lowers the return requirement. Both exact-default and opt-in approximate branches are executed.

Candidate records need finite mean/nonnegative variance. Externally supplied records are not thereby proven feasible in any investment universe. Default filtering refers to the supplied reported candidate values, not hidden exact moments or a continuous feasible set. Duplicate equal points do not strictly dominate each other. Grid minimum ties prefer higher expected return.

`evaluate` uses integer/displayed-decimal rational intermediates and 80-digit Decimal roots; accepted budgets within 1e-10 are normalized. Every required float field must remain finite and preserve nonzero exact values or ValueError is deliberate. It reports both variance and SD, so an unreportable variance rejects the whole record. Displayed weights must reconcile to one. Sharpe is formed as an exact excess-return ratio before reporting, avoiding intermediate subtraction overflow or integer-offset loss.

The full covariance screen applies rational Schur complements to covariance plus delta times identity, delta=1e-10 times maximum diagonal; accepted asymmetric pairs are averaged, negative diagonals/nonzero zero-variance rows reject, and negative exact requested forms reject instead of clip. This numerical screen is not exact PSD/model certification. No grid result is presented as a continuous optimization guarantee.

## Independent mathematics and all 30 answers

Expected returns and variances are independently derived as functions of rational w: `mu=.04+.04*w`, `V=.04*w²+.09*(1−w)²`. The analytical identity `V=9/325 + .13*(w−9/13)^2` proves the continuous GMV for this model. Discrete Pareto weights follow the monotonic mean and quadratic variance over the specified grid. Sharpe values use independent squared rational ratios and high-precision roots, separately from the source excess-return division. Supplemental algebra, gross exposure and metadata are not extra source exports.

| Answers | Review and executed boundary |
|---|---|
| 1–3 | Source equal-weight mean .06, variance .0325, SD sqrt(.0325)≈.1802775638. |
| 4–6 | Source two-asset steps10 count11, three-asset steps4 count15 and nonnegative unit budgets; steps20 count21 also executed. |
| 7–10 | Source strict dominance, genuine tradeoff, equal-risk higher-mean dominance, equal-mean lower-risk dominance and identical nondominance checked. Tiny improvements and tradeoffs retained by exact default. |
| 11–13 | Supplemental continuous A weight9/13, variance9/325≈.0276923077, SD≈.1664100589. Source steps13 grid contains that allocation; source does not export a continuous optimizer. |
| 14–15 | Source steps20 target .07 selects A=.75, mean .07, variance .028125. Target .10 rejects long-only grid. Independent continuous inequality gives w≥.75. |
| 16–18 | Source Sharpe(.08,.2,.02)=.30; supplemental excess .06; zero-volatility source Sharpe rejects. Integer-offset and large finite ratio contracts also tested. |
| 19–20 | Adding a matched-horizon hypothetical zero-risk asset can change the feasible set; fixed-risk correlation stress raises risk. No source cash-allocation-line or borrowing/lending implementation. |
| 21–24 | Negative source weights reject; supplemental signed gross exposure1.4 is not a long-only feasible allocation. Steps20 count21, explicit grid-versus-continuous gap1/130000, and steps13 inclusion checked. No continuous-optimality acceptance of arbitrary grids. |
| 25–27 | Uncertain means, covariance validity and factor concentration reviewed; source global invalid-direction rejection tested under the added screen. No empirical forecast/rank/factor model accepted. |
| 28–30 | Costs can reduce modeled returns; source feasible rho.5/1 stress frontiers recomputed; untouched-period evaluation must avoid look-ahead. No turnover/cost engine or real out-of-sample dataset executed. |

## Twelve lab-step contracts

Prerequisites: long-only unit budget, matched asset ordering/currency/horizon, mean–variance criteria, quadratic risk, dominance and discrete versus continuous optimization. Inputs are fictional A/B with means [.08,.04], diagonal variances [.04,.09], covariance0, common hypothetical period and fictional USD. No actual dates, estimator window or calibration supplied.

| Step | Result and source boundary |
|---|---|
| 1 | Original moment model and long-only constraints fixed; actual source provenance unknown. |
| 2 | Source 21 candidates at .05 increments. |
| 3–4 | Every source candidate mean and variance checked against independent rational formulas; source SDs feed Sharpe calculation and base SD independently checked. |
| 5 | Source grid GMV weights [.7,.3], mean .068, variance .0277. |
| 6 | Supplemental analytical w_A=9/13, variance9/325; no standalone continuous optimizer exported here. |
| 7 | Variance gap .0277−9/325=1/130000≈.0000076923077. Steps13 source grid contains9/13. Changing resolution changes approximation, not the underlying moment model. |
| 8 | Source strict-default nondominated A weights [.7,.75,.8,.85,.9,.95,1], seven reported-grid candidates. Continuous frontier efficiency is a separate mathematical question. |
| 9 | Source strict target7% selects [.75,.25], variance9/320=.028125. Separate tiny-record probe rejects below-target default; explicit tolerance admits relaxed target as declared. |
| 10 | Source Sharpe at rf=.02 calculated for all21 candidates and checked against independent squared-ratio oracles. Grid maximum A=.85 differs from grid GMV=.7. Matched-horizon risk-free rate is hypothetical; no actual instrument/borrowing contract accepted. |
| 11 | Source means/variances held fixed, off-diagonal .03 (rho.5) then .06 (rho1). Grid GMV A weights .85,1; variances .038575,.04. Source grid-efficient sets retained in report. Models remain feasible but not empirical stress forecasts. |
| 12 | Grid resolution, strict/approximate policies, input/listing/source hashes, approximation gap, runtime and actual outputs retained. Corrected revision is containing commit. No actual as-of or unseen-period evidence. |

## Limits and resume checkpoint

Local Linux CPython standard library only. Exact source execution is separate from supplemental closed forms, numerical expectations, metadata and conceptual designs. No actual source timestamp/FX/NAV integration, continuous optimization acceptance, estimation accuracy, borrowing/costs, production performance/conditioning, platform coverage, independent reviewer acceptance or certification. F28 notebook/platform, F32 broader shared-input integration and newer unresolved findings remain open.

Chapter 16 now records twelve core workflows and 336 local answers within scope. Next: Section 16.13 — Portfolio Constraints.
