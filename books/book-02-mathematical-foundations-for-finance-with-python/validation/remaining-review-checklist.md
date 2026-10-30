# Book 02 — Remaining Review and Release Checklist

**Date:** 2026-10-30  
**Candidate source revision:** `378775bc25034f5551f1d1efa51d836da77d6737`  
**Disposition:** Runtime evidence available; independent review and release approval pending.

## Reconciled evidence

[V-38 seventh refresh](runtime-refresh-2026-10-30-r2.md) covers the maturity/covariance changes: 464 files compiled, 253 scripts passed and 465 hashes verified before/after. Latest candidate execution; G2–G8 unchanged.

The [sixth full refresh](runtime-refresh-2026-10-30.md), V-37, covers both recent Chapter 14 integrations and the Chapter 15 Hessian/Jacobian/level-set additions: 461 compiled files, 250 successful scripts and 462 required hashes verified before/after. Historical candidate execution at that time; G2–G8 unchanged.

The [fifth full refresh](runtime-refresh-2026-10-29-r5.md), V-36, covers the four subsequent Chapter 14 checker additions and Section 14.1/14.2/14.5 corrections: 456 files compiled, 245 scripts passed and 457 source/fixture hashes verified before/after. This was the latest candidate execution at that time; G2–G8 unchanged.

The [fourth full refresh](runtime-refresh-2026-10-29-r4.md), V-35, includes all eight subsequent Chapter 13/14 checkers: 452 files compiled, 241 scripts exited zero and 453 required blobs verified before/after. This was the latest candidate execution at that time. G2–G8 remained unchanged.

The [third full refresh](runtime-refresh-2026-10-29-r3.md), V-34, includes the subsequent Chapter 8, 10 and 11 follow-ups: 444 Python files compiled, 233 scripts exited zero and 445 required source/fixture blobs verified before and after execution. This was the latest candidate execution at that time; independent review and release acceptance remain pending. Earlier records below are historical.

The [second full refresh](runtime-refresh-2026-10-29-r2.md), V-33, includes all code changes through the factor audit: 444 Python files compiled and 233 scripts exited zero; 445 required sources/fixture blobs verified. It superseded earlier runs at that time. Independent reviewers and release acceptance remain pending.


The [latest full refresh](runtime-refresh-2026-10-29.md), V-32, includes subsequent Chapter 12/14/15/19/21 changes: 444 sources compiled, 233 script exits zero and 467 downloaded blobs verified before/after execution. This superseded the earlier run below at that time; all independent-review and release gates remain open.


The [full pinned runtime pass](pinned-revision-runtime-validation.md) covers 444 Python files and 233 script exits on Python 3.12.14/Linux. It includes the focused chapter fixes and clears the earlier unavailable-runtime blocker. Earlier reports remain historical records; their wording about an unexecuted final-revision run must be read alongside this newer candidate-revision result. A candidate pass is not final release acceptance.

V-01–V-06 and V-10–V-29 are implementation findings or focused review records, not independently closed mathematical findings. Their runtime component is covered by V-31 at the candidate revision; independent numerical review remains open. V-28 and V-30 required no implementation fix. V-07 (links/indexes), V-08 (coverage) and V-09 (independent review/release) remain open.

## Gate register

No reviewer is assigned by this document. “Unassigned” is an open ownership item, not evidence of a completed review.

| Gate | State | Required evidence to close | Owner |
|---|---|---|---|
| G1 Candidate compilation/runtime | Passed, scoped | V-38 refresh at current pinned candidate; reopen for affected source or fixture changes | Automated run recorded |
| G2 Curriculum and navigation | In progress | Title/scope mismatch resolved in the [reconciliation](chapter-04-title-scope-reconciliation.md); complete rendered navigation/external checks and record exceptions | Unassigned |
| G3 Substantive coverage | Mapping complete; gaps open | All215 sections mapped in26 records; disposition COV-01–COV-90 and complete required manual review. [Index and queue](substantive-coverage-index.md) | Unassigned |
| G4 Independent mathematics/numerics | Pending | Named reviewer, revision, reviewed material, derivations, reference computations, findings and dispositions | Unassigned |
| G5 Editorial/source review | Pending | Named reviewer; notation, units, assumptions, attribution, source policy and exercise/solution consistency | Unassigned |
| G6 Supported environments | Pending | Declare supported Python versions/platforms; record actual clean-snapshot runs, including Windows if supported | Unassigned |
| G7 Release revision validation | Pending | Pin the reviewed release candidate; reconcile changes since G1, rerun affected/full agreed suite and retain results | Unassigned |
| G8 Canonical decision | Not granted | Authorized decision linked to resolved findings, accepted exceptions and exact release revision | Unassigned |

## Independent review sequence

Review the implementation changes and manuscript together. Do not infer mathematical validity from a zero script exit.

