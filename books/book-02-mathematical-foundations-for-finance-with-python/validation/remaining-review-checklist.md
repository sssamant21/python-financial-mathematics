# Book 02 — Remaining Review and Release Checklist

**Date:** 2026-10-28  
**Candidate source revision:** `2366ddd9ea146f841ad2822ffa5193bd637e4e9d`  
**Disposition:** Runtime evidence available; independent review and release approval pending.

## Reconciled evidence

The [full pinned runtime pass](pinned-revision-runtime-validation.md) covers 444 Python files and 233 script exits on Python 3.12.14/Linux. It includes the focused chapter fixes and clears the earlier unavailable-runtime blocker. Earlier reports remain historical records; their wording about an unexecuted final-revision run must be read alongside this newer candidate-revision result. A candidate pass is not final release acceptance.

V-01–V-06 and V-10–V-29 are implementation findings or focused review records, not independently closed mathematical findings. Their runtime component is covered by V-31 at the candidate revision; independent numerical review remains open. V-28 and V-30 required no implementation fix. V-07 (links/indexes), V-08 (coverage) and V-09 (independent review/release) remain open.

## Gate register

No reviewer is assigned by this document. “Unassigned” is an open ownership item, not evidence of a completed review.

| Gate | State | Required evidence to close | Owner |
|---|---|---|---|
| G1 Candidate compilation/runtime | Passed, scoped | V-31 report at pinned revision; reopen for affected source or fixture changes | Automated run recorded |
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
