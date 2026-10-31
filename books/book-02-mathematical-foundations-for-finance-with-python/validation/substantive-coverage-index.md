# Book 02 — Substantive coverage index and remediation queue

**Date:** 2026-10-28
**Scope:** 215/215 numbered sections across21 chapters mapped.
**Disposition:** Mapping pass complete; coverage gaps, independent reviews and release acceptance remain open.

This index consolidates source-level comparisons of manuscript claims, examples, exercise/solution tasks, labs, projects and actual assertions. “Mapped” means the evidence or its absence is documented. It does not mean every claim is tested, every solution is correct, or a reviewer has approved the material. Ninety COV categories describe recurring evidence gaps; they are not ninety confirmed software defects or a severity score.

## Complete section map

| Chapter | Sections | Coverage records |
|---|---:|---|
| 01 | 15 | [1.1–1.5](coverage-sections-01-01-05.md), [1.6–1.10](coverage-sections-01-06-10.md), [1.11–1.15](coverage-sections-01-11-15.md) |
| 02 | 10 | [2.1–2.5](coverage-sections-02-01-05.md), [2.6–2.10](coverage-sections-02-06-10.md) |
| 03 | 10 | [Chapter3](coverage-chapter-03.md) |
| 04 | 10 | [4.1–4.6](coverage-sections-04-01-06.md), [4.7–4.8](coverage-sections-04-07-08.md), [4.9–4.10](coverage-sections-04-09-10.md) |
| 05 | 10 | [Chapter5](coverage-chapter-05.md) |
| 06 | 10 | [Chapter6](coverage-chapter-06.md) |
| 07 | 10 | [Chapter7](coverage-chapter-07.md) |
| 08 | 10 | [Chapter8](coverage-chapter-08.md) |
| 09 | 10 | [Chapter9](coverage-chapter-09.md) |
| 10 | 10 | [Chapter10](coverage-chapter-10.md) |
| 11 | 10 | [Chapter11](coverage-chapter-11.md) |
| 12 | 10 | [Chapter12](coverage-chapter-12.md) |
| 13 | 10 | [Chapter13](coverage-chapter-13.md) |
| 14 | 10 | [Chapter14](coverage-chapter-14.md) |
| 15 | 10 | [Chapter15](coverage-chapter-15.md) |
| 16 | 10 | [Chapter16](coverage-chapter-16.md) |
| 17 | 10 | [Chapter17](coverage-chapter-17.md) |
| 18 | 10 | [Chapter18](coverage-chapter-18.md) |
| 19 | 10 | [Chapter19](coverage-chapter-19.md) |
| 20 | 10 | [Chapter20](coverage-chapter-20.md) |
| 21 | 10 | [Chapter21](coverage-chapter-21.md) |
| **Total** | **215** | **26 scoped mapping records** |

Each map names inspected source revision and assertion files. The records were produced sequentially at different revisions; this is not a claim that all maps were re-reviewed against one new source snapshot.

## Evidence that remains established

- [Full pinned runtime pass](pinned-revision-runtime-validation.md):444 Python files compiled;233 check/test scripts exited zero on Python3.12.14/Linux at `2366ddd9ea146f841ad2822ffa5193bd637e4e9d`. Aggregates repeat checks.
- Filename inventory covers215 sections; substantive mapping now also covers215. Neither supplies a line/branch-coverage percentage or proof of exercise completeness.
- Static link audit and sampled GitHub rendered markup are recorded separately. They do not establish full visual/browser navigation.
- Independent mathematical/editorial reviewers remain unassigned; canonical approval has not been granted.

The mapping pass added validation documents and narrowed several manuscript descriptions to the actual checks, including10.7 refinement versus convergence order,13.6 dependent-column test wording and18.9 nonfinite-derivative rejection. These prose changes do not create a new runtime result. Prior runtime results remain tied to their pinned source.

## Remediation order

Priorities below are a work order based on potential effect and evidence dependencies, not an adjudicated defect severity. Confirm each issue with a minimal independent reference before changing numerical behavior. Assign responsible implementer and independent reviewer before closing a review item.

