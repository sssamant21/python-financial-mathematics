# Section 16.11 — scoped correlation and diversification review

Baseline manuscript: `232476e4b766bcbae0c52357dd952ff9cd663bc6`. One core workflow, all 30 local answers and twelve lab steps reviewed. Predicates, workflows, answers and historical unique methods remain separate inventories.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-correlation-review/review.py
```

Reproduce unchanged-source failures (requires baseline in Git history; intentionally exits nonzero and writes `baseline.json`):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-correlation-review/review.py 232476e4b766bcbae0c52357dd952ff9cd663bc6
```

The runner extracts the exact Python reference fence, runs the printed demonstration and twelve existing unittest methods, checks silent import and executes the printed compileall command in isolation. Final `results.json`: three successful commands, 59 passing supplemental predicates, hashes, raw outputs, runtime/platform and rational/Decimal references and comparison tolerances. No new historical unique methods.

## Baseline, observer correction and contracts

`baseline.json` retains 16 failed supplemental predicates against unchanged source; the original twelve unittest methods already passed. F152 corrects integer centering/coercion loss, mean/squared moment overflow, correlation underflow/overflow, weight residual amplification, premature quadratic conversion, accepted correlation diagonal/endpoint residuals, tiny negative variance clipping, nonzero zero-variance covariance rows and finite-report/exception contracts. Two predicates labelled `PSD extension` extend screening to the full arbitrary correlation/covariance matrix beyond the old correctly disclosed limitation; this is design-gap closure, not a previous false full-PSD guarantee.

`observer-failure.json` separately retains the initial QA traceback: Fraction times Decimal was unsupported. Before completing a baseline, review also corrected its unevaluated simplified SD reference, which had incorrectly assumed all sample correlations were zero. The actual fixture has AB=AC=0 and BC=−1/sqrt(3). The corrected observer consistently uses Decimal and derives rescaled SD from the actual independent covariance. This was an observer error, not a source failure; no complete baseline predicate count was emitted before the traceback. To reproduce the observer error in a throwaway copy, replace the final `reference_sd` calculation with `F(1,5)*root(F(1,3))` at that probe. Baseline and final reports use the corrected observer.

Integer/displayed-decimal rational intermediates precede 80-digit Decimal roots and final reporting. Each required float result must be finite and preserve a nonzero exact value, or ValueError is deliberate. Sample correlation uses internal exact moments and can remain reportable when standalone sample covariance cannot be represented. Portfolio SD similarly roots the exact quadratic before float conversion of variance. Constant-series Pearson correlation remains undefined.

Within-tolerance supplied correlation diagonals are set to one; accepted symmetric pairs are averaged and bounded endpoint excursions clipped. A rational Schur-complement screen tests C+1e-10*I. Covariance consumers use a scale-relative screen on covariance plus 1e-10 times its largest diagonal times identity, reject negative diagonals/nonzero zero-variance rows and reject negative exact requested forms. This is numerical screening, not exact PSD/model certification. Near-singular float conversion does not preserve exact matrix rank. Supplied zero SDs may use a model correlation placeholder, but no empirical constant-series correlation is thereby defined.

Accepted long-only budgets within 1e-10 are normalized. Generated equicorrelation rho near the exact lower/upper bound snaps within 1e-12; negative reported endpoints round inward as necessary. Materially invalid correlations reject. Actual timestamps, currency and horizon are external prerequisites.

## Independent mathematics and all 30 answers

The observer uses the pairwise-difference covariance identity `sum(i<j)(x_i−x_j)(y_i−y_j)/(T*(T−1))`, independently of source centered products. Correlation derives from these rational moments and high-precision roots. Stress risk uses the independent equicorrelation closed form `s²*(rho+(1−rho)/N)`. Inverse conversion, limiting risk, fixture assembly and metadata are supplemental, not extra source exports.

