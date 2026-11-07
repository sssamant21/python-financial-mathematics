# Section 16.6 — scoped portfolio variance and attribution review

Baseline manuscript: `e9923503c1330e6c9612fd36222426bdf4308098`. One core workflow, all 30 local answers and twelve lab steps reviewed within the boundaries below. Predicate, workflow, answer and historical unique method counts are separate.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-variance-review/review.py
```

Reproduce unchanged-source failures (baseline must exist in Git history; expected nonzero exit writes `baseline.json`):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-variance-review/review.py e9923503c1330e6c9612fd36222426bdf4308098
```

The runner extracts the exact reference Python fence. It runs the printed demonstration and twelve existing unittest methods, checks silent import and executes the printed compileall command in isolated temporary directories. Final `results.json` records three successful commands, 60 passing supplemental predicates, hashes, runtime, raw output and independent references/tolerances. No new historical unique methods.

## Initial evidence, correction and added scope

Corrected-observer `baseline.json` retains 24 failed predicates against unchanged source. All twelve original reference methods passed before correction. F147 corrects integer-weight/budget coercion loss, intermediate quadratic/marginal overflow, amplification of tolerated weight-budget residuals, nonboolean policy and invalid tolerance acceptance, negative tiny diagonals/form clipping, unreportable fields and premature volatility underflow/overflow. Numeric inputs use integer/displayed-decimal rational intermediates; roots use 80-digit Decimal before float output. Required float fields must be finite and preserve exact nonzero values or raise ValueError.

Five of the 24 baseline failures are explicitly labelled `PSD extension`: the old manuscript correctly disclosed that it checked only the requested direction. Full-matrix screening was an acknowledged design gap, not a falsely claimed prior guarantee. The corrected listing extends all five risk APIs to the common full-matrix screen, and rejects [[1,2],[2,1]] even for supplied weights [1,0]. This added coverage does not establish exact PSD, empirical calibration or independent acceptance.

Initial observer records are preserved separately. `baseline-observer-initial.json` incorrectly counted a rejection expectation for the finite value 1.48e308. `first-correction-rerun.json` retains the corrected-source rerun that failed only this incorrect expectation. `observer-correction.json` explains the error: changing the overflow fixture from weights [1.2,−.2] to [1.5,−.5] makes variance 2.5e308, beyond float range. The corrected observer then produced the retained baseline and final results, including a new independent volatility check at the overflowing-variance fixture. This observer failure is not a source defect. The earlier two reports also retain their smaller check inventories; counts are not added together.

Fully invested budgets within 1e-10 are normalized explicitly before all calculations. Signed positions require a boolean permission; financing/margin remain external. Matrix validation averages within-tolerance asymmetric pairs, forbids negative diagonals and nonzero zero-variance rows, and applies a rational Schur-complement screen to the matrix plus delta times identity. Delta is the declared relative tolerance times the largest diagonal (default 1e-10). This permits bounded numerical matrix error, not arbitrary non-PSD inputs. The exact requested quadratic form must be nonnegative for every risk API. Unlike Section 16.5's documented clipping policy, this section rejects any negative requested exact form so attribution and total do not silently disagree. Float rounding can affect near-singular inputs and public validation helper outputs; calculation routines retain exact normalized intermediates.

Output availability is per API: variance can be unreportable while its SD is finite; decomposition or contributions can be unreportable even when total variance is finite. Volatility therefore roots the exact quadratic before conversion, not a prematurely rounded variance.

## Independent expectations and all 30 answers

The observer independently expands rational quadratic forms, constructs diagonal/cross terms and covariance sensitivities from the written formulas, and uses Decimal roots. It checks the feasible directional derivative by a central difference, analytically exact for a quadratic. Fixture assembly, unnormalized quadratic evaluation and annualization calculations are supplemental implementations, not extra reference exports.