| Queue | Material | Concrete next result | Closure evidence |
|---|---|---|---|
| R1 Numerical contracts and range | COV-31/32,45,51,54,61,68,71,75,80,87; related focused fixes | Review duplicate small-rate/derivative/rank/covariance/scale helpers, beginning with15.2 finite-difference guards and12.5 target-dependent rank threshold. Distinguish confirmed defects from restricted teaching domains. | Independent expected behavior, minimal reproducer, stated contract, targeted regression/fix where justified, exact revision and rerun. |
| R2 Independent numerical oracles | COV-49/50,52,55/56,64/65,67,70,79,82 | Verify reported convergence orders/estimators, nonzero full-Hessian contraction, adaptive rejection semantics and bracket/call diagnostics with independently derived values. | Assertions that can catch a plausible wrong result; avoid self-comparison or literal-to-literal checks. |
| R3 Report and project contracts | COV-15/28,41,53,57,58/60,62/63,66,69/70,74,77/78,81,83,86,88/89 | Reconcile promised fields/inputs with actual reports; address19.9 missing scenario inputs,15.9 portfolio error fields,14.9 covariance-eigenpair scope and21.9 sensitivity diagnostics. | Published schema/scope, meaningful field and failure tests, re-fetched source/report verification. |
| R4 Remaining exercise and proof evidence | Exact-input/manual categories across COV-01–90 | Review all documented unasserted derivations, worked solutions, assumptions, units and applied tasks; decide which need executable cases and which need manual sign-off. | Named reviewer with exact sections/revision and conclusions; no inference from passing script counts. |
| R5 Integration and reproducibility | COV-26/27,29,44,73/74,76,83,86,88/89 | Review aggregate dependencies, CLI/error paths, manifest/schema behavior, event logs and input provenance. | Clean-snapshot runs and artifacts tied to source, fixtures, environment, command and outcomes. |
| R6 Navigation, editorial and environments | G2/G5/G6/G7 | Complete full-book navigation/editorial review, declare supported Python/platform matrix and validate reviewed candidate. | Actual platform results; no unexecuted Windows or version-support claims. |
| R7 Authorized decision | G4/G8 | Complete independent mathematical review and obtain authorized canonical decision for exact release scope. | Identified reviewer/authority, resolved findings or explicit accepted exceptions, revision and intended use. |

## Remediation progress

R1: Section 15.2 finite-difference guards fixed; 21 files compiled and 11 Chapter 15 check scripts passed, including nine boundary methods. [Scoped evidence](chapter-15-scalar-difference-followup.md). COV-71 remains partially open. Section 12.5 target-dependent rank threshold also fixed and its column-equilibration contract documented; 21 files compiled and all 11 Chapter 12 scripts passed. [Rank follow-up](chapter-12-rank-target-scaling-followup.md). COV-61 remains partially open. R2/R3: Section 15.9 now has an independent path-series oracle across nine shocks and complete signed/absolute portfolio error fields. All 21 Chapter 15 files compiled and 11 scripts passed; three contraction mutations were detected. [Taylor follow-up](chapter-15-taylor-oracle-followup.md). COV-70 remains partially open for final-assessment/shared-dependency review. R3/R5: Section 19.9 now retains full validated inputs and jump schedules; ten report cases and selected event traces pass. All 21 Chapter 19 files compiled and 11 scripts passed. [Input provenance follow-up](chapter-19-input-provenance-followup.md). COV-83 remains partially open. R2: adaptive RK4 policy now has selected exact-polynomial and callback-trace checks, including forced rejection and unchanged retry state/time; all nine intentional policy mutations were detected. [Adaptive follow-up](chapter-19-adaptive-policy-followup.md). COV-82 remains partially open; 21 chapter files compiled and 11 scripts passed. R2/R3: Section 14.9 now reports and independently checks its fixed covariance eigenpairs, including pairing, reconstruction and orthogonality; four corrupted reports were detected. [Covariance follow-up](chapter-14-covariance-eigenpair-followup.md). All 21 Chapter 14 files compiled and 11 scripts passed. COV-69 remains partially open. Next selected report-contract item: Section 21.9 finite-difference sensitivity diagnostics (COV-89).

## Disposition rules

1. Preserve each gap's original evidence and link the confirmed disposition. Do not silently rewrite a gap as a pass.
2. A missing exercise-specific assertion is not automatically a software bug; a general proof obligation is not resolved by finite random cases.
3. A restricted API may be valid if manuscript scope is explicit. Reconcile the contract before broadening it.
4. Retest affected code/fixtures when changed; repeat the full agreed release suite at the reviewed release revision.
5. Keep mapping completion, runtime execution, independent review and approval as separate tracker states.

G3 therefore remains **mapped; gaps open**, rather than a clean coverage gate. The [review checklist](remaining-review-checklist.md) and [progress tracker](PROGRESS.md) retain outstanding work.

