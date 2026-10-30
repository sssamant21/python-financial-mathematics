# Book 02 — Coverage-gap remediation register

**Updated:** 2026-10-30
**Scope:** Selected follow-ups after the 215-section substantive mapping pass.
**Disposition:** Twenty-eight COV categories partially addressed; none closed by this register.

This register separates concrete changes from remaining obligations. It is not a completion percentage for the ninety categories: categories differ in scope, overlap and contain manual proof/review requirements. Earlier chapter fixes remain in their own records.

| Category | Concrete result | Remaining scope | Evidence |
|---|---|---|---|
| COV-49 | Section 8.6 checks exact polynomial second-difference errors/orders and selected cancellation; two faulty variants detected. | Other helpers, noise/wrong-reference/range cases and independent review. | [Difference order](chapter-08-difference-order-followup.md) |
| COV-50 | Section 8.9 directly checks errors/gates, retains tolerances and rejects nonfinite computed estimates/errors. | Broader comparator/reference/range and independent review. | [Comparator audit](chapter-08-comparator-audit-followup.md) |
| COV-51 | Section 8.8 validates returned estimates and avoids Richardson intermediate overflow; selected perturbation/callback/denominator guards checked. | Earlier copies, implicit domains/ranges and independent review. | [Helper guards](chapter-08-helper-guards-followup.md) |
| COV-55 | Section 10.7 checks exact polynomial errors/orders/estimators and selected smooth exponential ratios; three faulty variants detected. | Broader report/error and financial-oracle scope; independent review. | [Quadrature order](chapter-10-quadrature-order-followup.md) |
| COV-59 | Section 11.9 retains limits/allowances and checks isolated gross/name/NAV-gap threshold breaches. | Selected Section 11.7 budget/threshold cases now checked; broader policy scope/units and independent review remain. | [Policy audit](chapter-11-policy-audit-followup.md) |
| COV-60 | Section 11.6 adds fixed residual norms and rational projection/scale/sign/label oracles. | Other report fields, relative-distance/cumulative scope and independent review. | [Projection audit](chapter-11-projection-audit-followup.md) |
| COV-61 | Section 12.5 rank_A no longer depends on target magnitude; column-equilibration policy disclosed; selected scale/zero/near-dependent cases added. | Larger pivot/scaling cases and independent numerical-rank review. | [Rank](chapter-12-rank-target-scaling-followup.md) |
| COV-62 | Section 12.9 retains aligned limits; controlled factor rejection and threshold/constructor/guardrail cases checked. | Broader ranges, source/version provenance and independent review. | [Factor audit](chapter-12-factor-audit-followup.md) |
| COV-64 | Selected Section 13.6 exact normalized-pivot boundaries and reordered-column rational least-squares references checked. | Selected basis-span reconstruction now checked; general near-dependence, Q/R identities and independent review remain. | [QR rank screen](chapter-13-qr-rank-followup.md) |
| COV-65 | Fixed Section 13.8 ridge positions, residuals, objectives, nonoptimal comparisons and selected positive-strength limit checked against exact rational references. | General weighted/regularized derivations, target/coefficient scaling, broader optimality and independent review. | [Ridge optimality](chapter-13-ridge-optimality-followup.md) |
| COV-66 | Section 13.9 direct invalid-input, report-field, standardized residual and repeated strict-JSON checks added. | Complete configuration/provenance, economic unit consistency, broader ranges and independent review. | [Project contract](chapter-13-project-contract-followup.md) |
| COV-67 | Twelve restricted SVD cases assert reconstruction, orthonormality, factor-order/sorted-summary conventions and thresholded solves. | Copied-reference reports, broader integration/range and independent review. | [SVD ordering](chapter-14-svd-order-followup.md) |
| COV-68 | Twelve selected repeated/near-repeated eigenpair cases check scaled closed-form values, projectors, residuals and reconstruction. | Unequal spectra, symmetry/gap boundaries, near-SPD pivots, broader range and independent review. | [Near-repeated spectra](chapter-14-near-repeated-followup.md) |
| COV-69 | Section 14.9 computes/reports covariance eigenpairs; closed-form roots, projectors and direct residual/reconstruction checks added. | Independent review and broader numerical/interface scope. Fixed compression bound and input/unit metadata now asserted. | [Eigenpairs](chapter-14-covariance-eigenpair-followup.md) · [Compression bound](chapter-14-compression-bound-followup.md) |
| COV-70 | Section 15.9 second-order contractions checked by a Decimal path expansion across nine shocks; signed/absolute portfolio errors implemented and asserted. | Final-assessment/shared-dependency coverage and independent derivation/unit review. | [Taylor](chapter-15-taylor-oracle-followup.md) |
| COV-71 | Section 15.2 finite-difference representability and denominator guards aligned with related helpers; boundary tests added. | Perturbation asymmetry, step accuracy/convergence and selected Hessian numerical benchmarks. | [Scalar difference](chapter-15-scalar-difference-followup.md) |
| COV-72 | Section 15.8 directly checks zero/adjacent iso-variance denominator and selected signed-rate/maturity-domain cases. | Applied/manual examples, covariance contracts, units, range and independent review. | [Level-set boundaries](chapter-15-level-set-boundary-followup.md) |
| COV-73 | Nine adjacent exact Armijo boundary cases, backtracking counts and selected stationary/stagnation/budget/no-descent paths checked. | Other optimizer copies, status/report boundaries and independent review. | [Optimizer statuses](chapter-16-optimizer-status-followup.md) |
| COV-74 |Section 16.9 now evaluates metrics, normalized loss/gradient and acceptance per candidate; independent residual metrics and selected failed candidates/holdout/budget cases checked. Sections 16.8–16.10 metric range correction, shared-helper integration and selected invalid inputs checked. Section 16.8 fit/curvature/gradient/weighted-loss range corrected with exact/Decimal references. Sections 16.9/16.10 normalized-rate/curvature/gradient range corrected and independently referenced. Section 16.10 now recomputes candidate metrics/derivatives with explicit provisional gates and failed scenarios. Sections16.9/16.10 normalized-loss overflow/collective-underflow corrected with independent Decimal references. | Broader price/residual/update range, limit sensitivity, configuration/provenance, invalid data, conditioning and independent review. |[Candidate acceptance](chapter-16-candidate-acceptance-followup.md) · [Metric range](chapter-16-residual-metric-followup.md) · [Calibration range](chapter-16-calibration-range-followup.md) · [Normalized range](chapter-16-normalized-calibration-followup.md) · [Final candidate validation](chapter-16-final-candidate-followup.md) · [Normalized loss](chapter-16-normalized-loss-followup.md) |
| COV-75 |Section 16.7 multistart roots/local classification and scaling references; Sections 16.2–16.4 stencil geometry/denominator correction with exact polynomial checks; Section 16.6 exact secant threshold/callback/range correction and combined Newton update range/scaling checks. Section16.10 selected written curvature4/1 objectives and real histories now have distinct exact references. Section16.8 lab step10 now has an exact fixed-model rank/null-family demonstration. | Broader derivative accuracy/range, nonlinear Newton/convergence scope, convexity proofs, exact cumulative objectives and independent review. |[Multistart](chapter-16-multistart-reference-followup.md), [scaling](chapter-16-scaling-reference-followup.md), [derivative boundaries](chapter-16-derivative-boundary-followup.md), [secant boundaries](chapter-16-secant-boundary-followup.md), [Newton range](chapter-16-newton-range-followup.md) · [Cumulative objectives](chapter-16-cumulative-objective-followup.md) · [Identifiability lab](chapter-16-identifiability-followup.md) |
| COV-76 | Section 17.9 KKT fields independently recomputed across four regimes; four isolated rejection families and incomplete acceptance variants checked. | Tolerance units/scales, adjacent active-set transitions, degeneracy and independent review. | [KKT rejection](chapter-17-kkt-rejection-followup.md) |
| COV-77 | Section 17.9 guards trade/notional range, avoids intermediate cost overflow and computes turnover directly; selected extreme cases pass. | Report/input/audit scope, underflow policy and independent review. | [Financial range](chapter-17-financial-range-followup.md) |
| COV-78 | Section 17.10 now reports/checks second-cap multipliers and rejected candidates; rounded-sum empty intervals are rejected. | Broader final LP/QP coverage, shared dependencies and independent proofs/review. | [Final allocation](chapter-17-final-allocation-followup.md) |
| COV-79 | Section 18.8 now derives bracket invariants from cached signs/history and retains endpoint residuals; independent trace and callback-count checks cover seven paths. | Other solver trace/count diagnostics, numerical range and independent review. | [Bracket audit](chapter-18-bracket-audit-followup.md) |
| COV-82 | Section 19.6 stage/controller/rejection policy checked with Fraction stability references and callback traces; nine faulty variants detected. | Broader adaptive ODE behavior, numerical range, failure modes and independent review. | [Adaptive policy](chapter-19-adaptive-policy-followup.md) |
| COV-83 | Section 19.9 retains validated inputs/schedule and model/policy metadata; selected negative-jump/adjacent-time/log and JSON cases added. | Broader event numerics, cross-section policies and independent review. | [Provenance](chapter-19-input-provenance-followup.md) |
| COV-87 | Section 20.5 now raises explicit numerical-range errors for unrepresentable error magnitudes; exact tolerance comparison remains independent; extreme/subnormal cases added. | Section 20.6 now also validates numeric inputs/results and empty-portfolio rates. Other duplicated contracts/ranges, underflow interpretation and independent review remain. | [Error range](chapter-20-error-range-followup.md) · [PV contract](chapter-20-metamorphic-contract-followup.md) |
| COV-89 | Section 21.9 adds first-derivative finite-difference diagnostics, deterministic JSON, selected schema and injected failure propagation checks. | Broader interfaces, error paths and independent review. | [Integrated diagnostics](chapter-21-integrated-diagnostics-followup.md) |

