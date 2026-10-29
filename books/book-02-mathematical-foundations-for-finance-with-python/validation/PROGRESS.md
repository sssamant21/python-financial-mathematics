# Book 02 — Validation Progress Tracker

**Updated:** 2026-10-28  
**Overall status:** In progress — full pinned-revision runtime pass complete (444 compiled files; 233 successful script exits); coverage, independent review and final release/platform validation remain pending.

This tracker records evidence and open work. A passed script is not a validated chapter, an independent review, or canonical approval. Update the evidence and revision whenever a status changes; do not treat a draft, missing result, or an unchecked item as a pass.

## Current evidence

| Workstream | Status | Progress / evidence |
|---|---|---|
| Numbered manuscript inventory | Initial inventory complete | 215/215 section files found across 21 chapters at revision `a20484672beae64e7c61037af0b11baba2fd7e54`; content completeness and index consistency not yet audited. |
| Python compilation | Pinned-revision pass complete | 444/444 files compiled at `2366ddd9ea146f841ad2822ffa5193bd637e4e9d` on Python 3.12.14/Linux. [Evidence](pinned-revision-runtime-validation.md). |
| Automated script execution | Pinned-revision pass complete | 233/233 check/test scripts exited zero at `2366ddd9ea146f841ad2822ffa5193bd637e4e9d`. Aggregate scripts repeat checks; counts do not measure independent coverage. [Evidence](pinned-revision-runtime-validation.md). |
| Initial failures | Fixed and rerun locally; independent review pending | Six failed checks were addressed; the follow-up pass returned zero exits. Numerical and cross-platform review remains open. |
| Test coverage and dependencies | In progress | Filename mapping covers 215 sections; substantive mapping covers 185/215 sections (all Chapters 1–18), with eighty-one recorded gap categories and no coverage certification. [4.1–4.6 map](coverage-sections-04-01-06.md) · [4.7–4.8 map](coverage-sections-04-07-08.md). Focused [Chapter 21](chapter-21-capstone-review.md), [Chapter 20](chapter-20-boundary-review.md) [Chapter 19](chapter-19-continuous-time-review.md) and [Chapter 18](chapter-18-solver-boundary-review.md) reviews identified fixes; broader substantive coverage and dependencies remain pending. [Inventory](section-check-inventory.md). |
| Mathematical and numerical review | Pending | Review derivations, examples, solutions, assumptions, error bounds and numerical edge cases, including the six fixes. |
| Links and index consistency | In progress — sampled rendered markup passed | Latest static scan: 270 Markdown files, 2,743 recognized local destinations, zero missing paths; no local fragment destinations or reference definitions detected. Rendered navigation, external scan checked 102 distinct URLs (99 HTTP 200, three 404); MathWorld corrected; Federal Reserve/NIST references subsequently resolved. [Source resolution](source-reference-resolution.md). Section 4.7–4.8 titles/scope reconciled. Six pinned GitHub pages retrieved; 14 rendered-markup navigation checks passed. Browser/visual and full-book navigation remain pending. [Rendered sample](rendered-navigation-sample-review.md). [External audit](external-url-audit.md). [Anchor/reference audit](anchor-reference-link-audit.md) · [Earlier index audit](link-index-audit.md). |
| Editorial, source and copyright review | Pending | Review manuscript quality, attribution and source policy. |
| Final-revision and platform validation | Candidate Linux pass complete; release/platform checks pending | Full candidate snapshot passed on Python 3.12.14/Linux; rerun after relevant review changes and assess supported Python versions and Windows. [Evidence](pinned-revision-runtime-validation.md). |
| Canonical approval | Not granted | Requires documented review, resolved findings and the authorized decision. |

## Runtime evidence and scope

- **Latest full run:** [Pinned revision runtime validation](pinned-revision-runtime-validation.md): 444/444 Python files compiled and 233/233 check/test scripts exited zero at `2366ddd9ea146f841ad2822ffa5193bd637e4e9d`; all 445 source/fixture blobs matched the pinned Git tree.

- [Initial inventory and failures](initial-runtime-inventory.md): 210/216 scripts passed initially.
- [Failure fixes and follow-up](runtime-failure-followup.md): 216/216 scripts exited successfully after targeted fixes. Changes published through `deac1e6b9d447322b71cdda751fb04197e497b57`; the local run used the original snapshot plus those changes and did not cover unrelated concurrent branch changes.
- Runtime environment: Python 3.12.14 on Linux; checks invoked from their own directories, with a 15-second timeout.
- Manuscript coverage and independent review are **not quantified** by the script counts.

## Chapter review register

Status reflects book-wide runtime script execution only, not an individual chapter certification. Set a review status only after recording scoped evidence and reviewer.