## Latest integrated-report follow-up — 2026-10-29

Section 21.9's finite-difference diagnostic, JSON serialization and selected failure-propagation gaps are addressed. [Evidence](chapter-21-integrated-diagnostics-followup.md): 19 files compiled, 10 scripts passed, including 18 integration methods. COV-89 remains partially open; a full-book runtime refresh follows these code changes.

## Full runtime refresh — 2026-10-29

The [latest candidate run](runtime-refresh-2026-10-29.md) includes these remediations: 444 sources compiled and 233 scripts exited zero at `37aac57a72303a6d4178790f8d172495e2bc0ada`, with 467 downloaded blobs verified before and after execution. This supersedes the earlier full run as latest execution evidence; the mapping and partial COV dispositions do not become independent review or approval.

## Remediation monitoring

The [gap-remediation register](gap-remediation-register.md) consolidates seven selected partial dispositions and remaining obligations. No whole-category closure or percentage is inferred from those follow-ups.

## Compression/report follow-up — 2026-10-29

Section 14.9 now computes loss from the actual compression matrices and checks its spectral bound across selected diagonal cases, with input/unit metadata. [Evidence](chapter-14-compression-bound-followup.md): 21 chapter files compiled and 11 scripts passed. This change is subsequent to the recorded full-book refresh; COV-69 retains independent-review and broader-scope obligations.

## Candidate acceptance follow-up — 2026-10-29

Section 16.9 now records and evaluates every iterative candidate's training/holdout metrics and recomputed normalized loss/gradient. [Evidence](chapter-16-candidate-acceptance-followup.md): 20 files compiled and 10 scripts passed, including selected negative acceptance cases. COV-74 is partially addressed; the [register](gap-remediation-register.md) now tracks eight selected partial categories. Next selected numerical-contract review: Section 20.5 extreme error reporting (COV-87).

## Error-range follow-up — 2026-10-29

Section 20.5 no longer returns infinite error magnitudes from finite inputs; it raises explicit range errors, while the exact tolerance decision remains available independently. [Evidence](chapter-20-error-range-followup.md): 19 sources compiled and 10 scripts passed, including 20 tolerance methods. COV-87 is partially addressed; the [register](gap-remediation-register.md) tracks nine selected partial categories. Next selected contract item: Section 20.6 numeric input/output validation.

## Section 20.6 contract follow-up

The [metamorphic PV contract record](chapter-20-metamorphic-contract-followup.md) documents explicit numeric validation and range policy, including empty-portfolio rates. All 19 Chapter 20 files compiled and 10 scripts passed. This extends partial COV-87 remediation; no independent approval or new full-book runtime is implied.

## Bracket diagnostic follow-up

The [Section 18.8 bracket audit](chapter-18-bracket-audit-followup.md) adds actual sign/history and callback-count evidence across seven paths. All 21 chapter files compiled and 11 scripts passed. COV-79 is partially addressed; the register now tracks ten selected partial categories.

## KKT rejection follow-up

The [Section 17.9 KKT record](chapter-17-kkt-rejection-followup.md) adds independent field checks and isolated primal/dual/stationarity/complementarity failures. All 20 chapter sources compiled and 10 scripts passed; optimizer unchanged. COV-76 is partially addressed; eleven selected partial categories are tracked. Next selected report-contract review: Section 17.9 finite financial-report arithmetic (COV-77).

## Financial-report range follow-up

The [Section 17.9 financial-range record](chapter-17-financial-range-followup.md) documents explicit range errors and avoided intermediate cost overflow, while preserving underflow limitations. All 20 chapter sources compiled and 10 scripts passed. COV-77 is partially addressed; twelve selected partial categories are tracked.

## Final allocation assessment follow-up

The [Section 17.10 follow-up](chapter-17-final-allocation-followup.md) adds multiplier/rejection evidence and fixes an empty interval hidden by rounded cap addition. All 20 chapter sources compiled and 10 scripts passed. COV-78 is partially addressed; thirteen selected partial categories are tracked.

## Factor-limit audit follow-up

The [Section 12.9 factor audit](chapter-12-factor-audit-followup.md) adds retained limits and meaningful rejection/boundary evidence. All 21 chapter sources compiled and 11 scripts passed. COV-62 is partially addressed; fourteen selected partial categories are tracked.

## Full execution reconciliation — second refresh