The initial seven follow-ups through Section 21.9 are included in the [full runtime refresh](runtime-refresh-2026-10-29.md) at `37aac57a72303a6d4178790f8d172495e2bc0ada`: 444/444 compiled files; 233/233 script exits zero. The subsequent Chapter 14 compression-bound change has a 21-file/11-script scoped pass; Chapter 16 candidate acceptance has a 20-file/10-script scoped pass. Chapter 20 error-range reporting has a 19-file/10-script scoped pass. These follow the earlier full run. This execution evidence does not close the remaining column.

## Next executable and manual work

1. Section 14.9's selected compression-bound assertions are complete; continue the remaining numerical-contract/oracle obligations and independent review.
2. Continue numerical-contract and oracle items from the [prioritized queue](substantive-coverage-index.md), preserving exact expected behavior and scope.
3. Review unasserted exercise/proof, unit, model-assumption and editorial obligations with named independent reviewers.
4. Complete navigation/environment/release gates in the [review checklist](remaining-review-checklist.md).

When closing an item, record the exact sub-obligation, reviewer/evidence and revision; never promote the whole category solely because one selected example passed.

Section 18.8's subsequent bracket-audit change has a 21-file/11-script scoped pass; it is not included in the earlier full-book run.

Section 17.9's subsequent checker-only KKT follow-up has a 20-file/10-script scoped pass and is not included in the earlier full-book run.

