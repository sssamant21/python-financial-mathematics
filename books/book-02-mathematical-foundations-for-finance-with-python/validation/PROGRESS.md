# Book 02 — Validation Progress Tracker

**Updated:** 2026-10-27  
**Overall status:** In progress — automated runtime pass completed on a defined snapshot; coverage, independent review and final-revision validation remain pending.

This tracker records evidence and open work. A passed script is not a validated chapter, an independent review, or canonical approval. Update the evidence and revision whenever a status changes; do not treat a draft, missing result, or an unchecked item as a pass.

## Current evidence

| Workstream | Status | Progress / evidence |
|---|---|---|
| Numbered manuscript inventory | Initial inventory complete | 215/215 section files found across 21 chapters at revision `a20484672beae64e7c61037af0b11baba2fd7e54`; content completeness and index consistency not yet audited. |
| Python compilation | Initial pass complete | 427/427 files compiled in the follow-up local snapshot on Python 3.12.14/Linux. |
| Automated script execution | Initial pass complete; final-revision run pending | 216/216 check/test scripts exited zero on the original snapshot plus seven fixes. Counts are script runs, not coverage or independent tests; some checks invoke others. |
| Initial failures | Fixed and rerun locally; independent review pending | Six failed checks were addressed; the follow-up pass returned zero exits. Numerical and cross-platform review remains open. |
| Test coverage and dependencies | In progress | Filename mapping covers 215 sections. Focused [Chapter 21](chapter-21-capstone-review.md) and [Chapter 20](chapter-20-boundary-review.md) reviews identified fixes; broader substantive coverage and dependencies remain pending. [Inventory](section-check-inventory.md). |
| Mathematical and numerical review | Pending | Review derivations, examples, solutions, assumptions, error bounds and numerical edge cases, including the six fixes. |
| Links and index consistency | In progress | 2,004 inline relative link occurrences checked: zero missing paths at scan revision; stale index entries corrected. Anchors, external and reference-style links remain pending. [Audit report](link-index-audit.md). |
| Editorial, source and copyright review | Pending | Review manuscript quality, attribution and source policy. |
| Final-revision and platform validation | Pending | Rerun the agreed suite against the exact final commit; assess supported Python versions and Windows where applicable. |
| Canonical approval | Not granted | Requires documented review, resolved findings and the authorized decision. |

## Runtime evidence and scope

- [Initial inventory and failures](initial-runtime-inventory.md): 210/216 scripts passed initially.
- [Failure fixes and follow-up](runtime-failure-followup.md): 216/216 scripts exited successfully after targeted fixes. Changes published through `deac1e6b9d447322b71cdda751fb04197e497b57`; the local run used the original snapshot plus those changes and did not cover unrelated concurrent branch changes.
- Runtime environment: Python 3.12.14 on Linux; checks invoked from their own directories, with a 15-second timeout.
- Manuscript coverage and independent review are **not quantified** by the script counts.

## Chapter review register

Status reflects book-wide runtime script execution only, not an individual chapter certification. Set a review status only after recording scoped evidence and reviewer.

| Chapter | Numbered sections inventoried | Independent mathematical review | Editorial / source review | Chapter validation |
|---|---:|---|---|---|
| 01 | 15 | Pending | Pending | Not certified |
| 02 | 10 | Pending | Pending | Not certified |
| 03 | 10 | Pending | Pending | Not certified |
| 04 | 10 | Pending | Pending | Not certified |
| 05 | 10 | Pending | Pending | Not certified |
| 06 | 10 | Pending | Pending | Not certified |
| 07 | 10 | Pending | Pending | Not certified |
| 08 | 10 | Pending | Pending | Not certified |
| 09 | 10 | Pending | Pending | Not certified |
| 10 | 10 | Pending | Pending | Not certified |
| 11 | 10 | Pending | Pending | Not certified |
| 12 | 10 | Pending | Pending | Not certified |
| 13 | 10 | Pending | Pending | Not certified |
| 14 | 10 | Pending | Pending | Not certified |
| 15 | 10 | Pending | Pending | Not certified |
| 16 | 10 | Pending | Pending | Not certified |
| 17 | 10 | Pending | Pending | Not certified |
| 18 | 10 | Pending | Pending | Not certified |
| 19 | 10 | Pending | Pending | Not certified |
| 20 | 10 | Pending | Pending | Not certified |
| 21 | 10 | Pending | Pending | Not certified |

## Finding register

| ID | Area | Current state | Remaining evidence |
|---|---|---|---|
| V-01 | Chapter 08 derivative check | Fix applied; local script passed | Independent review of step size and numerical behavior |
| V-02 | Chapter 10 exception type | Fix applied; local script passed | Confirm interface and manuscript agree |
| V-03 | Chapter 11 angle computation | Fix applied; local script passed | Independent numerical and boundary review |
| V-04 | Chapter 16 descent stopping | Fix applied; local script passed | Review near-stationary behavior and convergence assumptions |
| V-05 | Chapter 18 summation demonstration | Fix applied; local script passed | Check manuscript wording and supported Python versions |
| V-06 | Chapter 20 tolerance comparison | Fix applied; local script passed | Review exact-float comparison semantics and performance |
| V-07 | Book indexes and links | In progress | Reconcile Section 4.7–4.8 title/scope differences; audit anchors, external and reference-style links. [Audit](link-index-audit.md) |
| V-08 | Coverage and executable examples | In progress | Filename mapping complete; focused Chapter 21 review and fixes recorded. Review remaining assertions, exercise coverage, dependencies and executable examples. [Inventory](section-check-inventory.md) · [Chapter 21 review](chapter-21-capstone-review.md) |
| V-10 | Chapter 21 numerical and report gaps | Fixes applied; independent review pending | Review small-rate transition, finite-difference overflow and scenario inputs; rerun final revision. [Evidence](chapter-21-capstone-review.md) |
| V-11 | Chapter 20 tiny-rate annuity underflow | Fix applied; independent review pending | Review extreme-rate numerical behavior and Section 20.6 input contract. [Evidence](chapter-20-boundary-review.md) |
| V-09 | Independent review and final release | Open | Record reviewer, scope, findings, final revision and authorized decision |

## Next actions

1. Resolve the Section 4.7–4.8 title/scope mismatch and complete remaining link checks.
2. Assess substantive coverage and dependencies; review assertions and validate manuscript examples using the section-to-check inventory.
3. Review the six fixes and mathematical examples independently, tracking findings and owners.
4. Rerun checks on the agreed final commit and supported environments; retain command, results and runtime details.
5. Complete editorial, source and copyright review before any canonical decision.

## Update rules

For each completed item record the date, exact commit or snapshot, environment, scope, command or review method, outcome, evidence link and unresolved findings. Reopen affected items when relevant source, requirements or dependencies change. Use **pending**, **in progress**, **passed**, **failed**, or **blocked** with a clear scope; a local automated pass does not mean the book is certified.