All code follow-ups recorded above through the factor audit are included in the [second full-book refresh](runtime-refresh-2026-10-29-r2.md): 444 sources compiled and 233 scripts exited zero at `7ee99f60d5089510f860a0b6f695f971beb2eac6`, with 445 required sources/fixture blobs verified. Earlier statements about subsequent scoped-only changes remain historical; this shared run now covers them. Fourteen categories remain partially addressed; no independent closure or approval is inferred.

## Quadrature oracle follow-up

The [Section 10.7 quadrature record](chapter-10-quadrature-order-followup.md) adds exact polynomial order/estimator evidence and selected smooth-integrand checks. All 21 chapter sources compiled and 11 scripts passed; algorithm unchanged. COV-55 is partially addressed; fifteen selected partial categories are tracked.

## Derivative accuracy follow-up

The [Section 8.6 record](chapter-08-difference-order-followup.md) adds exact error ladders and selected cancellation evidence. All 21 chapter files compiled and 11 scripts passed; algorithm unchanged. COV-49 is partially addressed; sixteen selected partial categories are tracked.

## Comparator audit follow-up

The [Section 8.9 comparator record](chapter-08-comparator-audit-followup.md) adds explicit error/tolerance evidence and rejects nonfinite false-pass calculations. All 21 chapter files compiled and 11 scripts passed. COV-50 is partially addressed; seventeen selected partial categories are tracked.

## Derivative helper-guard follow-up

The [Section 8.8 guard record](chapter-08-helper-guards-followup.md) adds finite-output validation and avoids an unnecessary Richardson overflow. All 21 chapter files compiled and 11 scripts passed. COV-51 is partially addressed; eighteen selected partial categories are tracked.

## Normalized-sensitivity range follow-up

The [Section 8.8 sensitivity record](chapter-08-sensitivity-range-followup.md) adds explicit zero-normalizer and nonfinite report handling, with independent ratio checks. All 21 chapter files compiled and 11 scripts passed. COV-51 remains partially open; the selected register count remains eighteen.

## Projection diagnostic follow-up

The [Section 11.6 projection record](chapter-11-projection-audit-followup.md) adds rational coordinate/scalar/error checks and fixed-report residual norms. All 21 chapter files compiled and 11 scripts passed. COV-60 is partially addressed; nineteen selected partial categories are tracked.

## Relative-distance contract follow-up

The [Section 11.4 record](chapter-11-relative-distance-followup.md) adds direct three-norm/denominator/boundary evidence. All 21 chapter files compiled and 11 scripts passed; implementation unchanged. This extends partial COV-60 remediation; the selected count remains nineteen.

## Exposure policy audit follow-up

The [Section 11.9 policy record](chapter-11-policy-audit-followup.md) retains decision inputs and checks isolated effective-threshold cases. All 21 chapter files compiled and 11 scripts passed. COV-59 is partially addressed; twenty selected partial categories are tracked.

## Budget boundary follow-up

The [Section 11.7 record](chapter-11-budget-boundary-followup.md) verifies the missing budget path and selected inclusive/adjacent constraints. All 21 chapter files compiled and 11 scripts passed; implementation unchanged. This extends COV-59; the selected category count remains twenty.

## Final vector assessment follow-up

The [Section 11.10 record](chapter-11-final-nonfinite-followup.md) adds direct nonfinite/overflow checks and strict JSON evidence. All 21 chapter files compiled and 11 scripts passed; implementation unchanged. This extends partial COV-60 remediation; the selected count remains twenty.

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

## Adjacent active-set boundary correction — 2026-10-30

[Section17.4 evidence](chapter-17-active-boundary-followup.md) preserves adjacent probes and the original failed check, corrects near-transition dual cancellation with exact decimal-model formulas, and separates rounded display, exact model geometry and numerical activity. Nine cap sets yield63 weight/dual/value/geometry checks and27 activity reports across three tolerances. All21 Chapter17 files compiled and11 scripts passed, including existing tiny-empty-interval regressions, at `bf81791b09530e2711c89ca4960d62bd571bb9b9`; corrected scoped hashes match the published tree. Current inventory is479 Python files/268 check-test scripts, not a new full run. This helper/checker change follows V-45. Twenty-eight categories remain partially addressed; none closed by the register. Next executable item: COV-76 Section17.4 cap-zero nonunique lower-bound/cap multiplier families, exact stationarity/complementarity and isolated sign failures. Broader tolerance units/scales, conditioning, independent-review, supported-platform and release obligations remain open.