Section 17.9's subsequent financial-range change has a 20-file/10-script scoped pass and is not included in the earlier full-book run.

Section 17.10's final-allocation change has a 20-file/10-script scoped pass and follows the earlier full-book run.

Section 12.9's subsequent factor-audit change has a 21-file/11-script scoped pass and follows the earlier full-book run.

## Full execution reconciliation — second refresh

All code follow-ups recorded above through the factor audit are included in the [second full-book refresh](runtime-refresh-2026-10-29-r2.md): 444 sources compiled and 233 scripts exited zero at `7ee99f60d5089510f860a0b6f695f971beb2eac6`, with 445 required sources/fixture blobs verified. Earlier statements about subsequent scoped-only changes remain historical; this shared run now covers them. Fourteen categories remain partially addressed; no independent closure or approval is inferred.

Section 10.7's subsequent checker follow-up has a 21-file/11-script scoped pass and is not included in the second full-book refresh.

Section 8.6's subsequent checker follow-up has a 21-file/11-script scoped pass and follows the second full-book refresh.

Section 8.9's comparator change has a 21-file/11-script scoped pass and follows the second full-book refresh.

Section 8.8's helper changes have a 21-file/11-script scoped pass and follow the second full-book refresh.

Section 8.8's [normalized-sensitivity follow-up](chapter-08-sensitivity-range-followup.md) extends COV-51 with zero-normalizer/nonfinite report guards and independent stencil-ratio checks. Its 21-file/11-script scoped pass follows the second full-book refresh. The selected category count remains eighteen.

Section 11.6's projection-report change has a 21-file/11-script scoped pass and follows the second full-book refresh.

The [Section 11.4 relative-distance follow-up](chapter-11-relative-distance-followup.md) extends COV-60 with independent denominator/norm and boundary checks. Its 21-file/11-script scoped pass follows the second full-book refresh; the selected category count remains nineteen.

Section 11.9's policy-audit change has a 21-file/11-script scoped pass and follows the second full-book refresh.

The [Section 11.7 budget follow-up](chapter-11-budget-boundary-followup.md) extends COV-59 with isolated budget and adjacent constraint-threshold cases; its 21-file/11-script pass follows the second full-book refresh. The selected count remains twenty.

The [Section 11.10 final nonfinite follow-up](chapter-11-final-nonfinite-followup.md) extends COV-60 with direct final-module validation and selected overflow paths. Its 21-file/11-script scoped pass follows the second full-book refresh; twenty selected categories remain partially addressed.

The [third full refresh](runtime-refresh-2026-10-29-r3.md) includes all prior Chapter 8/10/11 code follow-ups: 444 files compiled, 233 scripts passed and 445 required blobs verified before/after. The new Chapter 13 checker follows that full run.

## Selected Chapter 13 QR rank-screen follow-up — 2026-10-29

[New evidence](chapter-13-qr-rank-followup.md): exact selected normalized-pivot boundaries across four common scales and an independently known least-squares solution under column/target-label permutations. All 22 Chapter 13 files compiled and 12 scripts passed. Solver unchanged; COV-64 partially addressed, with general near-dependence, Q/R identities, basis-span reconstruction and independent review still open. This checker follows the third full-book runtime refresh.

