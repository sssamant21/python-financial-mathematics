# Section 16.10 — scoped multi-asset workflow and answer review

Baseline manuscript: `e147979929d466657bc3b4ec43f003cc5e1cf3fa`. One core workflow, all 30 local answers and twelve lab steps reviewed. Predicates, workflows, answers and historical unique methods are separate inventories.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-multi-asset-review/review.py
```

Reproduce unchanged-source failures (requires baseline in Git history; expected nonzero exit writes `baseline.json`):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-multi-asset-review/review.py e147979929d466657bc3b4ec43f003cc5e1cf3fa
```

The runner extracts the exact reference Python fence, runs its printed demonstration and twelve existing unittest methods, checks silent import, and runs printed compileall in isolation. Final `results.json`: three successful commands, 62 passing supplemental predicates, hashes, raw output, runtime/platform and independent rational/Decimal expectations and tolerances. No new historical unique methods.

## Baseline and scoped corrections

`baseline.json` retains 19 failed predicates against unchanged source; all twelve original methods passed. F151 corrects budget/probability residual amplification, allocation-total overflow, integer expectation cancellation, zero-mass/rare-large scenario moments, variance/output underflow/overflow, finite-limit weight drift, nonboolean permission, huge integer exception contracts, malformed scenario containers and nonzero zero-variance covariance rows.

Three baseline failures are explicitly scope/policy extensions: one full-matrix PSD screen beyond the old disclosed limit, and two explicit signed-scenario permission cases. Previously scenario weights could be signed implicitly and there was no permission keyword. The new API defaults consistently to long-only and accepts signed scenarios only with boolean `allow_short=True`; both rejection and permitted .11 expectation are executed. This closes a declared policy/validation gap rather than implying a previous explicit permission guarantee. No observer crash or failed corrected-source transition occurred here.

Internal vectors retain integer/displayed-decimal rational values. Weights and nonnegative scenario probabilities accepted within 1e-10 of unit mass are normalized exactly before use. Roots use 80-digit Decimal. Every required float output must be finite and preserve an exact nonzero value or raise ValueError; all statistics fields must be reportable even if a different field alone would be. Displayed variance contributions must reconcile to total within relative 1e-10, no absolute floor; normalized allocation/drift outputs must reconcile to one. Catastrophic float cancellation in a reported vector rejects instead of claiming an identity that the output cannot retain.

The covariance screen applies rational Schur complements to matrix plus delta times identity, delta=1e-10 times maximum diagonal, averages accepted within-tolerance asymmetry and rejects negative diagonals/nonzero zero-variance rows. Requested negative exact forms reject rather than clip. This numerical screen is not exact model/estimator certification.

Drift assumes long-only simple returns no lower than −100%, no external flows/trades and positive ending NAV. Scenario inputs are finite linear return shocks; arbitrary finite values are not certified as economically valid unleveraged asset returns. Financing, actual NAV/collateral and real data alignment remain outside the API.

## Independent mathematics and all 30 answers

The observer independently expands rational weighted means/quadratics, contributions and relative ending values. Scenario variance uses the two-scenario pairwise identity p1*p2*(R1−R2)^2 rather than source centered squares. Decimal roots give SD expectations. Supplemental scenario-implied asset moments feed source portfolio_statistics for a same-model cross-route check. These derivations and synthetic metadata are supplemental, not extra manuscript exports.

