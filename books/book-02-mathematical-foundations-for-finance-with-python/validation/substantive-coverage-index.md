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

R1: Section 15.2 finite-difference guards fixed; 21 files compiled and 11 Chapter 15 check scripts passed, including nine boundary methods. [Scoped evidence](chapter-15-scalar-difference-followup.md). COV-71 remains partially open. Section 12.5 target-dependent rank threshold also fixed and its column-equilibration contract documented; 21 files compiled and all 11 Chapter 12 scripts passed. [Rank follow-up](chapter-12-rank-target-scaling-followup.md). COV-61 remains partially open. R2/R3: Section 15.9 now has an independent path-series oracle across nine shocks and complete signed/absolute portfolio error fields. All 21 Chapter 15 files compiled and 11 scripts passed; three contraction mutations were detected. [Taylor follow-up](chapter-15-taylor-oracle-followup.md). COV-70 remains partially open for final-assessment/shared-dependency review. R3/R5: Section 19.9 now retains full validated inputs and jump schedules; ten report cases and selected event traces pass. All 21 Chapter 19 files compiled and 11 scripts passed. [Input provenance follow-up](chapter-19-input-provenance-followup.md). COV-83 remains partially open. R2: adaptive RK4 policy now has selected exact-polynomial and callback-trace checks, including forced rejection and unchanged retry state/time; all nine intentional policy mutations were detected. [Adaptive follow-up](chapter-19-adaptive-policy-followup.md). COV-82 remains partially open; 21 chapter files compiled and 11 scripts passed. Next selected scope item: Section 14.9 covariance-eigenpair promise (COV-69).

## Disposition rules

1. Preserve each gap's original evidence and link the confirmed disposition. Do not silently rewrite a gap as a pass.
2. A missing exercise-specific assertion is not automatically a software bug; a general proof obligation is not resolved by finite random cases.
3. A restricted API may be valid if manuscript scope is explicit. Reconcile the contract before broadening it.
4. Retest affected code/fixtures when changed; repeat the full agreed release suite at the reviewed release revision.
5. Keep mapping completion, runtime execution, independent review and approval as separate tracker states.

G3 therefore remains **mapped; gaps open**, rather than a clean coverage gate. The [review checklist](remaining-review-checklist.md) and [progress tracker](PROGRESS.md) retain outstanding work.