| Chapter | Numbered sections inventoried | Independent mathematical review | Editorial / source review | Chapter validation |
|---|---:|---|---|---|
| 01 | 15 | Pending | Pending | [Focused foundation review](chapter-01-foundation-boundary-review.md); 17/17 scripts passed, including aggregate reruns; not certified |
| 02 | 10 | Pending | Pending | [Focused quadratic review](chapter-02-quadratic-boundary-review.md); 11/11 scripts passed on recorded snapshot; not certified |
| 03 | 10 | Pending | Pending | [Focused exact-domain review](chapter-03-exact-domain-review.md); 11/11 scripts passed on recorded snapshot; not certified |
| 04 | 10 | Pending | Pending | [Focused growth review](chapter-04-growth-recovery-review.md); 11/11 scripts passed on recorded snapshot; not certified |
| 05 | 10 | Pending | Pending | [Focused recurrence review](chapter-05-recurrence-boundary-review.md); not certified |
| 06 | 10 | Pending | Pending | [Focused series review](chapter-06-series-boundary-review.md); not certified |
| 07 | 10 | Pending | Pending | [Focused limit review](chapter-07-limit-boundary-review.md); not certified |
| 08 | 10 | Pending | Pending | [Focused derivative review](chapter-08-difference-denominator-review.md); not certified |
| 09 | 10 | Pending | Pending | [Focused scenario review](chapter-09-scenario-revaluation-review.md); not certified |
| 10 | 10 | Pending | Pending | [Focused cash-flow review](chapter-10-cashflow-boundary-review.md); not certified |
| 11 | 10 | Pending | Pending | [Focused projection review](chapter-11-projection-coefficient-review.md); not certified |
| 12 | 10 | Pending | Pending | [Focused inverse review](chapter-12-inverse-scaling-review.md); not certified |
| 13 | 10 | Pending | Pending | [Focused projection review](chapter-13-projection-scaling-review.md); not certified |
| 14 | 10 | Pending | Pending | [Focused review](chapter-14-decomposition-boundary-review.md); not certified |
| 15 | 10 | Pending | Pending | [Focused review](chapter-15-derivative-boundary-review.md); not certified |
| 16 | 10 | Pending | Pending | [Focused review](chapter-16-stopping-review.md); not certified |
| 17 | 10 | Pending | Pending | [Focused review](chapter-17-feasibility-review.md); not certified |
| 18 | 10 | Pending | Pending | [Focused review](chapter-18-solver-boundary-review.md); not certified |
| 19 | 10 | Pending | Pending | [Focused review](chapter-19-continuous-time-review.md); not certified |
| 20 | 10 | Pending | Pending | [Focused review](chapter-20-boundary-review.md); not certified |
| 21 | 10 | Pending | Pending | [Focused review](chapter-21-capstone-review.md); not certified |

## Finding register

