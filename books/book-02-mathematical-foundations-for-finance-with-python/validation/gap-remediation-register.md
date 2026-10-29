# Book 02 — Coverage-gap remediation register

**Updated:** 2026-10-29
**Scope:** Selected follow-ups after the 215-section substantive mapping pass.
**Disposition:** Twenty-five COV categories partially addressed; none closed by this register.

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
| COV-74 | Section 16.9 now evaluates metrics, normalized loss/gradient and acceptance per candidate; independent residual metrics and selected failed candidates/holdout/budget cases checked. | Broader invalid-data, optimizer/threshold and independent-review scope. | [Candidate acceptance](chapter-16-candidate-acceptance-followup.md) |
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