## Selected fixed-model ridge follow-up — 2026-10-29

[Exact-objective evidence](chapter-13-ridge-optimality-followup.md) partially addresses COV-65: four positive ridge strengths, twelve nonoptimal objective comparisons and a six-point limit sequence. All 23 Chapter 13 files compiled and 13 scripts passed. The helper remains a fixed two-identical-column model with positive strength required. Broader weighted/regularized, scaling and independent-review obligations remain open; this scoped run follows the third full-book refresh.

## Selected project-contract follow-up — 2026-10-29

[Section 13.9 evidence](chapter-13-project-contract-followup.md) partially addresses COV-66 with direct nonfinite/bool, scale/limit, label/shape/unit-metadata rejection and selected report/strict-JSON checks. All 24 Chapter 13 files compiled and 14 scripts passed. Economic unit consistency, complete retained inputs/provenance, broader ranges and independent review remain open. This scoped run follows the third full-book refresh.

## Selected reordered basis-span follow-up — 2026-10-29

[Section 13.2 evidence](chapter-13-basis-span-followup.md) extends partial COV-64 remediation: eighteen permutation/scale cases with exact selected-basis coordinates reconstruct every original column and a separately chosen exposure. All 25 Chapter 13 files compiled and 15 scripts passed. General near-dependence, Q/R identities and independent review remain open. This scoped run follows the third full-book refresh; twenty-three selected categories remain partially addressed.

## Selected null-basis follow-up — 2026-10-29

[Section 13.3 evidence](chapter-13-null-basis-followup.md) extends COV-64 with 72 selected known-rank cases, exact returned-vector Az=0 identities, free-coordinate independence and unchanged exposures under null-space shifts. All 26 Chapter 13 files compiled and 16 scripts passed. General near-dependence, Q/R identities and independent review remain open. This scoped run follows the third full-book refresh; twenty-three categories remain partially addressed.

## Selected near-repeated spectral follow-up — 2026-10-29

[Section 14.1 evidence](chapter-14-near-repeated-followup.md) partially addresses COV-68 with twelve closed-form value/projector and normalized residual/reconstruction checks. The coordinate-direction fallback below the gap cutoff is explicitly approximate for nonzero off-diagonals. All 22 Chapter 14 files compiled and 12 scripts passed. Broader spectrum/range, symmetry, Cholesky and independent-review obligations remain open. This scoped run follows V-34; twenty-four selected categories are partially addressed.

## Selected near-SPD Cholesky follow-up — 2026-10-29

[Section 14.5 evidence](chapter-14-near-spd-followup.md) extends COV-68 with exact dyadic determinant/pivot references, factor/reconstruction/forward/backward-solve checks and singular/indefinite boundary rejection. All 23 Chapter 14 files compiled and 13 scripts passed. Nondyadic rounding, arbitrary right-hand-side conditioning, broader ranges and independent review remain open. This scoped run follows V-34; twenty-four categories remain partially addressed.

## Selected restricted-SVD ordering follow-up — 2026-10-29

[Section 14.6 evidence](chapter-14-svd-order-followup.md) partially addresses COV-67 with twelve reconstruction, direction-orthonormality, sorted-summary and thresholded-solve cases. Factor-order directions must be paired with original magnitudes, not blindly zipped with the sorted summary. All 24 Chapter 14 files compiled and 14 scripts passed. Reference-report/integration and independent-review scope remains open. This scoped run follows V-34; twenty-five selected categories remain partially addressed.

## Full execution reconciliation — fourth refresh

[V-35 evidence](runtime-refresh-2026-10-29-r4.md) covers all eight subsequent Chapter 13/14 checkers at `3e185649bf53f5a72ad9e1869d17762110444a26`: 452 files compiled, 241 scripts passed and 453 source/fixture blobs verified before/after. Earlier scoped-only wording is historical. Twenty-five categories remain partially addressed; independent review and approval remain pending. Next executable investigation: COV-68 Section 14.1 unequal-spectrum small-eigenvalue cancellation, using an exact/high-precision reference before any correction.

## Unequal-spectrum correction — 2026-10-29

[Section 14.1 evidence](chapter-14-unequal-spectrum-followup.md) records a confirmed representable-small-eigenvalue cancellation defect, its original regression failure and corrected exact/Decimal references. All 25 Chapter 14 files compiled and 15 scripts passed. This source change follows V-35; a new full-book run is not claimed. COV-68 remains partially open and twenty-five categories remain partially addressed. Next executable item: Section 14.2 duplicate spectral path against the unequal-spectrum references; independent review/platform/release gates remain pending.

## Spectral-report integration and correction — 2026-10-29

