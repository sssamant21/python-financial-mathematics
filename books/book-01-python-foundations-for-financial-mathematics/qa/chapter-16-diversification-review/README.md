# Section 16.8 — scoped diversification lab and answer review

Baseline manuscript: `880945028862ef69c463abc320e4842b88128217`. One core workflow, all 30 local answers and twelve lab steps reviewed within the stated limits. Test predicates, workflow records, answers and historical unique methods are separate inventories.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-diversification-review/review.py
```

Reproduce unchanged-source failures (baseline must exist in Git history; intentionally exits nonzero and writes `baseline.json`):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-diversification-review/review.py 880945028862ef69c463abc320e4842b88128217
```

The observer extracts the exact Python reference fence, executes its printed demonstration and twelve existing unittest methods, checks silent import, and executes the printed compileall command in isolated temporary directories. Final `results.json`: three successful commands, 66 passing supplemental predicates, source/listing/input hashes, runtime/platform, raw output and independent expectations/tolerances. No new historical unique methods.

## Baseline, transition and scoped corrections

`baseline.json` retains 13 failed predicates against unchanged source; all twelve original methods passed. F149 corrects budget-residual amplification in variance/effective holdings, cancellation of tiny positive diversification benefit, premature variance conversion before SD, accepted out-of-bound generated correlations, covariance output overflow/underflow contracts, tiny negative-form clipping, huge integer exception handling and nonzero covariance rows for zero-variance assets. Three baseline predicates explicitly labelled `PSD extension` add full-matrix screening beyond the original correctly disclosed limitation; this is an acknowledged design-gap closure, not a previous false PSD guarantee.

`boundary-transition.json` retains a later corrected-source rerun with six failed predicates: generated N=4,7,12 theoretical lower endpoints were rounded just outside their own bound, and the exact requested form then rejected them. This is a source generation/reporting defect, not an observer crash. The final generator uses its reported diagonal and rounds negative endpoint entries inward when needed. Tiny positive variance can replace an ideal zero after float reporting; the observer independently checks the bound and permits only variance between zero and 1e-16 for the stated .2-SD fixtures. To reproduce the transition in a throwaway copy, replace the final generator block starting `variance=report(s*s)` with `return [[report(s*s*(1 if i==j else rho)) for j in range(n)] for i in range(n)]`, then run the observer. This reproduces the earlier declared exact-input generator policy before the reporting repair.

Integer/displayed-decimal rational intermediates, explicit normalization within 1e-10, 80-digit Decimal roots and finite/nonzero-preserving float output contracts are now explicit. Each API validates its requested outputs: SD may remain reportable when variance cannot be represented. Generated nonzero covariance entries that cannot be reported feasibly reject rather than silently become zero.

Benefit uses `(S²−q)/(S+sqrt(q))` with `S=sum(w_i*sqrt(v_i))`; its pairwise gaps `sqrt(v_i*v_j)−cov_ij` are also rationalized. This avoids subtraction of two already rounded SDs. Weights [1,1e-300], independent unit variances, produce a benefit approximately 1e-300 although both separately reported SDs round to one. The recorded rational reference differs only by terms of relative order 1e-300, well below the stated 1e-12 comparison tolerance. Ratio increments that cannot be distinguished from one in float are not claimed to be preserved.

Arbitrary covariance matrices receive a scale-relative full PSD screen on `matrix + 1e-10*max(diagonal)*I`, symmetry averaging within the stated tolerance, exact pairwise Cauchy bounds and a nonnegative exact requested-form check. This numerical screen is not exact PSD/model certification. Generated rho within 1e-12 of the mathematical bounds snaps to those bounds; farther excursions reject. For one asset, rho is unused but still validated under its declared bounds.

## Independent mathematics and all 30 answers

The source evaluates full quadratic sums; the observer independently uses the equicorrelation identity `s²*(rho+(1-rho)/N)`. Concentration uses rational sums of squared weights; roots use 80-digit Decimal. HHI, limiting-risk derivations and fixture metadata are supplemental, not extra source exports.