| Priority | Material | Questions and evidence |
|---|---|---|
| 1 | Original failures V-01–V-06 | Verify derivative step selection, exception contract, angle stability, descent stopping, summation behavior and exact-float tolerance semantics independently |
| 2 | Chapters 18–21, V-10–V-13 | Check solver stopping and range, event ordering/tolerances, near-zero account and annuity formulas, invariants, scenario/report completeness |
| 3 | Chapters 14–17, V-14–V-17 | Check feasibility at exact represented bounds, KKT scaling, Armijo stagnation, finite-difference representability, decomposition norms and conditioning |
| 4 | Chapters 10–13, V-18–V-21 | Check projection/inverse scaling, coefficient range, weighted integrals, cash-flow timing and sensitivity references |
| 5 | Chapters 5–9, V-22–V-26 | Check scenario revaluation, derivative denominators, limiting formulas, extreme-rate series, recurrence rounding reconciliation and withdrawal timing |
| 6 | Chapters 1–4, V-27–V-30 | Check growth recovery domain, rational inverse domains, quadratic cancellation and Decimal range, exact/float contracts and batch status semantics |
| 7 | All 215 numbered sections | Review remaining derivations, worked solutions, model assumptions and substantive coverage beyond the focused findings |

## Review record template

For each review item record:

- Finding/gate ID and chapter/section.
- Exact source revision and relevant paths.
- Reviewer name/role and relationship to the author or implementation work.
- Method: derivation, independently implemented reference, manual example calculation or executable assertion.
- Inputs, expected result, actual result and numerical tolerance rationale where applicable.
- Outcome: passed, failed, pending or blocked; link evidence and list limitations.
- Required correction, responsible owner and disposition; exact correction revision if changed.
- Rerun/re-review evidence and the person authorized to accept an exception.

A second pass by the same assistant is a further source review, not automatically an independent reviewer sign-off.

## Immediate executable queue

1. Static anchor/reference scanning and sampled rendered markup are recorded; complete full-book/browser/visual navigation and reassess external links for the release revision.
2. Sections 4.7–4.8 title/scope reconciliation is [recorded](chapter-04-title-scope-reconciliation.md); preserve established TOC titles during further review.
3. All215 sections now have substantive claims-to-evidence maps. Execute the [remediation queue](substantive-coverage-index.md), confirming numerical issues and reconciling report/lab scope; keep unresolved manual review obligations open.
4. Gather the original six fixes into a review packet and document independent numerical findings.
5. Define the supported environment matrix before calling G6 complete.

External reviews and approval are not claimed, and no review requests have been sent.

## Unequal-spectrum correction — 2026-10-29

[Section 14.1 evidence](chapter-14-unequal-spectrum-followup.md) records a confirmed representable-small-eigenvalue cancellation defect, its original regression failure and corrected exact/Decimal references. All 25 Chapter 14 files compiled and 15 scripts passed. This source change follows V-35; a new full-book run is not claimed. COV-68 remains partially open and twenty-five categories remain partially addressed. Next executable item: Section 14.2 duplicate spectral path against the unequal-spectrum references; independent review/platform/release gates remain pending.

## Spectral-report integration and correction — 2026-10-29

[Section 14.2 evidence](chapter-14-spectral-report-followup.md) confirms the shared Section 14.1 solver path and corrects one-shot input reuse and squared-norm underflow. The original checker failure and tiny-error probe are retained; all 26 chapter files compiled and 16 scripts passed after correction. This scoped change follows V-35. Twenty-five categories remain partially addressed. Next executable item: Section 14.1 off-diagonal averaging/symmetry boundary; broader numerical, platform and independent-review gates remain open.

## Symmetry-policy boundary follow-up — 2026-10-29

[Chapter 14 evidence](chapter-14-symmetry-policy-followup.md) adds nine adjacent represented-threshold cases, exact-versus-tolerant symmetry contrast and three subnormal midpoint cases. No implementation change was justified; the manuscript now states the policies and absolute floor. All 27 chapter files compiled and 17 scripts passed. This checker addition follows V-35; twenty-five categories remain partially addressed. Next executable item: Section 14.5 tiny nondyadic reconstruction norms, then full-book runtime refresh after related fixes. Independent review, environment and release gates remain pending.

## Tiny Cholesky diagnostic correction and V-36 — 2026-10-29

[Correction evidence](chapter-14-cholesky-norm-followup.md) retains an original zero-error underflow failure and five Decimal norm/solve-report cases; all 28 Chapter 14 files compiled and 18 scripts passed. [V-36 full execution](runtime-refresh-2026-10-29-r5.md) subsequently compiled 456 sources and passed 245 scripts with 457 verified blobs at `82ec4d155b0b370008fab16f42a9781b7c4cd322`, covering all four recent checker additions and spectral/Cholesky corrections. Twenty-five categories remain partially addressed; independent review and release gates stay open. Next executable item: COV-67 Section 14.8/14.10 literal-report versus computed-factor integration and meaningful fault detection.

## Computed diagnostic integration follow-up — 2026-10-29

[Section 14.8 evidence](chapter-14-diagnostic-integration-followup.md) replaces literal-factor diagnostics with actual helper calls and independently recomputed errors. Four calls are observed and five wrong outputs detected; all 29 chapter files compiled and 19 scripts passed. This source/checker change follows V-36; G1's full-book evidence is historical for the changed source. Twenty-five categories remain partially addressed. Next executable item: Section 14.10 reference-report integration under COV-67. Independent review, environment and release gates remain pending.

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