[Section 14.2 evidence](chapter-14-spectral-report-followup.md) confirms the shared Section 14.1 solver path and corrects one-shot input reuse and squared-norm underflow. The original checker failure and tiny-error probe are retained; all 26 chapter files compiled and 16 scripts passed after correction. This scoped change follows V-35. Twenty-five categories remain partially addressed. Next executable item: Section 14.1 off-diagonal averaging/symmetry boundary; broader numerical, platform and independent-review gates remain open.

## Symmetry-policy boundary follow-up — 2026-10-29

[Chapter 14 evidence](chapter-14-symmetry-policy-followup.md) adds nine adjacent represented-threshold cases, exact-versus-tolerant symmetry contrast and three subnormal midpoint cases. No implementation change was justified; the manuscript now states the policies and absolute floor. All 27 chapter files compiled and 17 scripts passed. This checker addition follows V-35; twenty-five categories remain partially addressed. Next executable item: Section 14.5 tiny nondyadic reconstruction norms, then full-book runtime refresh after related fixes. Independent review, environment and release gates remain pending.

## Tiny Cholesky diagnostic correction and V-36 — 2026-10-29

[Correction evidence](chapter-14-cholesky-norm-followup.md) retains an original zero-error underflow failure and five Decimal norm/solve-report cases; all 28 Chapter 14 files compiled and 18 scripts passed. [V-36 full execution](runtime-refresh-2026-10-29-r5.md) subsequently compiled 456 sources and passed 245 scripts with 457 verified blobs at `82ec4d155b0b370008fab16f42a9781b7c4cd322`, covering all four recent checker additions and spectral/Cholesky corrections. Twenty-five categories remain partially addressed; independent review and release gates stay open. Next executable item: COV-67 Section 14.8/14.10 literal-report versus computed-factor integration and meaningful fault detection.

## Computed diagnostic integration follow-up — 2026-10-29

[Section 14.8 evidence](chapter-14-diagnostic-integration-followup.md) replaces literal-factor diagnostics with actual helper calls and independently recomputed errors, retaining known numeric checks. Four helper calls are observed and five wrong outputs detected. All 29 chapter files compiled and 19 scripts passed. This source/checker change follows V-36; twenty-five categories remain partially addressed. Next executable item: Section 14.10 reference-report integration under COV-67. Broader numerical, independent-review, environment and release gates remain pending.

## Final-assessment integration follow-up — 2026-10-30

[Section 14.10 evidence](chapter-14-final-integration-followup.md) propagates computed helper results and recomputes factor/matrix diagnostics. Four helper calls and five corrupted outputs are checked; all 30 chapter files compiled and 20 scripts passed. This source/checker change follows V-36; twenty-five categories remain partially addressed. The selected 14.8/14.10 wiring obligation is addressed, while COV-67 and independent review remain open. Next executable item: Chapter 15 COV-71 Hessian finite-difference accuracy/convergence and representability, beginning with its coverage map. Environment and release gates remain pending.

## Selected Hessian accuracy follow-up — 2026-10-30

[Chapter 15 evidence](chapter-15-hessian-accuracy-followup.md) checks 18 analytic Hessian entries against independent 90-digit direct-valuation stencils at one interior input, with selected second-order ladders and rate-time block integration. These stencils are supplemental references, not a production numerical Hessian API. All 22 chapter files compiled and 12 scripts passed; implementation unchanged. COV-71 remains partially open and twenty-five categories remain partially addressed. This checker follows V-36; next executable item is Section 15.9 centered Jacobian-column convergence and selected cancellation/asymmetry. Independent-review, platform and release gates remain pending.

## Production-float Jacobian accuracy follow-up — 2026-10-30

[Section 15.9 evidence](chapter-15-jacobian-accuracy-followup.md) checks eighteen float-column/reference pairs, four selected second-order ladders, three tiny-step cancellation cases and one unequal represented-offset case. The manuscript clarifies approximation limits; implementation unchanged. All 23 chapter files compiled and 13 scripts passed. This follows V-36; twenty-five categories remain partially addressed. Next executable item: COV-72 Section 15.8 zero iso-variance denominator and rate-sign-crossing/domain rejection, followed by full-book reconciliation. Independent-review, environment and release gates remain pending.

## Level-set boundary follow-up and V-37 — 2026-10-30

[Section 15.8 evidence](chapter-15-level-set-boundary-followup.md) adds selected zero/adjacent iso-variance and signed-rate/maturity-domain cases; implementation unchanged. All 24 Chapter 15 files compiled and 14 scripts passed. [V-37 full evidence](runtime-refresh-2026-10-30.md) subsequently compiled 461 sources and passed 250 scripts with 462 hashes verified before/after at `28af429b7695520536cf4a3384af1318614e31aa`. This covers all recent scoped integrations and accuracy checkers. Twenty-six categories are partially addressed; independent review and approval remain pending. Next executable item: Section 15.8 finite rate-shock addition and extreme intermediate range with independent level-preservation references.