| Answers | Review and executed boundary |
|---|---|
| 1–4 | Source 50/50 equal-.2-SD scenarios rho 0,1,−1,.5 give variances .02,.04,0,.03 and corresponding independent roots. |
| 5–9 | Source weighted standalone SD .2; rho0 benefit .2−sqrt(.02)≈.0585786438, ratio sqrt(2); rho1 benefit0/ratio1; rho−1 zero-risk ratio rejects. Benefit is percentage-point SD reduction, not return premium. |
| 10–13 | Source equicorrelation models N=3/.3/rho0, N=10/.2/rho0, N=25/.2/rho0 and N=5/.2/rho.25 give variances .03,.004,.0016,.016 with independent roots. |
| 14 | Supplemental fixed-rho≥0 large-N limit gives variance .01 and SD .10 at s=.2,rho=.25. This is a limit, not a fabricated finite covariance matrix or empirical floor. |
| 15–18 | Supplemental HHI=.375 for [.5,.25,.25]; source effective holdings 8/3, four equal weights→4, [1,0,0]→1. Source has no separate HHI export. |
| 19–20 | Common-factor risk cannot be removed by name count alone; original two-asset rho0→.5→1 stress strictly raises executed SD. No actual factor/crisis calibration. |
| 21–22 | Base-currency return convention and horizon must match; signed weights need a different diversification convention and source long-only metric rejects them. No FX adapter or signed metric implemented. |
| 23–24 | Three-asset rho−.75 rejects (lower bound−.5); source symmetric rho−.5 matrix has zero equal-weight variance for the recorded fixture. Symmetry prerequisite checked separately. |
| 25–27 | Pairwise missingness may destroy a common PSD estimator; weights dimensionless but risk horizon explicit; hedges can lower total risk. These are mathematical/design reviews, not missingness/annualization/attribution exports here. |
| 28 | Source three equal capital weights give effective number3 while perfect-common-correlation model still has SD .2. Effective names are not independent risk count. |
| 29–30 | Recompute metrics after drift using current weights; low historical covariance does not establish tail protection. No rebalance, cost/tax engine or rare-joint-loss model executed. |

## Twelve lab-step contracts

Prerequisites: fixed long-only unit budget, covariance in matching asset order/currency/return units/horizon, correlation bounds and SD versus variance. Main synthetic fixtures are fictional A/B in common USD for one shared return period; no actual dates or sample window are invented.

| Step | Executed result and limit |
|---|---|
| 1–2 | Source rho1 matrix: SD .2, ratio1, benefit0. |
| 3 | Source rho.5: SD sqrt(.03)≈.1732050808, ratio≈1.1547005384, benefit≈.0267949192. |
| 4 | Source rho0: SD sqrt(.02)≈.1414213562, ratio≈1.4142135624, benefit≈.0585786438. |
| 5 | Source rho−1: SD0, benefit .2, ratio undefined and rejected. Idealized model, no risk-free guarantee. |
| 6 | Source benefits monotonically increase as correlation falls across the fixed two-asset fixtures. |
| 7 | Separate three-asset equal-.2-SD model with rho−.5 and weights [1/3]*3: source zero variance; rho−.75 rejects. Other generated lower endpoints N=4,7,12 are checked for safe inward float reporting. |
| 8–9 | Separate capital weights [.5,.25,.25], supplemental HHI .375, source effective holdings 8/3 versus three names. |
| 10 | Original rho0→.5→1 stress raises source SD from ~.1414 to ~.1732 to .2. These are controlled feasible matrices, not a forecast. |
| 11 | Sector/common-factor overlap reviewed conceptually and supported by the three-name perfectly correlated fixture. No factor estimation. |
| 12 | Separate fixture labels, conventions, hashes, runtime, actual outputs and baseline/transition retained. Corrected revision is containing publication commit. |

## Limits and resume checkpoint

Local Linux CPython standard library only. Exact source commands/functions are separate from supplemental HHI, limit/expectation formulas and conceptual design reviews. No empirical covariance accuracy, actual timing/FX/NAV integration, costs/taxes/rebalancing, production conditioning/performance, platform coverage, independent reviewer acceptance or certification. F28 notebook/platform, F32 shared-input integration and newer unresolved findings remain open.

Chapter 16 now records eight core workflows and 216 local answers within scope. Next: Section 16.9 — Two-Asset Portfolios.