## Degenerate multiplier family and V-46 — 2026-10-30

[Section17.4 evidence](chapter-17-degenerate-multiplier-followup.md) derives the cap-zero family (a,0,a+4/25), checks six parameter sets, three isolated dual-sign/stationarity/complementarity failures and three omitted-family rules. The first run passed against the unchanged helper; no numerical defect was demonstrated. Tiny-negative and zero-tolerance cases distinguish numerical acceptance from exact feasibility. All22 Chapter17 files compiled and12 scripts passed. [V-46 full execution](runtime-refresh-2026-10-30-r10.md) compiled480 files, passed269 scripts and verified481 required hashes before/after at `df656dbbe59bda073bf662392c9f0348fc18cc83`, covering the preceding active-boundary correction/checker too. The manuscript now explains multiplier choice and its escaped lab-command markup is repaired. Twenty-eight categories remain partially addressed; none closed by the register. Next executable item: COV-77 Section17.9 retained report inputs/model/tolerance metadata and deterministic strict-JSON contract; distinguish synthetic model provenance from real-market validation. Broader tolerance units/scales, independent-review, supported-platform and release obligations stay open.

## Allocation report audit contract — 2026-10-30

[Section17.9 evidence](chapter-17-report-contract-followup.md) preserves the initial missing-input-metadata failure and adds candidate/financial inputs, declared tolerances and residual units, fixed synthetic model metadata and schema version1. Four financial sets yield24 independently derived metric checks; six certificate/tolerance cases, strict JSON round-trip and two fresh-process outputs pass. Numerical allocation, financial arithmetic and acceptance rules are unchanged. All23 chapter sources compiled and13 scripts passed at `e5bf5f753a12e8b83f98933682c97f0a55ea9805`; all23 source hashes match the pinned tree and remain unchanged after execution. Current inventory is481 Python files/270 check-test scripts, not a full runtime run. V-46's480/269 full execution is historical for the changed Section17.9 source. Twenty-eight categories remain partially addressed; none closed by the register. Next executable item: COV-78 Section17.10 actual Section17.5 LP-helper integration, independent vertex/objective/certificate references and false-certificate checks; do not call the fixed LP a general solver. Broader report/data governance, mixed-unit tolerance scaling, independent-review, supported-platform and release obligations remain open.

## Final LP integration and V-47 — 2026-10-30

[Section17.10 evidence](chapter-17-final-lp-integration-followup.md) preserves the missing-certificate baseline failure, replaces literal LP assessment inputs with actual Section17.5 computation/certificate calls and independently checks six boundary intersections, four feasible vertices and six certificates (five rejected). Two actual helper calls and five injected wrong outputs are checked. All24 chapter sources compiled and14 scripts passed. [V-47 full runtime](runtime-refresh-2026-10-30-r11.md) compiled482 files, passed271 scripts and verified483 required hashes before/after at `60cd09c1072aec6d6f437b62961d0b4e50cad50c`, including preceding Section17.9 report changes/checker. Twenty-eight selected categories remain partially addressed; none closed by the register. Next executable item: COV-79 Section18.9 project safeguarded-Newton trace endpoint signs, middle-half proposal safeguards, returned-root residuals and exact objective/derivative call accounting; Section18.8 bracket audit is already recorded. Broader mathematical proof, report/data governance, tolerance scaling, independent-review, supported-platform and release obligations remain open.

## Project safeguarded-Newton trace audit — 2026-10-30

[Section18.9 evidence](chapter-18-project-trace-followup.md) logs ten selected pure-polynomial solver paths and independently audits87 trace rows,200 objective calls and87 derivative calls, strict middle-half safeguards, endpoint signs/updates, returned residuals and terminal conditions. Two quadratic paths have100-digit Decimal containment/half-width references; five altered reports are detected. The first new checker run passed against the unchanged helper. All22 Chapter18 files compiled and12 scripts passed at `f431e9daabc74a3cb25b254a2c219573f1267144`; all22 source hashes match the pinned tree and remain unchanged after execution. Current inventory is483 Python files/272 check-test scripts, not a new full runtime pass; V-47 remains the earlier482/271 full execution. Twenty-eight categories remain partially addressed; none closed by the register. Next executable item: COV-80 Section18.5 exact-grid repeated roots, scan/refinement deduplication threshold and nearby distinct-root separation, with polynomial references and explicit nonexhaustive flags. Continuity/uniqueness proofs, project evaluation-error paths, broader financial range/applied scope, independent-review, supported-platform and release obligations remain open.