## Adjusted-maturity range correction — 2026-10-30

[Section 15.8 evidence](chapter-15-maturity-range-followup.md) retains three original range-failure probes and the regression failure; the correction preserves the represented quotient through exact rational intermediates and states final range/underflow rejection. Eight Decimal references and five rejection cases pass; all 25 chapter files compiled and 15 scripts passed. This source/checker change follows V-37; twenty-six categories remain partially addressed. Next executable item: COV-72 Sections 15.4/15.6 covariance symmetry/PD and gradient/Hessian consistency. Independent-review, platform and release gates remain pending.

## Covariance derivative consistency correction — 2026-10-30

[Sections 15.4/15.6 evidence](chapter-15-covariance-consistency-followup.md) retains a confirmed accepted-asymmetry derivative inconsistency and original regression failure. Shared symmetric normalization/finite PD screening now passes three covariance cases, nine exact-quadratic references and selected rejection cases; all 26 chapter files compiled and 16 scripts passed. This source/checker change follows V-37. Twenty-six categories remain partially addressed. Next executable item: covariance determinant underflow/cancellation benchmarks, then full-book reconciliation of the maturity/covariance changes. Independent-review, platform and release gates remain pending.

## Covariance screen benchmarks and V-38 — 2026-10-30

[Exact-reference screen evidence](chapter-15-covariance-screen-followup.md) records three exact-PD exclusions from the limited float determinant contract, three accepted near-PD cases and two non-PD cases. Implementation unchanged; all 27 Chapter 15 files compiled and 17 scripts passed. [V-38 full evidence](runtime-refresh-2026-10-30-r2.md) subsequently compiled 464 sources and passed 253 scripts with 465 hashes verified before/after at `378775bc25034f5551f1d1efa51d836da77d6737`, including all maturity/covariance corrections. Twenty-six categories remain partially addressed. Next executable item: Chapter 16 COV-73/75 optimizer status/scaling obligations from its coverage map; independent-review, platform and release gates remain open.

## Optimizer status and Armijo follow-up — 2026-10-30

[Chapter 16 evidence](chapter-16-optimizer-status-followup.md) adds nine adjacent sufficient-decrease cases, objective/backtracking counts and selected stationary/stagnation/budget/no-descent states. All 21 chapter files compiled and 11 scripts passed; implementation unchanged. This checker follows V-38; twenty-seven categories are partially addressed and COV-73 remains open. Next executable item: Section 16.7 multistart/best-observed independent stationary-cubic roots and local classification; no global-optimum certification. Independent-review, platform and release gates remain pending.

## Independent multistart reference follow-up — 2026-10-30

[Section 16.7 evidence](chapter-16-multistart-reference-followup.md) checks four default starts against independent 80-digit stationary roots/objectives and curvature classification, plus real failed/mixed pools. Gradient-tolerance at the middle local maximum explicitly preserves the distinction from a minimum/global certificate. All 22 chapter files compiled and 12 scripts passed; implementation unchanged. This follows V-38; twenty-eight categories are partially addressed. Next executable item: Section 16.7 scaling transforms, Hessian condition and stable-step bounds with units explicit. Independent-review, platform and release gates remain pending.

## Scaling references and V-39 — 2026-10-30

[Section 16.7 evidence](chapter-16-scaling-reference-followup.md) independently checks Hessian transforms/condition numbers, four coordinate round trips, twelve curvature stencils and six real scalar stable/boundary/unstable mode runs. All 23 Chapter 16 files compiled and 13 scripts passed; implementation unchanged. [V-39 full evidence](runtime-refresh-2026-10-30-r3.md) then compiled 467 sources and passed 256 scripts with 468 hashes verified before/after at `18be350b40cc2a0a963e0c5fd91b793cf0c3c634`, covering all three Chapter 16 follow-ups. Twenty-eight categories remain partially addressed. Next executable item: COV-75 Sections 16.2–16.4 derivative representability and denominator extremes. Independent-review, environment and release gates remain pending.

## Derivative boundary correction and V-40 — 2026-10-30

[Sections 16.2–16.4 evidence](chapter-16-derivative-boundary-followup.md) retains collapsed-stencil/denominator failures, adds pre-callback geometry/range validation and finite callback checks, and passes 35 guard cases, nine exact polynomial pairs, one unequal-offset case and three nonfinite-result cases. All 24 Chapter 16 files compiled and 14 scripts passed. [V-40 full execution](runtime-refresh-2026-10-30-r4.md) then compiled 468 sources and passed 257 scripts with 469 required hashes verified before/after at `fe24a814a26fb542c7b5d6e0f34a0df8ff6eb6a7`. This covers the three source corrections and new checker after V-39. Twenty-eight categories remain partially addressed; none is closed by the register. Next executable item: COV-75 Section 16.6 scalar secant-curvature product/threshold and callback boundaries, with exact represented-number expectations. Independent-review, supported-platform and release gates remain pending.

