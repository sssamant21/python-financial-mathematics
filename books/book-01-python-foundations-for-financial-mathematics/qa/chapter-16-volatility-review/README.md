# Section 16.7 — scoped volatility and risk-budget review

Baseline manuscript: `5cbc3c95ef40a75d3af5aba8893064fbf745ad7b`. One core workflow, all 30 local answers and twelve lab steps reviewed. Predicate, workflow, answer and historical unique method counts remain separate.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-volatility-review/review.py
```

Reproduce unchanged-source failures (requires baseline in Git history; expected nonzero exit writes `baseline.json`):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-volatility-review/review.py 5cbc3c95ef40a75d3af5aba8893064fbf745ad7b
```

The observer extracts the exact Python reference listing, runs the printed demonstration and twelve existing unittest methods, checks silent import and executes printed compileall in isolation. Final `results.json`: three successful commands, 61 passing supplemental predicates, runtime/platform, input/listing/source hashes, raw outputs, independent rational/Decimal expectations and comparison tolerances. No new historical unique methods.

## Initial evidence, output contracts and linked follow-up

`baseline.json` retains 20 failed predicates with the final observer policy. All twelve existing tests passed before correction. F148 corrects integer centering and budget loss, overflow before signed cancellation, tiny/large realized moments, premature variance-to-SD conversion, budget residual amplification, nonboolean controls, nonfinite/zero-underflow scale results and exception contracts. Rational integer/displayed-decimal calculations precede 80-digit Decimal roots and final finite/nonzero-preserving float reports.

Two baseline failures explicitly labelled `PSD extension` add full-matrix screening beyond the original correctly disclosed requested-direction boundary. They are acknowledged design-gap closures, not evidence of a prior false PSD guarantee. The new common screen applies rational Schur complements to covariance plus 1e-10 times the largest diagonal times identity, averages within-tolerance symmetric pairs, rejects negative diagonals and nonzero zero-variance rows, and rejects negative exact requested forms. It is a scale-relative numerical screen, not exact PSD/model certification.

`initial-policy-baseline.json` preserves the original 61-predicate inventory with 21 failures, including an expectation that integer-hedge percentage contributions would be reportable. Review changed that output contract: exact identities can hold while the reported floats lose their sum through destructive cancellation. The final observer instead requires clear rejection of unreconcilable displayed attribution; this case was already rejected by the original listing for a different weight-coercion reason. The two baseline inventories are not added. No observer crash occurred in this section.

Every attribution field must be reportable, components must sum to total, and percentages to one within relative 1e-10 without an absolute floor. A valid positive exact variance does not guarantee the whole float attribution vector can be reported. Zero-risk attribution remains undefined. SD may be finite even when variance cannot be represented, and is computed directly from the exact quadratic. Scaling validates boolean assumption declaration only, not empirical independence/stationarity.

This batch also retains and corrects a linked Section 16.6 reporting issue discovered during attribution review. Its [reporting-baseline.json](../chapter-16-variance-review/reporting-baseline.json) executes published revision `5cbc3c95ef40a75d3af5aba8893064fbf745ad7b`: 60 checks pass and the added output-reconciliation rejection fails because [1e18+1,−1e18] contributions are reported as [1e18,−1e18], summing to zero rather than variance one. The Section 16.6 source now checks reported diagonal/cross and asset contributions; its expanded 61-predicate final rerun and twelve existing tests pass. Historical unique methods remain unchanged. This is separate source evidence, not an independent implementation/reviewer acceptance.

## Independent expectations and all 30 answers

Reference values derive from rational two-asset quadratic forms, exact two-observation variance identities, analytic Euler ratios and 80-digit Decimal roots. Scaling, population SD, diversification ratio, target ratio and metadata assembly are supplemental calculations where no source export exists. Different models remain labelled.