| Answers | Review and executed boundary |
|---|---|
| 1–4 | Source variance .04, .0325 and .0336; SD sqrt(.0336)≈.1833030278 checked. |
| 5–7 | Source diagonal .0288 plus cross .0048 reconciles to .0336. |
| 8–11 | Source zero/perfect positive/perfect negative correlations give variances .02,.04,0; the second perfect-hedge matrix also gives zero. SD .1414213562 for .02 is the independent square root. |
| 12–15 | Source concentrated variance .04; source asset contributions .0168 each sum to .0336. Cross terms are not themselves per-asset allocations. |
| 16–18 | Source marginals .056/.084; symmetric covariance increase .005 produces .0024 variance increase. Unconstrained marginal and budget-preserving direction distinguished. |
| 19–20 | Supplemental unnormalized doubled weights multiply variance by four (.1344); source deliberately rejects the doubled budget. Explicitly permitted [1.2,−.2] source variance is .0564. No financing claim. |
| 21–23 | Centered Gram-matrix rank is at most T−1=1 with two observations and five assets. Matrix [[1,2],[2,1]] has eigenvectors [1,1]/[1,−1] with eigenvalues 3/−1, so cannot be covariance; full source rejection executed. General rank/PSD statements are mathematical reviews, not a general eigen/rank routine. |
| 24–25 | Supplemental iid equal-day arithmetic scaling gives annual variance .0252 and SD sqrt(.0252)≈.1587450787; no source annualization function or empirical serial-dependence check. |
| 26–27 | Feasible lower symmetric covariance lowers variance at fixed positive weights; clarified signed change formula. Source percentage-unit matrix scaling makes .0336 become 336 (10,000 times larger). |
| 28 | Misordered matrix gives source variance .0436; consistently permuting both weights and matrix restores .0336. The API has no asset-label inference. |
| 29–30 | Tolerance must be documented in matrix units; negative exact requested forms now reject rather than hide under an absolute floor. Valid PSD hedge example weights [.75,.25], matrix [[1,−2],[−2,4]] gives a negative B contribution −.125 while total variance remains .0625. |

## Twelve lab-step contracts

Prerequisites: complete fixed weights, aligned covariance and asset order, variance/covariance, quadratic forms and partial versus directional derivatives. The supplied matrix is fictional in squared decimal simple-return units, one common period and common fictional USD. Estimation window, dates and sample size are absent; they are not invented.

| Step | Executed result and limit |
|---|---|
| 1 | Fictional A/B metadata fixed; horizon common but real dates unknown. |
| 2 | Source matrix dimension/symmetry checks and new full-matrix screen executed. |
| 3 | Source diagonal .0288; independent terms .0144+.0144. |
| 4 | Source cross .0048=2(.6)(.4)(.01). |
| 5 | Source total .0336, reconciled to independent rational expansion and diagonal+cross. |
| 6 | Source volatility .1833030278; independent Decimal root checked. |
| 7 | Supplemental covariance-weighted exposures [.028,.042]; source contributions [.0168,.0168]. No separate source Sigma-w export. |
| 8 | Source contributions sum to .0336. |
| 9 | Source unconstrained marginals [.056,.084]. Feasible direction [1,−1] has derivative −.028, verified by a centered h=1/8 perturbation that preserves unit budget. These are derivatives at normalized weights, not derivatives of the normalization adapter. |
| 10 | Source zero-covariance variance .0288. |
| 11 | Raising both off-diagonals .01 to .015 keeps the matrix feasible; source total .036, change .0024. |
| 12 | Fixture/listing/source hashes, conventions, runtime and actual outputs retained. Corrected revision is the containing publication commit; no actual data provenance or independent reviewer acceptance. |

## Limits and resume checkpoint

Local Linux CPython standard library only. Source execution is distinguished from supplemental numeric formulas, derivatives, metadata assembly and conceptual estimator reviews. No empirical calibration, source timestamp/FX/NAV integration, production conditioning/performance, platform coverage or independent acceptance established. F28 notebook/platform, F32 broader shared-input integration and all newer unresolved findings remain open; this is not certification.

Chapter 16 now records six core workflows and 156 local answers within scope. Next: Section 16.7 — Portfolio Volatility.