## Scalar secant boundary correction — 2026-10-30

[Section 16.6 evidence](chapter-16-secant-boundary-followup.md) preserves four original probes and a failing regression, corrects exact represented-product threshold comparison and callback/quotient validation, and passes twelve exact quadratic pairs, six adjacent-threshold gates, one rounded-product boundary, two absolute-threshold rejections and nineteen callback/range cases. All 25 Chapter 16 files compiled and 15 scripts passed at `af766375b896e5742389d343580dbd8d426afd33`; the complete scoped manifest matches the published tree. Fresh full-book inventory is 469 Python files and 258 check/test scripts, not new full-book execution counts. This source/checker change follows V-40; the last full run remains 468/257/469 at its earlier pin. Twenty-eight categories remain partially addressed, none closed by the register. Next executable item: COV-75 Section 16.6 Newton/quasi-Newton update scaling and represented-range boundaries with exact rational quadratic updates. Independent-review, supported-platform and release gates remain pending.

## Newton range correction and V-41 — 2026-10-30

[Section 16.6 evidence](chapter-16-newton-range-followup.md) retains underflow/overflow failures and the original regression, combines Newton/quasi-Newton updates before final rounding, and checks six range cases, twenty-eight scaled updates, seven one-step solves, rounding/stopping limits and twenty-three invalid cases. All 26 Chapter 16 files compiled and 16 scripts passed. [V-41 full execution](runtime-refresh-2026-10-30-r5.md) subsequently compiled 470 sources, passed 259 scripts and verified 471 required hashes before/after at `a10a3efdbc8c69abb68089855216f70f070996da`, covering both recent Section 16.6 changes and new checkers after V-40. Twenty-eight categories remain partially addressed; none is closed by the register. Next executable item: COV-74 Section 16.8 observation/weight/metric validation and extreme residual-metric range, beginning with independent exact/Decimal references. Independent-review, supported-platform and release gates remain pending.

## Residual metric correction and V-42 — 2026-10-30

[Sections 16.8–16.10 evidence](chapter-16-residual-metric-followup.md) preserves two initial failures and eight probes, corrects exact represented means/scaled RMS and shares the checked arithmetic with project/final report paths. Thirty-two metric/reference pairs, six cancellation permutations, thirty-nine invalid cases, two weighted/residual references and six entry-point reference sets pass; two shared-helper calls and strict JSON are checked. The final scoped run compiled 28 chapter files and passed 18 scripts. [V-42 full execution](runtime-refresh-2026-10-30-r6.md) compiled 472 sources, passed 261 scripts and verified 473 required hashes before/after at `c42fb1965a8febe91dc9ed310b2db9b0d0cb9ca2`, covering all three source changes and two new checkers. Twenty-eight categories remain partially addressed; none closed by the register. Next executable item: COV-74 Section 16.8 fit-rate/curvature/gradient/weighted-loss range boundaries, with exact represented-observation references. Independent-review, supported-platform and release gates remain pending.

## Calibration arithmetic range correction — 2026-10-30

[Section 16.8 evidence](chapter-16-calibration-range-followup.md) preserves seven original probes and an exit-1 regression, corrects complete fit/curvature/gradient/weighted-loss expression range handling and rejects nonzero-to-zero results. Nine independent Decimal fits, eight gradient references, five curvature references, four weighted-loss references and eight final-range rejections pass. All 29 chapter files compiled and 19 scripts passed at `7968be83604ba6d801b05e6d61ba9fec8726e7b6`; all corrected scoped hashes match the published tree. Current inventory is 473 Python files and 262 check/test scripts, not new full-runtime counts. This source/checker change follows V-42; its full pass remains historical for changed code. Twenty-eight categories remain partially addressed; none closed by the register. Next executable item: COV-74 Sections 16.9/16.10 normalized analytic-rate, curvature and gradient copies; preserve their distinct normalized objective scale and avoid scaling an already-rounded raw result. Independent-review, supported-platform and release gates remain pending.

## Normalized calibration correction and V-43 — 2026-10-30

[Sections 16.9/16.10 evidence](chapter-16-normalized-calibration-followup.md) preserves eight probes and the original regression, corrects analytical-rate/curvature/gradient expression range while retaining normalized scale and residual-rounding policies. Sixteen Decimal fit pairs, ten curvature references, six gradients, eighteen rejections and three scale/policy checks pass. All 30 chapter files compiled and 20 scripts passed. [V-43 full execution](runtime-refresh-2026-10-30-r7.md) then compiled 474 files, passed 263 scripts and verified 475 required hashes before/after at `b5b04e9fbee6367d5d81136d47d9475c96a2dea5`, covering this and the preceding Section 16.8 correction/checker. Manuscript candidate-runtime wording is reconciled; independent/platform/release claims are not granted. Twenty-eight categories remain partially addressed, none closed by the register. Next executable item: COV-74 Section 16.10 per-candidate training/holdout metrics and acceptance at each returned optimizer rate; current final assessment retains benchmark metrics. Objective/loss range and broader conditioning/review obligations remain open.