| Answers | Review and executed boundary |
|---|---|
| 1–5 | Source expectation .059; supplemental budget1 and mean contributions [.04,.015,.004]. The source exports no separate contribution-of-mean function. |
| 6–11 | Supplemental diagonal [.01,.0081,.000016] and A–B cross .0018; source total variance .019916 and SD≈.1411240589. |
| 12–14 | Source normalization of [50,30,20] and [500,300,200] yields [.5,.3,.2]; [1,0,0] source expected return .08. |
| 15–18 | Matrix dimensions/order and symmetry reviewed/executed; source component variances [.0109,.009,.000016] sum to .019916. Mathematical quadratic and Euler variance identities independently checked. There is no source general rank/eigenvalue routine. |
| 19–20 | Source two-asset drift gives [11/21,10/21]; supplemental original-period portfolio realized return .05. No source standalone realized-return export. |
| 21–22 | Source equal-probability two-asset scenario returns both .05 give mean .05/variance0. This is a separate exercise fixture from the three-asset lab alternative model. |
| 23–25 | Source explicitly permitted static signed weights [1.2,−.2] yield expected .11 before financing; long-only violations reject. Cash-like .2 weight at .02 mean contributes .004, but original C variance .0004 is not assumed zero. |
| 26–27 | Mixed return horizons require alignment; centered sample covariance rank is at most min(N,T−1)=4 for N10/T5. These are design/mathematical reviews, not actual resampling, rank estimation or observed-data execution. |
| 28–30 | Names with common factors may diversify little; global PSD requirement and source invalid-direction rejection reviewed; optimized historical moments can be unstable out of sample. No empirical calibration/optimization acceptance. |

## Twelve lab-step contracts and executed source chain

Prerequisites: asset order, consistent horizon/currency/return convention, fully invested beginning weights, covariance/variance, normalization, buy-and-hold without flows, and discrete scenario probabilities. Fictional A/B/cash-like C share hypothetical one-period simple-return inputs in common USD. No actual dates, forecast vintage, sample size or estimator window are invented.

| Step | Result and source boundary |
|---|---|
| 1 | Source normalized [50,30,20] yields original [.5,.3,.2], unit budget checked. |
| 2–3 | Supplemental return contributions [.04,.015,.004]; source expected return .059. |
| 4 | Source dimension/symmetry/full-matrix screen executed on supplied covariance; actual provenance unknown. |
| 5–7 | Supplemental diagonal and cross expansion reconciles to source variance .019916. |
| 8 | Source SD≈.1411240589 checked against independent Decimal root. |
| 9–10 | Supplemental Sigma-w [.0218,.03,.00008]; source variance contributions [.0109,.009,.000016] reconcile to total. No separate Sigma-w export. |
| 11 | Exact-source chain normalize_allocations→portfolio_statistics→drifted_weights→portfolio_statistics. Fixed realized returns [.10,−.05,0] give ending relative values [.55,.285,.20], total1.035, weights [110/207,57/207,40/207]. Held-fixed-model updated-weight mean≈.06014492754 and variance≈.01989054587 match independent rational expectations. This is a counterfactual sensitivity at new weights, not an actual next-period forecast without updated as-of inputs. No trades, flows/costs or actual shared source integration. |
| 12 | Alternative three-asset scenarios probabilities [.25,.75], rows [[.10,−.05,.02],[−.10,.04,.02]] give source portfolio returns [.039,−.034], mean −.01575, variance .0009991875, SD≈.03160992724. Supplemental asset means [−.05,.0175,.02] and covariance feed source portfolio_statistics, reproducing the same mean/variance. These inputs are a different model from original mean .059/covariance. Hashes/runtime/raw outputs retained; corrected revision is containing commit. |

The same-model cross-route variance contributions are [.00136875,−.0003695625,0]; their signed sum is .0009991875. Negative B contribution under this valid joint model is not negative total risk. The original static forecast, held-fixed sensitivity and alternative scenario forecast are explicitly labelled rather than equated.

## Limits and resume checkpoint

Local Linux CPython standard library only. Source execution is separate from supplemental moment construction/expectations/metadata and conceptual design reviews. The local API chain does not close F32 broader shared-input integration: actual asset IDs, as-of timestamps, source provenance, FX/NAV/financing, pipeline/calendar and real transaction assumptions remain unvalidated. F28 notebook/platform and newer unresolved findings also remain open. No production conditioning/performance, empirical accuracy, independent reviewer acceptance or certification.

Chapter 16 now records ten core workflows and 276 local answers within scope. Next: Section 16.11 — Correlation and Diversification.
