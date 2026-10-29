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