## Final per-candidate assessment follow-up — 2026-10-30

[Section 16.10 evidence](chapter-16-final-candidate-followup.md) retains the benchmark-only baseline and original failed check, adds actual-rate training/holdout residuals/metrics, recomputed loss/gradient, retained limits and named provisional acceptance gates. Six candidate reference sets (48 metric fields), six deliberately failed status/rate/gradient/loss/holdout/budget scenarios, a nonfinite rejection and stale-rate exact values pass. An intermediate reference-checker error and its correction are retained separately. All 31 chapter files compiled and 21 scripts passed at `2d61bd212ca245578b0f6d192dbe824a71132d6c`; scoped hashes match the published tree. Current inventory is 475 Python files/264 check-test scripts, not a new full run. This source/checker change follows V-43. Twenty-eight categories remain partially addressed; none closed by the register. Next executable item: COV-75 Section 16.10 exact Exercise1–5 (curvature4) and Exercise11–13 (curvature1) objective/history references, kept distinct from three-observation curvature14. Broader threshold/configuration, range, manual proof, independent-review, supported-platform and release obligations remain open.

## Exact cumulative-objective follow-up and V-44 — 2026-10-30

[Section16.10 evidence](chapter-16-cumulative-objective-followup.md) preserves the missing-scope baseline failure, adds distinct computed curvature4/1 exercise evidence alongside aggregate curvature14, and checks eight expanded-polynomial fields, thirty-three exact gradient-descent history fields, one-step Newton and two wrong-scope variants. This addresses a selected coverage gap, not a demonstrated original arithmetic defect. All 32 chapter files compiled and 22 scripts passed. [V-44 full execution](runtime-refresh-2026-10-30-r8.md) compiled 476 files, passed 265 scripts and verified 477 required hashes before/after at `692e8ffd8425c2fab1a0695f8c647b4fc5a128d7`, also covering the preceding candidate-assessment change/checker. Twenty-eight categories remain partially addressed; none closed by the register. Next executable item: COV-74 Sections16.9/16.10 normalized objective/loss intermediate range and false-zero cases, using exact represented-residual expectations. Remaining exercise proofs, thresholds/configuration, conditioning, independent-review, supported-platform and release obligations stay open.

## Normalized loss range correction — 2026-10-30

[Sections16.9/16.10 evidence](chapter-16-normalized-loss-followup.md) preserves eight baseline probes and the original regression, corrects complete normalized half-square sums and rejects nonzero-to-zero normalization/loss results. Fourteen independent Decimal loss pairs, fourteen range/input rejections, the representable collective-subnormal case and a direct normalization-underflow rejection pass. All 33 chapter files compiled and 23 scripts passed at `4c122d5aea349f6e4802ce9201814008d2252b70`; corrected scoped hashes match the published tree. Current inventory is 477 Python files/266 check-test scripts, not a new full run. This two-source/one-checker batch follows V-44; its earlier full-runtime counts remain historical for changed sources. Twenty-eight categories remain partially addressed; none closed by the register. Next executable item: COV-75 Section16.8 lab step10 rank-deficient two-parameter `m(a,b)=a+b` example, absent in the original coverage map's executable scope; add rank/null-direction/unchanged-prediction references. Broader price/residual/update range, acceptance/configuration, conditioning, independent-review, supported-platform and release obligations remain open.

## Rank-deficient lab follow-up and V-45 — 2026-10-30

[Section16.8 evidence](chapter-16-identifiability-followup.md) preserves the absent-lab baseline failure and adds the fixed `m(a,b)=a+b` example with computed minors/rank/normal matrix. Eleven exact parameter cases, three rank minors, five null-vector products, strict JSON and two wrong-output variants pass. This supplies the selected missing lab-step example, not a general numerical-rank method or independent sign-off. All 34 chapter files compiled and 24 scripts passed. [V-45 full execution](runtime-refresh-2026-10-30-r9.md) compiled 478 files, passed 267 scripts and verified 479 required hashes before/after at `0e2f5e4eebc9b3e0328a3bba2c6e0d7f88954db3`, also covering preceding normalized-loss changes/checker. Twenty-eight categories remain partially addressed; none closed by the register. Next executable item: COV-76 Section17.4 adjacent-float active-set transition/endpoints around the exact rational uncapped optimum, with independent weights/multiplier/value references. Preserve tiny-empty rejection and leave broader tolerance/degeneracy, manual proof, independent-review, supported-platform and release obligations open.