| ID | Area | Current state | Remaining evidence |
|---|---|---|---|
| V-01 | Chapter 08 derivative check | Fix applied; local script passed | Independent review of step size and numerical behavior |
| V-02 | Chapter 10 exception type | Fix applied; local script passed | Confirm interface and manuscript agree |
| V-03 | Chapter 11 angle computation | Fix applied; local script passed | Independent numerical and boundary review |
| V-04 | Chapter 16 descent stopping | Fix applied; local script passed | Review near-stationary behavior and convergence assumptions |
| V-05 | Chapter 18 summation demonstration | Fix applied; local script passed | Check manuscript wording and supported Python versions |
| V-06 | Chapter 20 tolerance comparison | Fix applied; local script passed | Review exact-float comparison semantics and performance |
| V-07 | Book indexes and links | In progress | Section 4.7–4.8 title/scope mismatch resolved. [Reconciliation](chapter-04-title-scope-reconciliation.md). Federal Reserve/NIST reference repair resolved in the [source-resolution report](source-reference-resolution.md); six-page rendered markup sample passed; browser/visual and full-book review pending. [Rendered sample](rendered-navigation-sample-review.md). [External audit](external-url-audit.md). Static scan detected no local fragments or reference definitions. [Latest audit](anchor-reference-link-audit.md) |
| V-08 | Coverage and executable examples | In progress | Filename mapping complete; substantive mapping covers Chapters 1–18, recording COV-01–COV-81. [Chapter 18 map](coverage-chapter-18.md). [Chapter 17 map](coverage-chapter-17.md). [Chapter 16 map](coverage-chapter-16.md). [Chapter 15 map](coverage-chapter-15.md). [Chapter 14 map](coverage-chapter-14.md). [Chapter 13 map](coverage-chapter-13.md). [Chapter 12 map](coverage-chapter-12.md). [Chapter 11 map](coverage-chapter-11.md). [Chapter 10 map](coverage-chapter-10.md). [Chapter 9 map](coverage-chapter-09.md). [Chapter 8 map](coverage-chapter-08.md). [Chapter 7 map](coverage-chapter-07.md). [Chapter 6 map](coverage-chapter-06.md). [Chapter 5 map](coverage-chapter-05.md). [Chapter 3 map](coverage-chapter-03.md). [Chapter 2 final slice](coverage-sections-02-06-10.md). [Chapter 2 slice](coverage-sections-02-01-05.md). [Final Chapter 1 slice](coverage-sections-01-11-15.md). [Latest slice](coverage-sections-01-06-10.md). [Chapter 1 slice](coverage-sections-01-01-05.md). [Project/assessment map](coverage-sections-04-09-10.md). [Six-section map](coverage-sections-04-01-06.md). [Coverage map](coverage-sections-04-07-08.md). Focused Chapter 21 review and fixes recorded. Review remaining assertions, exercise coverage, dependencies and executable examples. [Inventory](section-check-inventory.md) · [Chapter 21 review](chapter-21-capstone-review.md) |
| V-10 | Chapter 21 numerical and report gaps | Fixes applied; independent review pending | Review small-rate transition, finite-difference overflow and scenario inputs; rerun final revision. [Evidence](chapter-21-capstone-review.md) |
| V-11 | Chapter 20 tiny-rate annuity underflow | Fix applied; independent review pending | Review extreme-rate numerical behavior and Section 20.6 input contract. [Evidence](chapter-20-boundary-review.md) |
| V-12 | Chapter 19 continuous-time boundaries | Fixes applied; independent review pending | Section 19.8 near-zero discrete contributions fixed and checked; review event tolerances, numerical extremes and final-revision evidence. [Review](chapter-19-continuous-time-review.md) |
| V-13 | Chapter 18 solver boundaries | Fixes applied; independent review pending | Review solver stopping, numerical range, integration and final-revision evidence. [Review](chapter-18-solver-boundary-review.md) |
| V-14 | Chapter 17 cap feasibility | Fix applied; independent review pending | Assess near-boundary floating-point policy, KKT scaling and final-revision evidence. [Review](chapter-17-feasibility-review.md) |
| V-15 | Chapter 16 line-search stagnation | Fix applied; independent review pending | Review additional optimizer stagnation, Armijo arithmetic and final-revision evidence. [Review](chapter-16-stopping-review.md) |
| V-16 | Chapter 15 finite-difference boundaries | Fixes applied; independent review pending | Review perturbation asymmetry, covariance handling and final-revision evidence. [Review](chapter-15-derivative-boundary-review.md) |
| V-17 | Chapter 14 decomposition boundaries | Fixes applied; independent review pending | Review other norm calculations, matrix conditioning and final-revision evidence. [Review](chapter-14-decomposition-boundary-review.md) |
| V-18 | Chapter 13 projection scaling | Fix applied; independent review pending | Review large-target and coefficient range, QR screening and final-revision evidence. [Review](chapter-13-projection-scaling-review.md) |
| V-19 | Chapter 12 inverse scaling | Fixes applied; independent review pending | Review pivot scaling, residual normalizers and final-revision evidence. [Review](chapter-12-inverse-scaling-review.md) |
| V-20 | Chapter 11 projection coefficient | Fix applied; independent review pending | Review coefficient range, relative-distance scaling and final-revision evidence. [Review](chapter-11-projection-coefficient-review.md) |
| V-21 | Chapter 10 integral and sensitivity boundaries | Fixes applied; independent review pending | Review weighted integrals, quadrature spacing and final-revision evidence. [Review](chapter-10-cashflow-boundary-review.md) |
| V-22 | Chapter 9 scenario revaluation | Fix applied; independent review pending | Review Taylor bounds, elasticity range and final-revision evidence. [Review](chapter-09-scenario-revaluation-review.md) |
| V-23 | Chapter 8 derivative denominators | Fixes applied; independent review pending | Review remaining first-derivative guards, accuracy and final-revision evidence. [Review](chapter-08-difference-denominator-review.md) |
| V-24 | Chapter 7 limit and payment boundaries | Fixes applied; independent review pending | Review quotient range, approach tables and final-revision evidence. [Review](chapter-07-limit-boundary-review.md) |
| V-25 | Chapter 6 series boundaries | Fixes applied; independent review pending | Review extreme-rate annuities, formula independence and final-revision evidence. [Review](chapter-06-series-boundary-review.md) |
| V-26 | Chapter 5 recurrence cancellation | Fixes applied; independent review pending | Review rounding reconciliation, withdrawal timing and final-revision evidence. [Review](chapter-05-recurrence-boundary-review.md) |
| V-27 | Chapter 4 growth recovery | Fix applied; scoped runtime follow-up passed | 21/21 files compiled and 11/11 scripts passed at `94f7ad43cb5200826a97d3184691cd7d652849dd` on Python 3.12.14/Linux, including five new regression cases. Independent review and final-revision run pending. [Review](chapter-04-growth-recovery-review.md) |
| V-28 | Chapter 3 exact-domain boundaries | Focused review passed; no implementation change required | 20/20 files compiled and 11/11 scripts passed on baseline `695f393a6c14d37973bdd0644fc5a062df6f9af7` plus six new boundary cases. Independent manuscript review and final-revision run pending. [Review](chapter-03-exact-domain-review.md) |
| V-29 | Chapter 2 quadratic cancellation | Fix applied; scoped runtime follow-up passed | 20/20 files compiled; 11/11 scripts passed on recorded baseline plus fix and new regression. Independent review, Decimal range and final-revision validation pending. [Review](chapter-02-quadratic-boundary-review.md) |
| V-30 | Chapter 1 foundation boundaries | Focused review passed; no implementation change required | 32/32 files compiled; 17/17 scripts passed on recorded snapshot, with aggregate duplication. Five new unittest methods passed. Independent review and final-revision validation pending. [Review](chapter-01-foundation-boundary-review.md) |
| V-31 | Full pinned-revision runtime validation | Passed on Python 3.12.14/Linux | 444/444 files compiled; 233/233 scripts exited zero at `2366ddd9ea146f841ad2822ffa5193bd637e4e9d`. Independent review, supported platforms and final release reruns remain open. [Evidence](pinned-revision-runtime-validation.md) |
| V-09 | Independent review and final release | Open; review requirements documented | Eight gates and reviewer evidence requirements recorded in the [remaining review checklist](remaining-review-checklist.md). Reviewers are unassigned; no sign-off or canonical decision recorded. |