| Answers | Review and execution boundary |
|---|---|
| 1–4 | Source sample correlations +1,−1,0 and covariance2 checked for the written fixtures. |
| 5–6 | Source covariance .03 from [.2,.3]/rho.5; supplemental inverse .01/(.2*.3)=1/6. No source inverse-covariance helper. |
| 7–10 | Source two-asset equal-.2-SD models rho0,+1,−1 give SD sqrt(.02),.2,0. Source-derived variance difference independently confirms correlation sensitivity .03 for [.2,.3] at equal weights. |
| 11–14 | Source generated lower bounds N3−.5/N4−1/3 checked with inward reporting; N5/rho.25/s.2 risk sqrt(.016); supplemental fixed-rho nonnegative common floor .10. A fixed negative common rho cannot persist as N grows arbitrarily. |
| 15–18 | Source constant sample rejects; nondegenerate matrix diagonal1 and symmetry checked; invalid correlation1.2 lies outside required bounds. Pairwise bounds do not replace the added full-matrix screen. |
| 19 | Source X=[−2,−1,0,1,2], Y=X² has correlation0 while dependence is deterministic and nontrivial. This is a synthetic nonlinear counterexample, not evidence of market independence. |
| 20–23 | Pairwise missingness can destroy a common PSD estimate; controlled positive common-correlation stress raises risk. Rolling windows and spurious price-trend correlation reviewed conceptually; no rolling/join/price-to-return pipeline implemented here. |
| 24–26 | Common FX basis, outlier sensitivity and small-sample uncertainty reviewed. No actual FX conversion, robust estimator or empirical sampling calibration. |
| 27–30 | Signed hedge contributions can be negative in a suitable model; common factors can erode name diversification; daily/monthly correlations need not match; correlation does not imply causation. No signed-weight attribution, factor or tail-dependence engine exported here. |

## Twelve lab-step contracts

Prerequisites: synchronized finite returns, asset-major orientation, sample denominator T−1, positive sample variances for Pearson correlation, matching units/base currency/horizon and a valid joint stress matrix. Four fictional common observation labels 1–4 have no actual dates, missing entries or imputation.

| Step | Result and source boundary |
|---|---|
| 1 | Explicit A=[−.01,0,.01,0], B=[.01,−.02,.01,0], C=[0,.01,0,−.01], decimal simple returns in fictional common USD and shared hypothetical period. |
| 2 | Every source sample covariance checked: diagonal [1/15000,1/5000,1/15000], AB=AC=0, BC=−1/15000. |
| 3–5 | Every source sample correlation checked: diagonal1, AB=AC=0, BC=−1/sqrt(3)≈−.5773502692; symmetric common-sample matrix. |
| 6 | Separate model uses those dependence estimates with assumed standalone SDs [.2,.2,.2]. Source conversion and equal-weight risk give SD .2*sqrt((3−2/sqrt(3))/9)≈.09056119997. This is a rescaled model, not the original sample covariance or the later common-rho model. |
| 7 | Separate hypothetical equicorrelation rho0 gives variance .04/3 and source SD≈.1154700538. |
| 8 | Rho.25 gives variance .02, source SD≈.1414213562, matching the original acceptance reference. |
| 9 | Rho.75 gives variance1/30, source SD≈.1825741858. |
| 10 | N3/rho−.75 rejected; pairwise bounds alone are insufficient. |
| 11 | Closed form and source outputs show risk increases over rho0,.25,.75 at fixed SDs/weights. No empirical stress forecast. |
| 12 | Sample/rescaled/stress labels, observation IDs, complete-case policy, assumptions, hashes, runtime and actual results retained. Corrected revision is containing publication commit; actual estimator window and availability remain unknown. |

## Limits and resume checkpoint

Local Linux CPython standard library only. Exact source execution is separate from supplemental pairwise oracles, closed forms, metadata and conceptual designs. No actual source timestamp/FX/NAV integration, estimator suitability, nonlinear/tail forecast, production conditioning/performance, platform coverage, independent reviewer acceptance or certification. F28 notebook/platform, F32 broader shared-input integration and newer unresolved findings remain open.

Chapter 16 now records eleven core workflows and 306 local answers within scope. Next: Section 16.12 — Efficient Portfolio Concepts.