## Root-scan correction and V-48 — 2026-10-30

[Section18.5 evidence](chapter-18-root-scan-followup.md) preserves false-zero NPV probes, an original regression failure, finite-grid intermediate overflow and an intermediate missing-grid-metadata failure. Complete rational NPV/grid evaluation now prevents those false roots/range failures; nonzero NPV underflow and collapsed grids reject explicitly. Declared configurable merging retains candidates and the default1e-9 threshold; zero threshold preserves selected nearby roots. Thirteen rational NPV references, four repeated-root grids, five merging boundaries, four grid sets and selected range/input cases pass. All23 chapter sources compiled and13 scripts passed. [V-48 full execution](runtime-refresh-2026-10-30-r12.md) compiled484 files, passed273 scripts and verified485 required hashes before/after at `f02d9dc8de4198e2804737313a0ef9e05dcff50d`, including the preceding project-trace checker. COV-80 is newly partially addressed:29 selected categories remain partially addressed, none closed by the register. These are gap categories, not defect counts or completion percentages. Next executable item: COV-80 Section18.6 interpolation curvature-bound and half-width/factor-four references, with extrapolation kept outside the interpolation guarantee. Broader scan completeness, numerical range, independent-review, supported-platform and release obligations remain open.

## Interpolation curvature-bound oracle — 2026-10-30

[Section18.6 evidence](chapter-18-interpolation-bound-followup.md) checks the exact quadratic identity L(q)-f(q)=a(q-A)(B-q), curvature bound and midpoint equality across100 selected quarter-grid queries;16 additional midpoint queries verify factor-four error reduction on interval halving. An extrapolation counterexample keeps the bound's interval hypothesis explicit; three wrong methods are detected. The first checker run passed against the unchanged helper. All24 chapter files compiled and14 scripts passed at `7678af6b436748470a1a1798256d8fd546bcbade`; all24 source hashes match the pinned tree and remain unchanged after execution. Current inventory is485 Python files/274 check-test scripts, not a new full run; V-48 remains the earlier484/273 full execution. Twenty-nine selected categories remain partially addressed; none closed by the register. Next executable item: COV-80 Section18.7 selected exact signed trapezoid/Simpson error/order ladders and three-step first/second derivative sensitivity evidence, rather than error decrease alone. Broader smoothness/conditioning, input/result range, financial model review, independent-review, supported-platform and release obligations remain open.

## Quadrature-order and derivative-step oracle — 2026-10-30

[Section18.7 evidence](chapter-18-order-step-followup.md) adds48 rounded exact rule references,36 measured order checks, three polynomial difference steps and a100-digit Decimal three-step bond study with explicit callback/rounding allowances. Three wrong methods are detected. The first checker run passed against the unchanged helper. All25 chapter sources compiled and15 scripts passed at `497e1892a8bc08b353d711a092f40ddada9531bf`; hashes match the pinned tree and remain unchanged after execution. Current inventory486 Python files/275 check-test scripts is not a full runtime pass; V-48 remains the earlier484/273 run. Twenty-nine categories remain partially addressed; none closed by the register. Next executable item: COV-80 Sections18.7/18.10 finite-difference range contracts, including finite samples, combined numerator/denominator arithmetic and nonzero-to-zero results. Broader conditioning/model, independent-review, supported-platform and release obligations stay open.

## Complete-stencil range correction and V-49 — 2026-10-30

[Sections18.7/18.10 evidence](chapter-18-difference-range-followup.md) preserves five original false-zero/range probes and a failed first regression. Shared complete rational stencils now avoid intermediate numerator/denominator range loss, reject nonfinite/collapsed sample points before callbacks and reject unrepresentable nonzero/final results. Thirteen2500-digit Decimal references,11 point guards,12 callback-value guards,four final-range rejections and a shared-call observation pass. All26 chapter sources compiled and16 scripts passed. [V-49 full execution](runtime-refresh-2026-10-30-r13.md) compiled487 files,passed276 scripts and verified488 required hashes before/after at `e5780915662a4c69e0ef7acbbb961eadc16f2237`, including all three checkers added since V-48. Twenty-nine categories remain partially addressed; none closed by the register. Next executable item: COV-81 Section18.9 project nonfinite-derivative/evaluation-error contract, invalid relative tolerances/iteration controls and callback sequencing, preserving zero-derivative fallback. Broader final applied-scope, conditioning/model, independent-review, supported-platform and release obligations stay open.