| Answers | Review and executed boundary |
|---|---|
| 1–4 | Source SD .20 from variance .04, main variance .0336 and SD≈.1833030278; concentrated first asset SD .20. Supplemental .15²=.0225. |
| 5–7 | Source equal-risk 50/50 SDs sqrt(.02), .20, 0 for correlations 0,+1,−1. |
| 8–11 | Source hypothetical annual SD .01 sqrt(252)≈.1587450787 and .04 sqrt(12)≈.1385640646; source sample SD of [.1,−.1] is sqrt(.02), independent population SD .10 is supplemental. |
| 12–16 | Source components .0168/sqrt(.0336) each≈.0916515139 and shares [.5,.5]. Marginals .028/sqrt(.0336)≈.1527525232 and .042/sqrt(.0336)≈.2291287847; Euler identities checked. These are unconstrained derivatives at normalized weights. |
| 17–18 | Zero-risk source attribution rejects. Supplemental doubled unnormalized exposures double SD; fully invested source API rejects the doubled budget. |
| 19–20 | Explicitly permitted signed source variance .0564 has SD≈.2374868417; scaling covariance by 10,000 scales source SD by 100. No financing claim. |
| 21–22 | Serial covariance changes sum variance and historical SD is not a future guarantee. No empirical autocorrelation/forecast calibration performed. |
| 23–24 | Covariance-stress answer clarified to positive weights, positive starting variance and feasible symmetric changes. Valid PSD hedge example [.75,.25], [[1,−2],[−2,4]] gives negative B volatility component −.5 with positive total .25. |
| 25–26 | Consistent weight/matrix permutation preserves source SD; inconsistent ordering changes it. Indefinite input source rejection tested under the added global screen; no general eigenvalue routine. |
| 27–28 | Realized versus forecast labels and nonlinear option risks reviewed conceptually; no GARCH/full-revaluation/tail model implemented or accepted. |
| 29–30 | Supplemental diversification ratio .22/.18=11/9; separate target scale .09/.12=.75. No source diversification-ratio or target-ratio helper, no trading engine. |

## Twelve lab-step contracts

Prerequisites: fixed fully invested weights, covariance in matching asset order/horizon/currency/units, positive variance for attribution, and variance versus SD conventions. The main synthetic model has no real dates or empirical sample window.

| Step | Result and executed scope |
|---|---|
| 1–2 | Source main variance .0336 and SD≈.1833030278. |
| 3–4 | Supplemental standalone SDs [.2,.3] and Sigma-w [.028,.042]; source does not export these intermediates separately. |
| 5 | Source marginals≈[.1527525232,.2291287847]. Feasible direction [1,−1] derivative is their difference, separately checked. |
| 6–7 | Source components≈[.0916515139,.0916515139] sum to source total. |
| 8 | Source risk shares [.5,.5] sum to one; capital weights remain [.6,.4]. |
| 9 | Original-model zero symmetric covariance gives variance .0288 and SD≈.1697056275. This differs from the separate equal-risk 50/50 example. |
| 10 | Separate hypothetical daily SD .01 annualizes with 252 stable independent equal-period increments. Main matrix is not relabelled as daily. |
| 11 | Separate 12%-SD risky sleeve and hypothetical exactly zero-risk cash matrix [[.0144,0],[0,0]], weights [.75,.25], give source SD .09. Scaling original [.6,.4] risky weights to [.45,.30] plus .25 cash gives .75 sqrt(.0336)≈.1374772708, not .09. No turnover, financing or real cash-risk guarantee. |
| 12 | Labelled fixtures, input/source/listing hashes, conventions, raw output and runtime retained. Corrected revision is the containing publication commit; baseline above. |

## Limits and resume checkpoint

Local Linux CPython standard library only. Source commands/functions are separate from supplemental formulas, fixture assembly, metadata and conceptual financial designs. No actual as-of source timing, FX/NAV integration, volatility forecasts, nonlinear revaluation, production performance, independent reviewer acceptance or certification established. F28 notebook/platform, F32 shared-input integration and newer unresolved findings remain open.

Chapter 16 now records seven core workflows and 186 local answers within scope. Next: Section 16.8 — Diversification.