## Next actions

The [remaining review checklist](remaining-review-checklist.md) reconciles V-01–V-31 and defines eight evidence gates. The full pinned candidate runtime pass supersedes earlier runtime blockers; no independent review or release approval is inferred.

1. Expand substantive coverage mapping; retain browser/visual and full-book navigation review as pending. [Rendered markup sample](rendered-navigation-sample-review.md) passed 14 checks on six pages; Federal Reserve/NIST source-reference findings are [resolved](source-reference-resolution.md). [External audit](external-url-audit.md) records the 102-URL scan. [Section 4.7–4.8 title/scope reconciliation](chapter-04-title-scope-reconciliation.md) is recorded. [Static anchor/reference scan](anchor-reference-link-audit.md) found no local fragment destinations or reference definitions.
2. Continue substantive claims/example/exercise mapping with Chapter 19; Chapter 18 is [mapped](coverage-chapter-18.md); Chapter 17 is [mapped](coverage-chapter-17.md); Chapter 16 is [mapped](coverage-chapter-16.md); Chapter 15 is [mapped](coverage-chapter-15.md); Chapter 14 is [mapped](coverage-chapter-14.md); Chapter 13 is [mapped](coverage-chapter-13.md); Chapter 12 is [mapped](coverage-chapter-12.md); Chapter 11 is [mapped](coverage-chapter-11.md); Chapter 10 is [mapped](coverage-chapter-10.md); Chapter 9 is [mapped](coverage-chapter-09.md); Chapter 8 is [mapped](coverage-chapter-08.md); Chapter 7 is [mapped](coverage-chapter-07.md); Chapter 6 is [mapped](coverage-chapter-06.md); Chapter 5 is [mapped](coverage-chapter-05.md); all Chapter 3 sections are [mapped](coverage-chapter-03.md); all Chapter 2 sections are mapped, including [2.6–2.10](coverage-sections-02-06-10.md); Sections 2.1–2.5 are [mapped](coverage-sections-02-01-05.md); all Chapter 1 sections are mapped, including [1.11–1.15](coverage-sections-01-11-15.md); Sections 1.6–1.10 are [mapped](coverage-sections-01-06-10.md); Sections 1.1–1.5 are [mapped](coverage-sections-01-01-05.md); all ten Chapter 4 sections are mapped with open evidence gaps. [Project/assessment map](coverage-sections-04-09-10.md).
3. Review numerical fixes and manuscript material independently, recording reviewer and revision.
4. Declare and test supported environments; rerun the agreed suite against the reviewed release revision.
5. Complete editorial/source review and document the authorized canonical decision.


## Update rules

For each completed item record the date, exact commit or snapshot, environment, scope, command or review method, outcome, evidence link and unresolved findings. Reopen affected items when relevant source, requirements or dependencies change. Use **pending**, **in progress**, **passed**, **failed**, or **blocked** with a clear scope; a local automated pass does not mean the book is certified.
