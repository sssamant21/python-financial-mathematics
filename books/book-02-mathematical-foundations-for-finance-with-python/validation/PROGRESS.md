# Book 02 — Validation Progress Tracker

**Updated:** 2026-11-07  
**Overall status:** In progress — V-112 full candidate Linux pass (578 files, 365 scripts, 579 required hashes), including Section 8.5 exponential-derivative scaling. Independent review, supported platforms and release approval remain pending.

This tracker records evidence and open work. A passed script is not a validated chapter, an independent review, or canonical approval. Update the evidence and revision whenever a status changes; do not treat a draft, missing result, or an unchecked item as a pass.

## Current evidence

| Workstream | Status | Progress / evidence |
|---|---|---|
| Numbered manuscript inventory | Initial inventory complete | 215/215 section files found across 21 chapters at revision `a20484672beae64e7c61037af0b11baba2fd7e54`; content completeness and index consistency not yet audited. |
| Python compilation | Full candidate Linux pass | 578/578 at `8a23628022d832fbd80422aaf6ca582b28917de6`. [V-112](runtime-refresh-2026-11-07-r18.md). |
| Automated script execution | Full candidate Linux pass | 365/365 at `8a23628022d832fbd80422aaf6ca582b28917de6`; 579 required blobs verified before/after. [V-112](runtime-refresh-2026-11-07-r18.md). |
| Initial failures | Fixed and rerun locally; independent review pending | Six failed checks were addressed; the follow-up pass returned zero exits. Numerical and cross-platform review remains open. |
| Test coverage and dependencies | Mapping complete; gaps open | Filename mapping covers 215 sections; substantive mapping covers 215/215 sections (all Chapters 1–21), with ninety recorded gap categories and no coverage certification. [4.1–4.6 map](coverage-sections-04-01-06.md) · [4.7–4.8 map](coverage-sections-04-07-08.md). Focused [Chapter 21](chapter-21-capstone-review.md), [Chapter 20](chapter-20-boundary-review.md) [Chapter 19](chapter-19-continuous-time-review.md) and [Chapter 18](chapter-18-solver-boundary-review.md) reviews identified fixes; gap remediation and dependency review remain pending. [All-section coverage index](substantive-coverage-index.md). [Inventory](section-check-inventory.md). |
| Mathematical and numerical review | Pending | Review derivations, examples, solutions, assumptions, error bounds and numerical edge cases, including the six fixes. |
| Links and index consistency | In progress — sampled rendered markup passed | Latest static scan: 270 Markdown files, 2,743 recognized local destinations, zero missing paths; no local fragment destinations or reference definitions detected. Rendered navigation, external scan checked 102 distinct URLs (99 HTTP 200, three 404); MathWorld corrected; Federal Reserve/NIST references subsequently resolved. [Source resolution](source-reference-resolution.md). Section 4.7–4.8 titles/scope reconciled. Six pinned GitHub pages retrieved; 14 rendered-markup navigation checks passed. Browser/visual and full-book navigation remain pending. [Rendered sample](rendered-navigation-sample-review.md). [External audit](external-url-audit.md). [Anchor/reference audit](anchor-reference-link-audit.md) · [Earlier index audit](link-index-audit.md). |
| Editorial, source and copyright review | Pending | Review manuscript quality, attribution and source policy. |
| Final-revision and platform validation | Candidate Linux pass complete; release/platform checks pending | Full candidate snapshot passed on Python 3.12.14/Linux; rerun after relevant review changes and assess supported Python versions and Windows. [Evidence](pinned-revision-runtime-validation.md). |
| Canonical approval | Not granted | Requires documented review, resolved findings and the authorized decision. |

## Earlier full-book runtime refresh — V-39

467/467 sources compiled; 256/256 scripts exited zero; 468/468 required hashes matched before/after at `18be350b40cc2a0a963e0c5fd91b793cf0c3c634`. Includes three Chapter 16 optimizer reference checkers. [Report](runtime-refresh-2026-10-30-r3.md) · [Raw evidence](runtime-refresh-2026-10-30-r3.json). Twenty-eight categories remain partially addressed; independent review/release gates stay open.

## Earlier scoped multistart reference follow-up

Four selected starts now have independent stationary-cubic root/objective references and real failed/mixed pool checks. A stationary local maximum demonstrates status limits. All 22 Chapter 16 files compiled and 12 scripts passed; implementation unchanged. [Evidence](chapter-16-multistart-reference-followup.md). COV-73/75 partially open; follows V-38.

## Earlier scoped optimizer-status follow-up

Selected Section 16.5/16.7 Armijo/status obligations now have exact rational sufficient-decrease references and real failure-path checks. All 21 Chapter 16 files compiled and 11 scripts passed; implementation unchanged. [Evidence](chapter-16-optimizer-status-followup.md). COV-73 partially open; follows V-38.

## Earlier full-book runtime refresh — V-38

464/464 sources compiled; 253/253 scripts exited zero; 465/465 required hashes matched before/after at `378775bc25034f5551f1d1efa51d836da77d6737`. Includes all recent maturity/covariance changes and three checkers. [Report](runtime-refresh-2026-10-30-r2.md) · [Raw evidence](runtime-refresh-2026-10-30-r2.json). G1 refreshed; independent review/release gates remain pending.

## Earlier scoped covariance consistency correction

Sections 15.4/15.6 now share symmetric covariance normalization and finite determinant screening, correcting inconsistent accepted-input gradients/Hessians. All 26 Chapter 15 files compiled and 16 scripts passed. [Evidence](chapter-15-covariance-consistency-followup.md). This follows V-37; COV-72 remains partially open.

## Earlier scoped adjusted-maturity correction

Section 15.8 now avoids intermediate numerator range loss and rejects nonfinite shocked rates/unrepresentable final maturities. Eight Decimal references and five rejection cases pass; all 25 Chapter 15 files compiled and 15 scripts passed. [Evidence](chapter-15-maturity-range-followup.md). This follows V-37; COV-72 remains partially open.

## Earlier full-book runtime refresh — V-37

461/461 sources compiled; 250/250 scripts exited zero; 462/462 source/fixture hashes matched before/after at `28af429b7695520536cf4a3384af1318614e31aa`. Includes both recent Chapter 14 integrations and all three Chapter 15 accuracy/boundary checkers. [Report](runtime-refresh-2026-10-30.md) · [Raw outputs](runtime-refresh-2026-10-30.json). G1 refreshed; twenty-six categories partially addressed; independent review and release gates remain open.

## Earlier scoped float-Jacobian accuracy follow-up

Section 15.9's actual centered columns now have independent Decimal quotient references, selected convergence ladders and cancellation/asymmetry cases. All 23 Chapter 15 files compiled and 13 scripts passed; implementation unchanged. [Evidence](chapter-15-jacobian-accuracy-followup.md). COV-71 partially open; follows V-36.

## Earlier scoped Hessian accuracy follow-up

Selected analytic Hessians now have independent 90-digit valuation-stencil references and step ladders. All 22 Chapter 15 files compiled and 12 scripts passed; implementation unchanged. [Evidence](chapter-15-hessian-accuracy-followup.md). COV-71 remains partially open; this follows V-36.

## Earlier scoped final-assessment integration

Section 14.10 now uses actual eigen/Cholesky/SVD/compression outputs. Four helper calls and five injected wrong outputs are checked; all 30 Chapter 14 files compiled and 20 scripts passed. [Evidence](chapter-14-final-integration-followup.md). This follows V-36; COV-67 remains partially open.

## Earlier scoped diagnostic integration follow-up

Section 14.8 now computes diagnostics from actual helper outputs; four helper calls and five injected wrong outputs are checked. All 29 Chapter 14 files compiled and 19 scripts passed. [Evidence](chapter-14-diagnostic-integration-followup.md). This follows V-36; COV-67 remains partially open.

## Earlier full-book runtime refresh — V-36

456/456 Python files compiled; 245/245 scripts exited zero; 457/457 source/fixture blobs matched before/after. Includes the Section 14.1/14.2/14.5 corrections and four new checkers after V-35. [Report](runtime-refresh-2026-10-29-r5.md) · [Raw results](runtime-refresh-2026-10-29-r5.json). All 28 Chapter 14 files compiled and 18 scripts also passed in the scoped run; [latest correction](chapter-14-cholesky-norm-followup.md).

## Earlier scoped symmetry-policy follow-up

Nine adjacent symmetry cases and three subnormal midpoint cases now document eigen/decomposition tolerance versus exact Cholesky symmetry. Implementation unchanged; all 27 Chapter 14 files compiled and 17 scripts passed. [Evidence](chapter-14-symmetry-policy-followup.md). COV-68 partially open; follows V-35.

## Earlier scoped spectral-report correction

Section 14.2 now preserves one-shot matrix inputs and avoids underflow in tiny reconstruction norms. Shared Section 14.1 small-root integration is checked. All 26 Chapter 14 files compiled and 16 scripts passed. [Evidence](chapter-14-spectral-report-followup.md). COV-68 remains partially open; this follows V-35.

## Earlier scoped unequal-spectrum correction

Section 14.1 no longer loses selected representable small eigenvalues to trace-gap cancellation. The original source fails the retained regression; corrected 24 exact diagonal and six Decimal cases pass. All 25 Chapter 14 files compiled and 15 scripts passed. [Evidence](chapter-14-unequal-spectrum-followup.md). This follows V-35; COV-68 remains partially open.

## Earlier full-book runtime refresh — V-35

452/452 Python files compiled, 241/241 check/test scripts exited zero and 453/453 source/fixture blobs matched the pinned tree before and after execution. Includes all eight Chapter 13/14 checker additions. [Report](runtime-refresh-2026-10-29-r4.md) · [Raw evidence](runtime-refresh-2026-10-29-r4.json). G1 refreshed; independent review and release gates remain pending.

## Earlier scoped SVD ordering follow-up

Section 14.6 now checks twelve restricted factor-order reconstruction and threshold cases. All 24 Chapter 14 files compiled and 14 scripts passed. [Evidence](chapter-14-svd-order-followup.md). COV-67 partially open; implementation unchanged and follows V-34.

## Earlier scoped near-SPD Cholesky follow-up

Section 14.5 now checks nine selected near-SPD factorizations/solves and six non-SPD boundary matrices. All 23 Chapter 14 files compiled and 13 scripts passed. [Evidence](chapter-14-near-spd-followup.md). COV-68 partially open; implementation unchanged and follows V-34.

## Earlier scoped near-repeated spectral follow-up

Section 14.1 now checks twelve selected repeated/near-repeated cases at three scales. All 22 Chapter 14 files compiled and 12 scripts passed. [Evidence](chapter-14-near-repeated-followup.md). COV-68 partially open; implementation unchanged and follows V-34.

## Earlier scoped null-basis follow-up

Section 13.3 now checks 72 selected rank/nullity, exact null-vector and independence cases. All 26 Chapter 13 files compiled and 16 scripts passed. [Evidence](chapter-13-null-basis-followup.md). COV-64 partially open; follows V-34.

## Earlier scoped basis-span follow-up

Section 13.2 now checks exact basis-span reconstruction across six column orders and three scales. All 25 Chapter 13 files compiled and 15 scripts passed. [Evidence](chapter-13-basis-span-followup.md). COV-64 remains partially open; follows V-34.

## Earlier scoped project-contract follow-up

Section 13.9 now has direct selected invalid-input and report/serialization checks. All 24 Chapter 13 files compiled and 14 scripts passed. [Evidence](chapter-13-project-contract-followup.md). COV-66 partially open; implementation unchanged and follows V-34.

## Earlier scoped ridge optimality follow-up

Section 13.8 now has exact rational objective and nonoptimal-comparison checks plus a selected positive-strength limit sequence. All 23 Chapter 13 files compiled and 13 scripts passed. [Evidence](chapter-13-ridge-optimality-followup.md). COV-65 partially open; implementation unchanged and this follows V-34.

## Earlier scoped QR rank-screen follow-up

Section 13.6 now has selected threshold/scale and column-order reference checks. All 22 Chapter 13 files compiled and 12 scripts passed. [Evidence](chapter-13-qr-rank-followup.md). COV-64 partially open; follows V-34.

## Earlier full-book runtime refresh

V-34: 444/444 Python files compiled; 233/233 scripts exited zero; 445/445 required source/fixture blobs matched the pinned tree before and after execution. This third full refresh includes the recent Chapter 8, 10 and 11 follow-ups. [Report and raw evidence](runtime-refresh-2026-10-29-r3.md). Independent review and release gates remain pending.

## Earlier scoped final-assessment follow-up

Section 11.10 now directly tests nonfinite financial records/NAVs, selected arithmetic-overflow rejection and strict JSON output. All 21 Chapter 11 files compiled and 11 scripts passed; implementation unchanged. [Evidence](chapter-11-final-nonfinite-followup.md). COV-60 remains partially open; this follows the full-book run.

## Earlier scoped budget-boundary follow-up

Section 11.7 now checks an isolated budget breach and selected exact/adjacent constraint boundaries; an omitted-budget variant was detected. All 21 Chapter 11 files compiled and 11 scripts passed; implementation unchanged. [Evidence](chapter-11-budget-boundary-followup.md). COV-59 remains partially open; this follows the full-book run.

## Earlier scoped policy-audit follow-up

Section 11.9 now retains configured policy limits/allowances and tests isolated threshold breaches. All 21 Chapter 11 files compiled and 11 scripts passed; decision rules unchanged. [Evidence](chapter-11-policy-audit-followup.md). COV-59 remains partially open; this follows the full-book run.

## Earlier scoped relative-distance follow-up

Section 11.4 now has independent three-norm/asymmetric-denominator and zero/subnormal/range checks; a wrong-denominator variant was detected. All 21 Chapter 11 files compiled and 11 scripts passed; implementation unchanged. [Evidence](chapter-11-relative-distance-followup.md). COV-60 remains partially open; this follows the full-book run.

## Earlier scoped projection follow-up

Section 11.6 now reports residual norms and checks scalar/projection/reconstruction diagnostics against rational references across twenty selected cases. All 21 Chapter 11 files compiled and 11 scripts passed. [Evidence](chapter-11-projection-audit-followup.md). COV-60 remains partially open; this follows the full-book run.

## Earlier scoped normalized-sensitivity follow-up

Section 8.8 now rejects zero normalization prices and nonfinite sensitivity reports; independent stencil ratios pass at three cash-flow scales. All 21 Chapter 8 files compiled and 11 scripts passed. [Evidence](chapter-08-sensitivity-range-followup.md). This extends partial COV-51 remediation and follows the recorded full-book run.

## Earlier scoped helper follow-up

Section 8.8 now rejects nonfinite derivative estimates and avoids Richardson intermediate overflow. Selected perturbation/callback/denominator guards pass; all 21 Chapter 8 files compiled and 11 scripts passed. [Evidence](chapter-08-helper-guards-followup.md). COV-51 remains partially open; this follows the full-book run.

## Earlier scoped comparator follow-up

Section 8.9 now retains tolerance metadata, checks exact error fields/boundaries and rejects nonfinite estimates/errors that could falsely pass. All 21 Chapter 8 files compiled and 11 scripts passed. [Evidence](chapter-08-comparator-audit-followup.md). COV-50 remains partially open; this follows the full-book run.

## Earlier scoped derivative follow-up

Section 8.6 now checks exact polynomial second-difference errors/orders and a representable-step cancellation example; two faulty formulas were detected. All 21 Chapter 8 files compiled and 11 scripts passed; algorithm unchanged. [Evidence](chapter-08-difference-order-followup.md). COV-49 remains partially open; this follows the full-book run.

## Earlier scoped quadrature follow-up

Section 10.7 now checks exact signed polynomial errors, convergence ratios and fine estimators, plus selected exponential ratios; three faulty estimator variants were detected. All 21 Chapter 10 sources compiled and 11 scripts passed; algorithm unchanged. [Evidence](chapter-10-quadrature-order-followup.md). COV-55 remains partially open; this checker change follows the full-book run below.

## Historical full runtime refresh — second pass

All 444 Python files compiled and 233 check/test scripts exited zero at `7ee99f60d5089510f860a0b6f695f971beb2eac6`; all 445 required source/fixture blobs matched the pinned tree. [Historical report](runtime-refresh-2026-10-29-r2.md) · [Manifest and raw outputs](runtime-refresh-2026-10-29-r2.json). This includes all subsequent scoped code changes through the Chapter 12 factor audit. Fourteen COV categories remain partially addressed; independent review and release gates remain open.

## Earlier factor-audit follow-up

Section 12.9 now retains aligned factor limits; controlled factor rejection and exact/adjacent limit cases verify reported decisions and residuals. Constructor/unit/shape/guardrail cases pass; 21 Chapter 12 files compiled and 11 scripts passed. [Factor audit evidence](chapter-12-factor-audit-followup.md). COV-62 remains partially open; this follows the full-book run.

## Earlier final-allocation follow-up

Section 17.10 now reports/checks its second-cap multiplier and rejects missing multipliers/nonoptimal candidates. A rounded-cap-sum empty-interval defect is fixed. All 20 Chapter 17 files compiled and 10 scripts passed. [Final allocation evidence](chapter-17-final-allocation-followup.md). COV-78 remains partially open; this follows the full-book run.

## Earlier financial-range follow-up

Section 17.9 now guards trade/notional range and avoids intermediate transaction-cost overflow, with direct weight-based turnover. Extreme/subnormal/zero/true-overflow cases pass; 20 Chapter 17 files compiled and 10 scripts passed. [Financial-range evidence](chapter-17-financial-range-followup.md). COV-77 remains partially open; this follows the full-book run.

## Earlier KKT follow-up

Section 17.9 now has independent KKT residual/objective checks across four regimes and four isolated rejection families; four incomplete acceptance variants were detected. All 20 Chapter 17 files compiled and 10 scripts passed; optimizer unchanged. [KKT evidence](chapter-17-kkt-rejection-followup.md). COV-76 remains partially open; this checker change follows the full-book run.

## Earlier bracket-audit follow-up

Section 18.8's bracket flag now uses cached endpoint signs and interval history; endpoint residuals are reported. Independent reevaluation and callback counts cover seven solver paths. All 21 Chapter 18 files compiled and 11 scripts passed. [Bracket audit evidence](chapter-18-bracket-audit-followup.md). COV-79 remains partially open; this follows the full-book run below.

## Earlier Section 20.6 contract follow-up

Section 20.6 now rejects booleans/invalid numeric inputs, checks exponent/PV range and validates rates for empty portfolios. All 19 Chapter 20 sources compiled and 10 scripts passed, including 19 Section 20.6 methods. [Contract evidence](chapter-20-metamorphic-contract-followup.md). Underflow remains permitted and documented; COV-87 remains partially open. This code change follows the recorded full-book run.

## Earlier error-range follow-up — 2026-10-29

Section 20.5 now raises explicit OverflowError for unrepresentable absolute/relative error magnitudes, preserving exact tolerance comparison. All 19 Chapter 20 files compiled and 10 scripts passed, including 20 tolerance methods. [Error-range evidence](chapter-20-error-range-followup.md). COV-87 remains partially open; this follows the full run below.

## Earlier candidate-acceptance follow-up — 2026-10-29

Section 16.9 now recomputes training/holdout metrics and normalized loss/gradient per iterative candidate before acceptance. Independent rational references and selected rejection cases pass; 20 Chapter 16 files compiled and all 10 scripts passed. [Acceptance evidence](chapter-16-candidate-acceptance-followup.md). COV-74 remains partially open; this change follows the latest full run below.

## Earlier compression follow-up — 2026-10-29

Section 14.9 now calculates exposure loss from actual returned compression matrices and reports the spectral bound plus fixed-input/unit metadata. Twelve matrix/rank cases check 48 selected actions and attaining coordinate directions; 21 files compiled and all 11 chapter scripts passed. [Compression evidence](chapter-14-compression-bound-followup.md). This code change follows the full run below; COV-69 remains partially open for independent review and broader scope.

## Historical first full runtime refresh — 2026-10-29

All 444 Python files compiled and all 233 check/test scripts exited zero at `37aac57a72303a6d4178790f8d172495e2bc0ada`. All 467 downloaded Python/JSON blobs matched the pinned tree before and after execution. [Full evidence](runtime-refresh-2026-10-29.md) · [Manifest/outcomes](runtime-refresh-2026-10-29.json). This includes the recent Chapter 12/14/15/19/21 remediations and Section 21.9's 18 integration methods. Coverage gaps, independent review, platform support and approval remain open.

## Earlier covariance remediation — 2026-10-29

Section 14.9 now reports its promised covariance eigenpairs, checked against closed-form roots, spectral projectors and directly recomputed residual/reconstruction/orthogonality results. Four corrupted reports were detected; 21 Chapter 14 files compiled and all 11 scripts passed. [Scoped covariance evidence](chapter-14-covariance-eigenpair-followup.md). COV-69 remains partially open for compression-bound/report-metadata and independent review.

## Earlier adaptive remediation — 2026-10-29

Section 19.6 adaptive RK4 now has exact-polynomial and observed-stage checks for estimator/scaling, rejection preservation, retry acceptance and controller limits. Nine intentional policy errors were detected; no solver change was needed. All 21 Chapter 19 files compiled and 11 scripts passed, with the final checker recompiled/rerun after refining its zero-error case. [Scoped adaptive evidence](chapter-19-adaptive-policy-followup.md). COV-82 remains partially open for broader numerical behavior and independent review.

## Earlier event-report remediation — 2026-10-29

Section 19.9 now retains validated scenario inputs and complete jump schedules, with model/event policies. Ten report-contract cases and selected negative-jump/adjacent-time traces pass; 21 Chapter 19 files compiled and all 11 check scripts passed, plus successful CLI JSON parsing. [Scoped evidence](chapter-19-input-provenance-followup.md). COV-83 remains partially open for broader event numerics and independent review.

## Earlier Taylor remediation — 2026-10-29

Section 15.9 now checks full second-order contractions against a Decimal path-series reference for nine shocks and reports signed/absolute portfolio errors. All 21 Chapter 15 files compiled and 11 scripts passed; three incorrect contraction variants were detected. [Scoped Taylor evidence](chapter-15-taylor-oracle-followup.md). COV-70 remains partially open for final-assessment/shared-dependency and independent review.

## Earlier rank remediation — 2026-10-29

Section 12.5 target-dependent coefficient-rank defect fixed; column-equilibration policy disclosed in code and manuscript. All 21 Chapter 12 files compiled and 11 check scripts passed, including 21 new rank-policy outcomes. [Scoped evidence](chapter-12-rank-target-scaling-followup.md). COV-61 remains partially open; independent review pending.

## Earlier remediation

Section 15.2 finite-difference guard fix published; 21 Chapter 15 files compiled and all 11 check scripts passed, including nine boundary methods. [Scoped follow-up](chapter-15-scalar-difference-followup.md). This partially addresses COV-71/V-16; independent review and remaining numerical-accuracy work are pending. The historical full-book run below is unchanged.

## Runtime evidence and scope

- **Latest full run:** [V-67](runtime-refresh-2026-11-05-r9.md):519 compiled,308 passed,520 hashes matched before/after at `175c27e55a4eb0d48011937661f3295363d2c890`; project adapter/checker changed subsequently.

- **Historical seventh refresh:** [V-38 seventh refresh](runtime-refresh-2026-10-30-r2.md): 464 compiled sources, 253 successful scripts and 465 required hashes verified before/after at `378775bc25034f5551f1d1efa51d836da77d6737`.

- **Historical sixth refresh:** [V-37 sixth refresh](runtime-refresh-2026-10-30.md): 461 sources compiled and 250 scripts passed at `28af429b7695520536cf4a3384af1318614e31aa`; 462 hashes verified before/after.

- **Historical fifth refresh:** [V-36 fifth refresh](runtime-refresh-2026-10-29-r5.md): 456 files compiled; 245 scripts passed at `82ec4d155b0b370008fab16f42a9781b7c4cd322`; 457 required blobs verified before/after.

- **Historical fourth refresh:** [Fourth refresh](runtime-refresh-2026-10-29-r4.md): 452 sources compiled and 241 scripts passed at `3e185649bf53f5a72ad9e1869d17762110444a26`; 453 required blobs verified before/after.

- **Historical second refresh:** [V-33](runtime-refresh-2026-10-29-r2.md): 444 sources compiled and 233 scripts passed at `7ee99f60d5089510f860a0b6f695f971beb2eac6`; 445 required blobs verified.

- **Previous full run:** [2026-10-29 refresh](runtime-refresh-2026-10-29.md): 444/444 files compiled and 233/233 scripts exited zero at `37aac57a72303a6d4178790f8d172495e2bc0ada`; 467 blobs verified before/after execution.

- **Earlier full run:** [Pinned revision runtime validation](pinned-revision-runtime-validation.md): 444/444 Python files compiled and 233/233 check/test scripts exited zero at `2366ddd9ea146f841ad2822ffa5193bd637e4e9d`; all 445 source/fixture blobs matched the pinned Git tree.

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
| V-08 | Coverage and executable examples | In progress | Filename mapping complete; substantive mapping covers all 215 sections, recording COV-01–COV-90. [Consolidated index and remediation queue](substantive-coverage-index.md). [Chapter 21 map](coverage-chapter-21.md). [Chapter 20 map](coverage-chapter-20.md). [Chapter 19 map](coverage-chapter-19.md). [Chapter 18 map](coverage-chapter-18.md). [Chapter 17 map](coverage-chapter-17.md). [Chapter 16 map](coverage-chapter-16.md). [Chapter 15 map](coverage-chapter-15.md). [Chapter 14 map](coverage-chapter-14.md). [Chapter 13 map](coverage-chapter-13.md). [Chapter 12 map](coverage-chapter-12.md). [Chapter 11 map](coverage-chapter-11.md). [Chapter 10 map](coverage-chapter-10.md). [Chapter 9 map](coverage-chapter-09.md). [Chapter 8 map](coverage-chapter-08.md). [Chapter 7 map](coverage-chapter-07.md). [Chapter 6 map](coverage-chapter-06.md). [Chapter 5 map](coverage-chapter-05.md). [Chapter 3 map](coverage-chapter-03.md). [Chapter 2 final slice](coverage-sections-02-06-10.md). [Chapter 2 slice](coverage-sections-02-01-05.md). [Final Chapter 1 slice](coverage-sections-01-11-15.md). [Latest slice](coverage-sections-01-06-10.md). [Chapter 1 slice](coverage-sections-01-01-05.md). [Project/assessment map](coverage-sections-04-09-10.md). [Six-section map](coverage-sections-04-01-06.md). [Coverage map](coverage-sections-04-07-08.md). Focused Chapter 21 review and fixes recorded. Review remaining assertions, exercise coverage, dependencies and executable examples. [Inventory](section-check-inventory.md) · [Chapter 21 review](chapter-21-capstone-review.md) |
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
| V-32 | Full runtime refresh after gap remediation | Passed on Python 3.12.14/Linux | 444/444 files compiled, 233/233 script exits zero at `37aac57a72303a6d4178790f8d172495e2bc0ada`; independent review and release gates remain open. [Evidence](runtime-refresh-2026-10-29.md) |
| V-33 | Full runtime refresh including subsequent gap fixes | Passed on Python 3.12.14/Linux | 444 sources compiled; 233 scripts exited zero at `f4cffe7ec0877454330b96ff07a15cdea1a5abbb`; independent review/platform/release gates remain open. [Evidence](runtime-refresh-2026-10-29-r2.md) |
| V-09 | Independent review and final release | Open; review requirements documented | Eight gates and reviewer evidence requirements recorded in the [remaining review checklist](remaining-review-checklist.md). Reviewers are unassigned; no sign-off or canonical decision recorded. |

## Remediation monitoring

The [gap-remediation register](gap-remediation-register.md) consolidates twenty partially addressed COV categories with concrete changes, evidence and remaining scope. No category is closed by that register; runtime, substantive coverage and independent approval retain separate states.

## Next actions

The [remaining review checklist](remaining-review-checklist.md) reconciles V-01–V-33 and defines eight evidence gates. The full pinned candidate runtime pass supersedes earlier runtime blockers; no independent review or release approval is inferred.

1. Substantive coverage mapping is complete; resolve recorded gaps and retain browser/visual and full-book navigation review as pending. [Rendered markup sample](rendered-navigation-sample-review.md) passed 14 checks on six pages; Federal Reserve/NIST source-reference findings are [resolved](source-reference-resolution.md). [External audit](external-url-audit.md) records the 102-URL scan. [Section 4.7–4.8 title/scope reconciliation](chapter-04-title-scope-reconciliation.md) is recorded. [Static anchor/reference scan](anchor-reference-link-audit.md) found no local fragment destinations or reference definitions.
2. Address the [prioritized coverage remediation queue](substantive-coverage-index.md). All215 sections are mapped; COV-01–COV-90 remain scoped evidence categories requiring disposition. Begin with numerical contracts/range, independent oracles and project/report promises; retain manual proof/review tasks explicitly.
3. Review numerical fixes and manuscript material independently, recording reviewer and revision.
4. Declare and test supported environments; rerun the agreed suite against the reviewed release revision.
5. Complete editorial/source review and document the authorized canonical decision.


## Update rules

For each completed item record the date, exact commit or snapshot, environment, scope, command or review method, outcome, evidence link and unresolved findings. Reopen affected items when relevant source, requirements or dependencies change. Use **pending**, **in progress**, **passed**, **failed**, or **blocked** with a clear scope; a local automated pass does not mean the book is certified.

## V-34 — Third pinned full-book runtime refresh

Candidate revision `f4cffe7ec0877454330b96ff07a15cdea1a5abbb` passed on Python 3.12.14/Linux: 444 compiled files, 233 successful script exits and 445 verified source/fixture blobs. No failures or timeouts. [Evidence](runtime-refresh-2026-10-29-r3.md). G1 candidate evidence refreshed; G2–G8 unchanged. This is not independent mathematical sign-off or release acceptance.

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

## V-35 — Fourth pinned full-book runtime refresh

[Evidence](runtime-refresh-2026-10-29-r4.md): 452 compiled files, 241 zero-exit scripts, 453 verified source/fixture blobs at `3e185649bf53f5a72ad9e1869d17762110444a26`. No failed/timed-out scripts. Historical V-33 revision labels corrected without changing its evidence. Next executable investigation: COV-68 unequal-spectrum small-eigenvalue cancellation in Section 14.1. Twenty-five categories remain partially addressed; no independent closure/approval.

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

## Project evaluation-error contract — 2026-10-30

[Section18.9 evidence](chapter-18-project-errors-followup.md) directly checks9 pre-callback invalid controls,5 derivative-error cases,15 objective-error positions,3 unneeded-derivative paths,2 affine fallbacks,unchanged callback exception propagation and eager endpoint validation. Two wrong policies are detected; the first checker run passed against the unchanged solver. All27 chapter sources compiled and17 scripts passed at `0939286f031fc23b7b86f25b2f6dc80cb0bda807`; hashes match the pinned tree and remain unchanged after execution. Current inventory488 Python files/277 scripts is not a new full run; V-49 remains the earlier487/276 full execution. COV-81 is newly partially addressed:30 selected categories remain partially addressed,none closed by the register; these are gaps,not defect counts or percentages. Next executable item: COV-81 Section18.10 actual safeguarded-Newton/bisection and three-convention interpolation report integration, with independent references and injected wrong outputs. Broader applied-study, financial/model, independent-review,supported-platform and release obligations stay open.

## Final solver/curve integration and V-50 — 2026-10-30

[Section18.10 evidence](chapter-18-final-method-integration-followup.md) preserves the initial missing-comparison failure and integrates actual Section18.9 safeguarded Newton plus Section18.6 three-convention curve output. Common absolute width thresholds,100-digit Decimal references,independent callback counts,two helper calls and five injected wrong outputs are checked. The recorded Newton implementation uses more callbacks than bisection; no speed claim is made. All28 chapter files compiled and18 scripts passed. [V-50 full execution](runtime-refresh-2026-10-30-r14.md) compiled489 files,passed278 scripts and verified490 required hashes before/after at `54c73a8f98043676edad54efc5725e80f4af883c`, including the preceding project-error checker. Thirty categories remain partially addressed; none closed by the register. Next executable item: COV-81 Section18.10 actual three-step first/second sensitivity and trapezoid/Simpson PV report integration using Section18.7 helpers; the supplemental checker is not itself an integrated final-report field. Broader multiple-IRR input/range,applied/model,independent-review,supported-platform and release obligations stay open.

## Final sensitivity/quadrature integration — 2026-10-30

[Section18.10 evidence](chapter-18-final-studies-followup.md) preserves the missing-study baseline failure and a separate corrected checker-import error. The final report now uses actual Section18.7 price/difference/quadrature/analytic-PV helpers for three sensitivity steps and20/40/80 panels, with units,rounded-reference errors and refinement limits. Decimal/geometric-series references,observed helper calls,seven wrong outputs and strict JSON are checked. All29 chapter sources compiled and19 scripts passed at `015137295af393e4f1783474fc1d24a7cb1c1c7b`; hashes match the pinned tree and remain unchanged after execution. Current inventory490 Python files/279 scripts is not a full run; V-50 remains the earlier489/278 full execution. Thirty categories remain partially addressed; none closed by the register. Next executable item: COV-81 Section18.10 multiple-IRR valuation/input/range and false-root rejection, sharing corrected finite-period arithmetic while preserving single-flow/all-zero valuation and stricter discovery contracts. Broader model/conditioning,independent-review,supported-platform and release obligations stay open.

## Final NPV correction and V-51 — 2026-10-30

[Section18.10 evidence](chapter-18-final-npv-followup.md) preserves two false endpoint-root reports and a failed first regression. Shared exact periodic valuation now rejects those non-root brackets,preserves generic single/all-zero valuations and keeps the IRR-specific flow rules strict. Twenty-one rational references,six discovery rejections,two final-range and seven invalid-input cases,true roots,shared-call observation and a false-zero variant are checked. All30 chapter files compiled and20 scripts passed. [V-51 full execution](runtime-refresh-2026-10-30-r15.md) compiled491 files,passed280 scripts and verified492 required hashes before/after at `ae81661567a38edf78cac3a8c95bc0897819989a`,including final sensitivity/PV integration and both new checkers. Thirty categories remain partially addressed; none closed by the register. Next executable item: COV-80 Sections18.7/18.10 quadrature grid/result range,underflowed/collapsed steps and weighted-sum/intermediate overflow,preserving the retained order/financial oracles. Broader financial/model,applied-negative-case,independent-review,supported-platform and release obligations stay open.

## Quadrature grid/range correction — 2026-10-31

[Sections18.7/18.10 evidence](chapter-18-quadrature-range-followup.md) preserves nine original false-zero/range probes and a failed regression. Exact nominal grids now reject collapsed queries before callbacks; complete rational weighted sums avoid intermediate width/sum loss,and final Simpson shares the corrected helper. Thirty-two2500-digit Decimal rule/grid references,six grid guards,nine callback guards,six final-range rejections and one shared call pass. All31 chapter sources compiled and21 scripts passed at `bb4535d9b6692b7e33430e91b33a6808ded5e4b4`; hashes match the pinned tree and remain unchanged after execution. Inventory492 Python files/281 scripts is not a full execution; V-51 remains the earlier491/280 full pass. Thirty categories remain partially addressed; none closed by the register. Next executable item: COV-80 continuous_cashflow_pv combined product/quotient and small-exponent range,with explicit large-growth-factor limits. Broader smoothness/model,independent-review,supported-platform and release obligations stay open.

## Continuous-stream PV correction and V-52 — 2026-10-31

[Section18.7 evidence](chapter-18-continuous-pv-range-followup.md) preserves five original wrong-value/range probes and a failed regression. Complete product/quotient arithmetic,bounded small-exponent exprel evaluation and an approximate log-growth fallback now retain selected representable PVs; finite inputs validate before zero shortcuts. Eighteen2500-digit Decimal/decay-limit references,five final-range and five invalid-input cases pass. All32 chapter sources compiled and22 scripts passed. [V-52 full execution](runtime-refresh-2026-10-31.md) compiled493 files,passed282 scripts and verified494 required hashes before/after at `5396db3f4b64acb358f08ccfd89b13427ae33268`,including quadrature corrections and both new checkers. Thirty categories remain partially addressed; none closed by the register. Next executable item: COV-80 Section18.6 piecewise-linear/Section18.10 interpolation accepted-input and result range,complete affine quotients and extrapolation policy,with independent affine references. Broader scale/conditioning,financial/model,independent-review,supported-platform and release obligations stay open.

## Complete affine interpolation correction — 2026-10-31

[Sections18.6/18.10 evidence](chapter-18-linear-range-followup.md) preserves five initial probes (including one control) and a failed regression. Complete rational affine evaluation now prevents nonfinite/wrong/false-zero results from intermediate differences or ratios; the final helper shares this implementation. Twelve two-entrypoint2500-digit Decimal reference sets,five multisegment values,explicit extrapolation policies,range/input rejections and a shared call pass. All33 chapter sources compiled and23 scripts passed at `0c6adb3eee831bb109290c5c9e093a05cbdce19a`; hashes match the pinned tree and remain unchanged after execution. Inventory494 Python files/283 scripts is not a new full run; V-52 remains the earlier493/282 full pass. Thirty categories remain partially addressed; none closed by the register. Next executable item: COV-80 Section18.6 Lagrange polynomial normalization/product/sum range and knot recovery,with independent polynomial references. Financial curve suitability,conditioning,independent-review,supported-platform and release obligations stay open.

## Complete polynomial interpolation correction and V-53 — 2026-10-31

[Section18.6 polynomial evidence](chapter-18-polynomial-range-followup.md) retains four baseline probes and the original failed regression. Complete rational basis/product/sum evaluation now rounds once; exact zero is accepted and final overflow or nonzero underflow raises ValueError. Nineteen independently known polynomial/2500-digit Decimal values, two range and four invalid-input cases pass. All34 Chapter18 sources compiled and24 scripts passed at `4d90b8d6a3fdd397c7d071582829d5384fa410ab`.

[V-53 full refresh](runtime-refresh-2026-10-31-r2.md) includes both interpolation corrections/checkers: **495 compiled,284 scripts passed,496 required hashes verified before/after** at `4d90b8d6a3fdd397c7d071582829d5384fa410ab`. Thirty selected categories remain partially addressed; none closed by the register. Next substantive executable item: COV-79 Section18.3 per-iteration bisection halving, midpoint error bounds and the documented iteration-count exercise, using observed callbacks and independent exact bounds. Do not repeat the completed Section18.9 trace audit. Financial/model suitability, conditioning, independent review, supported-platform and release obligations remain open.

## Bisection halving and iteration-count references — 2026-10-31

[Section18.3 evidence](chapter-18-bisection-bounds-followup.md) checks observed callback points against known rational roots on five convergence/exhaustion paths. Dyadic midpoint/width/error bounds are exact; the0.2-to1e-6 exercise uses disclosed binary-rounding allowances and confirms eighteen reductions. Exact N+3 objective-call accounting and five altered records are checked. Initial audit passed; implementation unchanged. All35 Chapter18 files compiled and25 scripts passed at `aa176cb320bc21daf02b18bafa4fde1ec93bbfba`; scoped hashes match the pinned tree and remain unchanged after execution.

Inventory496 Python files/285 scripts is not a new full run; V-53 remains the495/284 full pass with496 required hashes. Thirty selected COV categories remain partially addressed; none closed by the register. Next substantive executable item: Section18.4 observed local Newton convergence-order evidence using an independent root/error reference and actual proposal/callback observations, preserving safeguard conditions; the completed Section18.9 trace audit is separate. Broader continuity/uniqueness, numerical ranges, independent review, supported-platform and release obligations remain open.

## Newton order, tiny discount changes and V-54 — 2026-10-31

[Section18.4 evidence](chapter-18-newton-order-followup.md) records24 accepted isolated Newton proposals,21 local error-order ratios (1.940–1.999), three complete hybrid traces and three altered records. The local simple-root identities use independent100-digit square roots. Each full hybrid accepts one Newton step then34 midpoint fallbacks; quadratic order is not claimed for the hybrid. The initial harness midpoint-assumption failure and corrected reruns are retained; the implementation is unchanged. All36 Chapter18 files compiled and26 scripts passed at `51abbe74562487aed5b14fb4fc84ee4f0b6dc30c`.

[Section18.2 evidence](chapter-18-discount-change-followup.md) adds59 selected1200-digit Decimal power references for tiny discount changes, with a four-ulp allowance and explicit sign/zero checks. Forty-six naive false zeros and three wrong variants are detected. Initial audit passed; implementation unchanged. All37 chapter files compiled and27 scripts passed at `228a2ce79ca4d14cd4c6196238ba2e5a112ea8f5`.

[V-54 full refresh](runtime-refresh-2026-10-31-r3.md) compiled498 files,passed287 scripts and verified499 required hashes before/after at `228a2ce79ca4d14cd4c6196238ba2e5a112ea8f5`,including all three checkers added since V-53. Thirty selected COV categories remain partially addressed; none closed by the register. Next substantive executable item: Section18.2 annuity PV accepted-input and complete product/quotient range,including tiny-rate/period scaling,zero-rate branch and representable versus unrepresentable final values,with independent cash-flow/analytic references. Broader local-convergence proof,continuity/uniqueness,conditioning,financial/model,independent-review,supported-platform and release obligations remain open.

## Annuity PV range and V-55 — 2026-11-04

[Section 18.2 annuity evidence](chapter-18-annuity-range-followup.md) retains 14 initial failed numerical cases and the successful rerun of all 22 numerical and five invalid-input cases. Complete discount and payment scaling now preserves selected representable results and rejects final overflow or nonzero underflow. [V-55](runtime-refresh-2026-11-04.md) compiled 499 files, passed 288 scripts and verified 500 required hashes before and after at `eac8f8da5643d573ad9f5946c09b12622c422c7e`. Thirty COV categories remain partially addressed; none closed. Next substantive item: Section 18.1 Exercise 16, independently bound the exponential Taylor remainder and compare the reported approximation error across selected magnitudes. Independent review, supported platforms and release acceptance remain pending.

## Taylor remainder oracle — 2026-11-04

[Section 18.1 evidence](chapter-18-taylor-remainder-followup.md) compares 11 actual reports with independent positive and alternating-series bounds and high-precision references. Two rounded zero differences are distinguished from nonzero mathematical remainders. The first audit passed; the numerical helper is unchanged. All 39 Chapter 18 sources compiled and 29 scripts passed at `9c77e189563fd2fc7bbcee7b43d2ee0c8a82b191`. V-55 remains the latest full pass (499 files, 288 scripts, 500 hashes); this subsequent checker has scoped evidence. Thirty COV categories remain partially addressed; none closed. Next substantive item: Section 18.1 present-value and error-report range, including false zero from an overflowing discount denominator and representable versus out-of-range diagnostics. Independent review, supported platforms and release approval remain pending.

## Present-value, error-report and cent rounding range — 2026-11-04

[PV and error-report checks](chapter-18-pv-error-range-followup.md) preserve 13 initial failures and a 26-case pass at `5504f2cf019487dae61912e6b01bdb6440931307`. [V-56](runtime-refresh-2026-11-04-r2.md) compiled 501 files, passed 290 scripts and matched 502 required hashes before and after execution. The subsequent [cent rounding checks](chapter-18-cents-range-followup.md) preserve 18 initial failures and pass all 32 observations at `7b779924a288286a39a55a98f7383bdc4310989d`; 41 Chapter 18 files compiled and 31 scripts passed. Thirty COV categories remain partially addressed; none closed. Next substantive item: Section 18.2 growth factor, growth increment and discount-change range and saturation policy with independent power references. Independent review, supported platforms and release approval remain pending.

## Compound growth and discount range — 2026-11-04

[Section 18.2 range checks](chapter-18-growth-discount-range-followup.md) preserve 27 initial failures and a 75-case pass at `1cdc4c891bd443dbbc5303d2f5715b26350da7bc`. [V-57](runtime-refresh-2026-11-04-r3.md) compiled 503 files, passed 292 scripts and verified 504 required hashes before and after execution. Thirty COV categories remain partially addressed; none closed. Next substantive item: Section 18.2 decimal-text cent rounding, including caller context isolation, half-even ties and explicit accepted magnitude/output limits. Independent review, supported platforms and release approval remain pending.

## Decimal-text cents — 2026-11-04

[Section 18.2 evidence](chapter-18-decimal-text-cents-followup.md) preserves 16 initial failures and a 32-observation pass at `3bb510f1715d9f734bc5e73ea19783e73f0ac4bf`. The formatter now isolates caller context and documents the original default output limit. All 43 Chapter 18 sources compiled and 33 scripts passed. V-57 remains the latest full run; this later change has scoped evidence. Thirty COV categories remain partially addressed; none closed. Next substantive item: Section 18.1 exponential approximation and cancellation-report range contracts, separating true saturation from a rounded zero and checking error behavior at extreme exponents. Independent review, supported platforms and release approval remain pending.

## Exponential reports and Chapter 19 applied cases — 2026-11-04

[Section 18.1 evidence](chapter-18-exponential-report-range-followup.md) preserves eight initial failures and a 44-case pass. [V-58](runtime-refresh-2026-11-04-r4.md) compiled 505 Python files, passed 294 scripts and verified 506 required hashes before and after at `46aa9c5a32f9a3293bcd7926efa4c04c984a3258`. Subsequent [Section 19.10 evidence](chapter-19-applied-target-timing-followup.md) preserves the missing applied outputs and passes all 11 observations at `62691beb94b8747787990a187ea5925eaeb9208d`; all 22 Chapter 19 sources compiled and 12 scripts passed. COV-84 is newly partially addressed, bringing the register to 31 selected categories partially addressed and none closed. Next substantive item: Section 19.8 discrete-to-continuous contribution frequency convergence, with independent finite cash-flow and integral references. Independent review, supported platforms and release approval remain pending.

## Contribution frequency, Euler stability and V-59 — 2026-11-05

[Section 19.8 evidence](chapter-19-contribution-frequency-followup.md) checks 20 finite-sum references, six identity controls, 16 observed/reference order ratios and three wrong variants. The initial harness failure and corrected rounding allowance are retained; the numerical helper is unchanged. [Section 19.5 evidence](chapter-19-euler-stability-followup.md) checks six observed four-step decay paths against exact amplification references and detects three altered records. All 24 Chapter 19 sources compiled and 14 scripts passed at `36006c921c0c005f2812e0589f2b68e64dfc17b4`.

[V-59](runtime-refresh-2026-11-05.md) compiled 508 Python files, passed 297 scripts and matched 509 required source/fixture hashes before and after at the same pin. Thirty-one selected COV categories remain partially addressed; none closed. Next substantive item: Section 19.5/19.6 arbitrary time-varying forcing, with independent polynomial solution/stage references and actual callback-time observations; selected constant-flow and decay cases are already covered. Independent review, supported platforms and release approval remain pending.

## Time-varying forcing, nonterminal jumps and V-60 — 2026-11-05

[Forcing evidence](chapter-19-time-varying-forcing-followup.md) covers20 Euler/RK4 grids, six observed order ratios and a coupled four-stage rational reference; the initial checker allowance failure and rerun are retained. [Section19.7 nonterminal evidence](chapter-19-nonterminal-jump-followup.md) preserves two initial failed policy cases and an eight-case pass, plus unchanged public-domain validation. Signed continuation now works across negative intermediate balances only in explicit nonterminal mode. All26 Chapter19 sources compiled and16 scripts passed at `9f2f2ae7297b44fa443a0fe70a5e2616a74a4536`.

[V-60](runtime-refresh-2026-11-05-r2.md) compiled510 Python files,passed299 scripts and matched511 required source/fixture hashes before/after at the same pin. Thirty-one selected COV categories remain partially addressed; none closed. Next substantive item: Section19.3 piecewise contribution-transition continuity and independent segment-integral references, rather than reusing the account primitive for expected values. Independent review, supported platforms and release approval remain pending.

## Piecewise continuity, logistic trajectories and V-61 — 2026-11-05

[Piecewise evidence](chapter-19-piecewise-continuity-followup.md) passes nine independent prefix references,18 two-sided transition probes and zero/split-segment controls. [Logistic evidence](chapter-19-logistic-trajectory-followup.md) passes54 reciprocal-coordinate references and five split-time controls, including above-capacity trajectories. Both initial audits passed; numerical helpers are unchanged. All28 Chapter19 files compiled and18 scripts passed at `9f66a3c24a0c66a7afc6605a6ccd0b04ac334b0c`.

[V-61](runtime-refresh-2026-11-05-r3.md) compiled512 Python files,passed301 scripts and matched513 required source/fixture hashes before/after at the same pin. Thirty-one selected COV categories remain partially addressed; none closed. Next substantive item: Section19.2 logistic accepted-input and result range, including t=0 identity at extreme initial/capacity ratios, positive subnormal results and large-exponent saturation, with independent reciprocal/rational references. Independent review, supported platforms and release approval remain pending.

## Logistic and quadratic growth range — 2026-11-05

[Logistic evidence](chapter-19-logistic-range-followup.md) preserves ten initial failures and a25-case pass with independent reciprocal-coordinate references. [Quadratic evidence](chapter-19-quadratic-range-followup.md) preserves two initial failures and a22-case pass against an exact reciprocal-state oracle. All30 Chapter19 files compiled and20 scripts passed at `9b4ae81bb9d057d7a904083f34f7586dcf3ec301`.

[V-62](runtime-refresh-2026-11-05-r4.md) compiled514 Python files,passed303 scripts and matched515 required source/fixture hashes before/after at the same pin. Thirty-one selected COV categories remain partially addressed; none closed. Next substantive item: Section19.2 pure growth, affine-time-rate growth and proportional-withdrawal accepted-input/result range, including complete exponent cancellation and finite scaled outputs, with independent integrated-rate references. Independent review, supported platforms and release approval remain pending.

## Integrated growth range and V-63 — 2026-11-05

[Section 19.2 evidence](chapter-19-integrated-growth-range-followup.md) preserves 18 initial failed cases, an intermediate rerun with six remaining affine-rate failures, and a final 36-case pass. Complete exact integrated rates and wider scaled exponential evaluation now retain selected finite amounts; nonzero final underflow and overflow reject explicitly. All 31 Chapter 19 sources compiled and 21 scripts passed at `ea55f5efc6c94d8e8f64b791641c48e7a064947e`.

[V-63](runtime-refresh-2026-11-05-r5.md) compiled 515 Python files, passed 304 scripts and matched 516 required source/fixture hashes before/after at the same pin. Thirty-one selected COV categories remain partially addressed; none closed. Next substantive item: Section 19.8 nominal/continuous rate-conversion accepted-input and result range, including tiny rate-to-frequency quotients, large integer frequencies and finite inverse conversions, with independent logarithm/power references. Independent review, supported platforms and release approval remain pending.

## Nominal/continuous rate-conversion range and V-64 — 2026-11-05

[Section 19.8 evidence](chapter-19-rate-conversion-range-followup.md) preserves 24 initial failed checks and a final 52-case pass, including tiny quotients, 1,001-digit frequency inputs, inverse conversion range and invalid-frequency controls. Complete scaling now retains selected finite rates; negative nominal saturation and the loss of round-trip invertibility at the rounded boundary are documented. All 32 Chapter 19 sources compiled and 22 scripts passed at `29e2c8fc93087cb58cf08f641f49c58e9ac33a05`.

[V-64](runtime-refresh-2026-11-05-r6.md) compiled 516 Python files, passed 305 scripts and matched 517 required source/fixture hashes before/after at the same pin. Thirty-one selected COV categories remain partially addressed; none closed. Next substantive item: Section 19.8 continuous/discrete growth balance range, including complete nominal-period exponent and initial-amount scaling, time-zero identities and representable final results, with independent finite-power/integrated-rate references. Independent review, supported platforms and release approval remain pending.

## Continuous/discrete growth-balance range and V-65 — 2026-11-05

[Section19.8 evidence](chapter-19-growth-balance-range-followup.md) preserves15 initial failures and a31-case pass. Complete nominal-period scaling and shared final exponential evaluation now retain selected representable balances; two observed calls check actual shared-helper use. All33 Chapter19 sources compiled and23 scripts passed at `47511f620984be32b808cd5b50897fbf18eb9f19`.

[V-65](runtime-refresh-2026-11-05-r7.md) compiled517 Python files,passed306 scripts and matched518 required source/fixture hashes before/after at the same pin. Thirty-one selected COV categories remain partially addressed; none closed. Next substantive item: Section19.8 continuous/end-period contribution balance range, including complete weighted accumulation, signed-flow cancellation, zero-rate/time identities and representable final values, with independent finite-payment/integral references. The contribution-frequency order oracle is already complete for its selected scope. Independent review, supported platforms and release approval remain pending.

## Contribution-balance range and V-66 — 2026-11-05

[Section19.8 evidence](chapter-19-contribution-balance-range-followup.md) preserves17 original failed cases, the first correction's pass, an intermediate false-finite large-period probe and a final33-case pass. Complete accumulation, exact zero-rate arithmetic and retained tiny period corrections now preserve selected balances. The declared end-period exponent evaluation limit remains an explicit open scope boundary. All34 Chapter19 files compiled and24 scripts passed at `552d14965ec893cb3022e7f9d1ee6e6596f9f7e5`.

[V-66](runtime-refresh-2026-11-05-r8.md) compiled518 Python files,passed307 scripts and matched519 required source/fixture hashes before/after at the same pin. A15-second scoped timeout in the unchanged rate-conversion checker is retained separately; scoped and full reruns used60 seconds per script. Thirty-one selected COV categories remain partially addressed; none closed. Next substantive item: Section19.8 depletion-time accepted-input/classification range, including complete rate*balance/withdrawal ratios near the nondepletion threshold and zero-rate quotient representability, with independent reciprocal/logarithmic references. Do not repeat the already-retained small-rate depletion cases. Independent review, supported platforms and release approval remain pending.

## Depletion classification, project event range and V-67 — 2026-11-05

[Section19.8 evidence](chapter-19-depletion-classification-range-followup.md) preserves seven initial failures and a24-case pass using independent reciprocal/logarithmic references. Exact threshold classification and complete scaling now preserve selected finite depletion times and reject unrepresentable nonzero times. [Section19.9 project evidence](chapter-19-project-depletion-range-followup.md) preserves four original failed simulator scenarios and passes all four after signed-flow delegation; one injected call verifies actual shared use. All36 chapter files compiled and26 scripts passed at `95dcc535a881a90fad323f8a2528cd2caf7f0fff`.

[V-67](runtime-refresh-2026-11-05-r9.md) compiled519 Python files,passed308 scripts and matched520 required source/fixture hashes before/after at `175c27e55a4eb0d48011937661f3295363d2c890`. The project adapter/checker are subsequent scoped evidence; current520-file/309-script inventory is not a new full run. Thirty-one selected COV categories remain partially addressed; none closed. Next substantive item: Section19.9 signed continuous-transition range and resulting project report consistency, including equilibrium cancellation and finite scaled balances between jumps. The exact depletion/classification scenarios above are complete for their selected scope. Independent review, supported platforms and release approval remain pending.

## Project transition, affine method steps and V-68 — 2026-11-05

[Project transition evidence](chapter-19-project-transition-range-followup.md) preserves 14 initial failures and a 19-case pass, plus an observed shared-helper call. Actual simulator balances, jump logs, post-jump depletion and result metadata use independent exponential/integral references. All 37 chapter sources compiled and 27 scripts passed at `908a65f2cd68240d65ef70f8a86c63078660218e`.

[V-68](runtime-refresh-2026-11-05-r10.md) compiled 521 Python files, passed 310 scripts and matched 522 required source/fixture hashes before and after at the same pin. Subsequent [affine account-step evidence](chapter-19-account-step-range-followup.md) preserves 12 initial failures and a 30-case pass using whole-horizon rational geometric method references. Complete Euler/RK4 affine increments now retain selected finite states; all 38 chapter files compiled and 28 scripts passed at `f60205d5025a2eb4a4055ad746074fe3a198f3c7`. Current 522-file/311-script inventory is not a new full run. Thirty-one selected COV categories remain partially addressed; none closed.

Next substantive item: Section 19.10 cumulative exact-account, depletion and timed-deposit range/integration contracts. Its copied helpers still evaluate naive exponential/ratio expressions; independently check complete balances, exact withdrawal thresholds and jump scaling before sharing corrected implementations. Do not repeat the completed Section 19.8/19.9 fixtures as a new result without exercising the actual cumulative helper/report paths. Section 19.8 end-period abs(rate*years)>4000 remains an explicit evaluation limit. Independent review, supported platforms and release approval remain pending.

## Cumulative lab scope and command markup — 2026-11-05

[Scope and command evidence](chapter-19-cumulative-scope-command-followup.md) reconciles Section 19.10's scalar steppers, separate depletion calculation and signed analytical jump helper with the promised lab scope. Terminal scheduling/event logs belong to Section 19.9; no numerical implementation changed. All ten Chapter 19 manuscripts had escaped bash fences; initial static failures are retained. At `f4144ee674ed49fcbebb460426cc1986d24ba14d`, ten corrected command blocks contain twenty existing source/checker targets; all 59 recognized local manuscript destinations exist and all ten published manuscripts were re-fetched exactly.

Runtime blocker: the execution tool returned "No usable execution environment is available. Wait for an environment to become available before using this tool." No Python compilation/execution or full refresh occurred. GitHub/static manuscript work proceeded. Current pinned inventory remains 522 Python files, 311 scripts and 523 required source/fixture blobs; V-68's 521/310/522 full pass and later Section 19.8 38/28 scope remain historical and distinct. Thirty-one selected COV categories remain partially addressed; none closed.

Resume next: when execution is available, run the retained Section 19.10 baseline range probes before modifying its copied exact-account, depletion or timed-deposit helpers; preserve initial results and extend exact threshold and actual integration expectations. The numerical obligation is not completed by this manuscript batch. A runnable unexecuted handoff and exact source blobs are retained in the report. If runtime remains unavailable, continue other tracked manuscript/navigation work; do not repeat this completed Chapter 19 fence audit or report a new runtime pass. Independent review, supported platforms and release approval remain pending.

## Invariant lab scope and exact matrix counterexample — 2026-11-05

[Section 20.3 scope evidence](chapter-20-invariant-scope-followup.md) reconciles the advertised covariance/evidence lab with the actual scalar 2×2 quadratic helper and fixed-scenario assessment. The manuscript now states that symmetry, general PSD/orthogonality, variable-rate curves and source/command provenance are not implemented by this companion. An independently derived nonsymmetric-matrix counterexample has exactly the same positive quadratic form as a symmetric positive-definite matrix. Six direct matrix-vector calculations, sum-of-squares identities, symmetry controls and the Applied D negative value passed exact BigInt checks in JavaScript; Python helper execution is not claimed.

COV-85 is newly partially addressed for this selected manuscript/counterexample scope: 32 selected categories now partially addressed, none closed. This count is not a defect total or completion percentage. No Python source/checker changed; V-68 and the later Section 19.8 scoped run remain the established runtime evidence. The execution environment is unavailable, so no new compile/script/full-book pass is claimed.

Resume Section 19.10's retained baseline range/integration probes once Python execution returns. If it remains blocked, next independent manuscript task: reconcile Section 20.5's vector/scaled-residual lab promises with its source and actual assertions. Chapter 19 command fences and Section 20.3 scope are completed for their recorded static boundaries; do not repeat them as new numerical results. Independent review, supported platforms and release approval remain pending.

## Cumulative account/step range and V-69 — 2026-11-05

Python execution is available again; the earlier environment blocker is resolved for this run. [Cumulative account evidence](chapter-19-cumulative-account-range-followup.md) preserves 17 baseline failed cases and a 44-case pass against independent integral/reciprocal-log/separately compounded payment references. Actual deposit and depletion shared-helper use is observed; signed analytical jump scope and finite intermediate-state requirements remain explicit. All 39 chapter files compiled and 29 scripts passed at `baf06212851ca7949fad4376e4b9857184fb1cb9`.

[Cumulative step evidence](chapter-19-cumulative-step-range-followup.md) preserves nine baseline failed cases and a 30-case pass with rational whole-horizon geometric method expectations and actual report fields. Six observed shared-method calls verify assessment integration. All 40 chapter files compiled and 30 scripts passed at `e747c068bfebd0959444b62b31fe25fe784cfa46`.

[V-69](runtime-refresh-2026-11-05-r11.md) compiled all 524 Python files, passed all 313 discovered scripts and matched all 525 required source/fixture hashes before/after at that same pin. It includes the prior Section 19.8 account-step change and both cumulative corrections/checkers. The baseline snapshot newline-transfer failure/correction is retained separately from numerical failures. Thirty-two selected COV categories remain partially addressed; none closed. Independent review, supported platforms and release approval remain pending.

Next substantive numerical item: Section 20.2 known-value benchmark helper range, starting with the closed annuity's complete payment/geometric scaling and explicit-sum comparison. The source still evaluates payment*expm1 before its final division; independently classify finite final values, genuine overflow/underflow and valid zero identities before changing behavior. Exercise the actual Section 20.2 helpers, not only already-tested Section 20.4 counterparts. Section 20.5 vector/scaled-residual manuscript scope remains a separate pending task. Section 19.10's selected range/integration obligations above are complete for the retained fixtures, not general numerical certification. Section 19.8 end-period abs(rate*years)>4000 remains an open evaluation boundary.

## Benchmark annuity range, vector/residual design and V-70 — 2026-11-05

[Section 20.2 annuity evidence](chapter-20-benchmark-annuity-range-followup.md) retains 20 original failed cases and a 62-case pass against an independent backward cash-flow recurrence. Exact represented-input arithmetic now preserves selected tiny payments, small rates and finite sums hidden by large powers; true final overflow/nonzero underflow rejects. The initial summary-only KeyError after result capture is recorded separately. Exact rational numerator/denominator sizes and memory/time grow with period count; these are reference benchmarks, not a constant-cost arbitrary-horizon pricing implementation. All 20 chapter sources compiled and 11 scripts passed at `825bca6fb21fec89f5598a26de3ee0c7745f1202`.

[Section 20.5 design evidence](chapter-20-vector-residual-design-followup.md) passes six initial cases: two componentwise-versus-vector-norm counterexamples and four exact diagonal-system scaled-residual/forward-error examples. Actual scalar comparator/error functions are exercised; the scalar implementation is unchanged. The manuscript separates selected design work from a general vector/solver API and distinguishes signed constraint residual from nonnegative violation. All 21 chapter sources compiled and 12 scripts passed at `e1364e25cf09cadb7210372c24d2cf8ef4ab0f67`.

[V-70](runtime-refresh-2026-11-05-r12.md) compiled all 526 Python files, passed all 315 discovered scripts and matched all 527 required source/fixture hashes before/after at the same final executable pin. Thirty-two selected COV categories remain partially addressed; none closed. Independent review, supported platforms and release approval remain pending.

Next substantive numerical item: Section 20.2's remaining continuous-account and depletion accepted-input/result-range contracts, including actual assessment integration. Its account still forms separate exponential/flow terms and its depletion helper still forms the rounded rate*balance/withdrawal ratio; compare independent complete-balance and exact threshold/reciprocal-log expectations before sharing or changing implementations. The annuity cases above are complete for their selected scope and must not be repeated as new progress. Present-value/rate-conversion copies and broader matrix/vector/unit work remain separate obligations. Section 19.8 end-period abs(rate*years)>4000 remains an open evaluation boundary.

## Benchmark/invariant account range and V-71 — 2026-11-05

[Section 20.2 account/depletion evidence](chapter-20-benchmark-account-range-followup.md) retains 16 initial failed cases and a 36-case pass against independent complete-balance, exact-threshold and reciprocal-log references, including two exact half-subnormal rounding controls. Actual assessment account/depletion calls are observed. The new chapter-local kernel adapts selected pinned Section 19.8 calculation bodies without cross-chapter imports or sys.path mutation; public guards and signed analytical scope remain. All 23 chapter files compiled and 13 scripts passed at `1008849303f6317fcaa343dde97ee8b9fc73216a`.

[Section 20.3 composition evidence](chapter-20-invariant-account-range-followup.md) retains 11 original failed cases and a 20-case pass. Direct, prefix and split balances use independent references, and four observed assessment calls verify actual prefix/resume/reconciliation integration. All 24 chapter files compiled and 14 scripts passed at `d0266c34257e717c964b8bc8c8a145c9d8448e53`.

[V-71](runtime-refresh-2026-11-05-r13.md) compiled all 529 Python files, passed all 317 discovered scripts and matched all 530 required source/fixture hashes before/after at that same pin. Thirty-two selected COV categories remain partially addressed; none closed. Case failures are not defect totals or completion percentages. Independent review, supported platforms and release approval remain pending.

Next substantive numerical item: Section 20.2 present-value and nominal-to-continuous benchmark range, including complete rate*time scaling, tiny rate/frequency quotients, valid zero identities, actual assessment use and independently derived valuation/conversion expectations. Those copied helpers still use separate float exponent/rate-quotient arithmetic. The selected account/depletion/composition cases above are complete for their retained scope; do not repeat them as a new result. Other Section 20.3 discount/FV, matrix/portfolio and provenance/manual work remain open. Section 19.8 end-period abs(rate*years)>4000 remains an explicit evaluation boundary.

## Benchmark/invariant valuation range and V-72 — 2026-11-05

[Section 20.2 valuation/conversion evidence](chapter-20-benchmark-valuation-range-followup.md) retains 15 original failed cases and a 39-case pass against independent complete-discount and periodic-gross/logarithm references. Selected tiny quotients, positive-gross boundary cases and 1,001-digit frequencies are covered; actual assessment valuation/conversion calls and the derived growth field are observed. A chapter-local kernel adapts pinned Section 19.2/19.8 calculation bodies without cross-chapter runtime imports or sys.path changes. All 26 chapter files compiled and 15 scripts passed at `df88087d11b755fa379796ad1efdd2932a7f2811`.

[Section 20.3 factor/PV/FV evidence](chapter-20-invariant-valuation-range-followup.md) retains 16 initial failed cases and a 40-case pass with direct, actual inverse, cash-flow and report references. Eleven observed shared calls verify composition, split payments and returned FV feeding PV. Nonzero final underflow and overflow reject; a separately unrepresentable factor does not by itself invalidate a finite scaled amount. Term rounding and aggregate-range limits remain explicit. All 27 chapter files compiled and 16 scripts passed at `ec2d14291906ca137698e6716779a4634495b18b`.

[V-72](runtime-refresh-2026-11-05-r14.md) compiled all 532 Python files, passed all 319 discovered scripts and matched all 533 required source/fixture hashes before/after at the same pin. Thirty-two selected COV categories remain partially addressed; none closed. Case failures are not defect totals or completion percentages. Independent review, supported platforms and release approval remain pending.

Next substantive numerical item: Section 20.3 raw quadratic-form and portfolio-feasibility accepted-input/result-range contracts. Derive complete rational quadratic-form and weight-sum/threshold expectations before changing behavior; distinguish numerical arithmetic/classification from unimplemented general symmetry/PSD validation. The scalar helper still forms b+c and its products separately, and feasibility still depends on a rounded floating-point sum. The selected valuation/conversion cases above are complete for their retained scope and must not be repeated as new progress. Other benchmark linear-system/provenance/manual obligations remain open. Section 19.8 end-period abs(rate*years)>4000 remains an explicit evaluation boundary.


## Matrix/feasibility and two-by-two benchmarks — V-73 (2026-11-05)

[Section 20.3 matrix range](chapter-20-invariant-matrix-range-followup.md) retains 12 original failed cases and a 36-case pass. Decimal row-product references and exact integer-scale feasibility expectations cover complete arithmetic, cancellation, range limits and actual assessment integration. Exact budget checks use the represented inputs; symmetry, PSD and optimality remain separate. Chapter scope: 28 files compiled and 17 scripts passed at `c8110de2a09da05fca5591c5a70c0d9278f51df4`.

[Section 20.2 linear benchmark range](chapter-20-benchmark-linear-range-followup.md) retains seven original failed cases and a 19-case pass. Independent exact pivoted elimination, equation residuals and assessment observation cover determinants lost to intermediate range or cancellation and final solution range rejection. Chapter scope: 29 files compiled and 18 scripts passed at `5988dee92cf70f48f718bf8b96e0ae465d22ee42`.

[V-73](runtime-refresh-2026-11-05-r15.md) compiled all 534 Python files, passed all 321 discovered scripts and matched all 535 required source/fixture hashes before and after at that executable pin. Thirty-two selected COV categories remain partially addressed; none closed. Independent review, supported platforms and release approval remain pending.

Next substantive item: Section 20.4 discrete present-value and annuity result-range boundaries beyond the retained subnormal-payment fix. Derive independent represented-gross power and finite payment-sum expectations; preserve the declared rate/period domains and assess the existing OverflowError contract separately from Section 20.2. Probe valid zero identities, full amount scaling and final range rejection before changing the helpers. The selected matrix, feasibility and two-by-two fixtures above are complete for their retained scope. Section 19.8's end-period exponent boundary and other manual/provenance obligations remain open.


## Discrete valuation and rounded-term aggregation — V-74 (2026-11-05)

[Section 20.4 discrete range](chapter-20-boundary-discrete-range-followup.md) retains 22 original mismatches across 60 cases and three intermediate failures from expanded exact half-subnormal probes. All 64 final cases pass. Independent represented-gross powers, payment recurrence and huge-count bounds check complete scaling, zero identities and rounding behavior. Genuine overflow still raises OverflowError and genuine underflow may return signed zero; the longer non-dyadic evaluation is not a general correct-rounding proof.

[Section 20.6 aggregate range](chapter-20-metamorphic-aggregate-range-followup.md) retains seven failed baseline cases and a 27-case pass. A common-scale dyadic oracle and observed calls verify complete accumulation of rounded terms, permutation stability and final overflow. Per-term discounting and its validation/range rules are unchanged.

[V-74](runtime-refresh-2026-11-05-r16.md) compiled all 536 Python files, passed all 323 discovered scripts and matched all 537 required source/fixture hashes before and after at `8795c02e5bbe873cd6db42a26564cc9adc7a070e`. Final Chapter 20 scope: 31 files compiled and 20 scripts passed. Thirty-two selected COV categories remain partially addressed; none closed. Independent review, supported platforms and release approval remain pending.

Next substantive item: Section 20.9 project valuation result-range and Section 20.10 delegation checks. The project still forms its discount factor separately from the monetary term and uses a potentially overflowing partial sum. Derive independent complete-term and final-aggregate expectations, distinguish its existing domain and exception contract, and verify the actual Section 20.10 assessment path. The pending dossier must remain separate from runtime evidence and approval. Do not repeat the completed Section 20.4 or 20.6 fixtures as new coverage. Section 19.8's end-period exponent boundary and other manual/provenance obligations remain open.


## Project valuation and manifest preflight — V-75 (2026-11-05)

[Project valuation and Section 20.10 delegation](chapter-20-project-valuation-range-followup.md) retains 17 baseline mismatches and a 48-case pass using independent scaled-term and represented-total references. The actual assessment callable, assessment suite and pending dossier were exercised. The project permits genuine underflow and retains OverflowError for unrepresentable terms or totals; existing shared-kernel defaults are unchanged. Project scope: 32 files compiled and 21 scripts passed at `503edbdc3e622f98acabea861a53ac1581b9132f`.

[Manifest preflight](chapter-20-manifest-preflight-followup.md) retains seven failed baseline rows and a ten-case pass for validation/serialization before exclusive creation, valid retry, preserved collision bytes and pending fields on disk. This adds selected partial COV-86 evidence. Actual provenance, authenticity, independent review and filesystem failure recovery remain open.

[V-75](runtime-refresh-2026-11-05-r17.md) compiled all 538 Python files, passed all 325 discovered scripts and matched all 539 required source/fixture hashes before and after at `081a73dce77591e11377df37ff7b23c5d1836674`. Final Chapter 20 scope: 33 compiled files and 22 passing scripts. Thirty-three selected COV categories are partially addressed; none closed. Independent review, supported platforms and release approval remain pending.

Next substantive item: Section 21.3 effective/continuous conversion and fractional-horizon valuation boundaries from the Chapter 21 map. Derive independent effective gross-power and continuous exponential expectations, check negative rates and the rounded effective-minus-one rejection boundary, and verify distinct convention and input rules before editing. Do not count repeated Chapter 20 fixtures as new coverage. Chapter 21 actual provenance and independent review, Section 19.8's end-period exponent boundary, and other manual obligations remain open.


## Capstone valuation and analytic sensitivity — V-76 (2026-11-05)

[Section 21.3 rate and valuation evidence](chapter-21-capstone-rate-range-followup.md) retains ten baseline mismatches and a 53-case pass. Independent effective gross-power, continuous exponential and conversion references cover fractional horizons, negative rates, the rounded-minus-one boundary, complete term scaling and the actual capstone cash-flow field. Conversion code is unchanged. Chapter scope at `239085a0580b7a97db6787e415c36f20d11f706c`: 20 files compiled and 11 scripts passed.

[Section 21.4 sensitivity evidence](chapter-21-capstone-sensitivity-range-followup.md) retains 17 baseline mismatches and a 32-case pass. Selected independent complete PV, derivative and Taylor references and the actual capstone analytic field verify the corrected scaling; finite-difference stencil guards are unchanged. This adds selected partial COV-90 evidence, not a general range proof.

[V-76](runtime-refresh-2026-11-05-r18.md) compiled all 540 Python files, passed all 327 discovered scripts and matched all 541 required source/fixture hashes before and after at `77a943c4ee6551431485c3a53d71f789691c2392`. Final Chapter 21 scope: 21 compiled files and 12 passing scripts. Thirty-four selected COV categories are partially addressed; none closed. Independent review, supported platforms and release approval remain pending.

Next substantive item: Section 21.5 replication screening, solve and residual ranges. Derive independent normalized determinant and pivoted-solve expectations, check the declared screening threshold separately from singularity, and check residuals on the returned represented holdings. Include selected finite results hidden by overflowing intermediate products and the actual integrated report path. Preserve the limited 2x2 interface and do not repeat the Section 20.2 benchmark fixtures as new coverage. Chapter 21 actual provenance and independent review, Section 19.8's end-period exponent boundary, and other manual obligations remain open.

## Capstone replication and allocation — V-77

[Replication](chapter-21-capstone-replication-range-followup.md) records five baseline mismatches and a 14-case pass against independent pivoted elimination, exact screening and residual checks on returned holdings. [Allocation](chapter-21-capstone-allocation-range-followup.md) records seven baseline mismatches and a 20-case pass against a high-precision projection and represented-weight feasibility reference. Both check the actual integrated report fields. Section 21.5 keeps its two-by-two screen; Section 21.6 keeps its two-weight teaching objective. These are selected additions to COV-90. Thirty-four selected COV categories are partially addressed; none closed.

[V-77](runtime-refresh-2026-11-05-r19.md) compiled 542 files, passed 329 scripts and matched 543 required blobs before and after at `bc29b0d67dfd61b3d522d36d956b768101fee0ab`. Chapter 21 scope: 23 compiled files, 14 passing scripts. Independent review, supported-platform evidence and release approval remain pending.

Next substantive item: [Section 21.7 baseline probes](chapter-21-capstone-account-range-baseline.md) reproduced four false overflow results in the unconstrained transition. Retain that initial evidence and build an independent account oracle for equilibrium, scaled growth and flow, cancellation and genuine overflow. Check the actual Section 21.9 account field and document the output underflow policy. Section 19.8's end-period exponent boundary, COV-88 provenance and requirement fulfillment, and wider manual obligations remain open.

## Capstone account and requirements traceability — V-78

[Account range](chapter-21-capstone-account-range-followup.md) retains 17 initial mismatches and a 29-case pass for the complete account transition and actual integrated field. It covers equilibria, scaled growth and flow, cancellation, signed zero, and genuine overflow while keeping the unconstrained final-state contract.

[Requirements and preflight evidence](chapter-21-capstone-requirements-evidence-map.md) maps F1–F8 to implemented evidence and manual obligations. It retains the cash-flow preflight failure and the 16-test pass: both row orders now report the invalid date before discounting, and a valid one-shot iterator still works. The map distinguishes proposed diagnostics from the actual report and its pending placeholders. COV-88 is newly partially addressed; COV-90 gains selected account evidence. Thirty-five selected COV categories are partially addressed; none closed.

[V-78](runtime-refresh-2026-11-05-r20.md) compiled 543 files, passed 330 scripts and matched 544 required blobs before and after at `59f713d346fbcbf14e7125902637cd2f6e2c56e4`. Chapter 21: 24 compiled files and 15 passing scripts. Independent review, supported platforms and release approval remain pending.

Next substantive item: [Section 19.8 end-period exponent baseline](chapter-19-end-period-exponent-baseline.md) records four finite-payment cases rejected under the documented exponent limit. Evaluate a bounded extension against independently derived end-period sums and genuine range failures; keep the Chapter 19 underflow contract. Wider Chapter 21 provenance, proofs and review remain open.

## End-period exponent extension — V-79

[Section 19.8 end-period extension](chapter-19-end-period-exponent-followup.md) preserves 15 baseline mismatches, separates a checker exception-classification issue, and records a 23-case pass against separately timed sums and analytical bounds. The nontrivial end-period domain extends through abs(rate*years)=5000; final overflow and nonzero underflow still reject. Broader exponent and rounding coverage remains open under COV-84. Thirty-five selected COV categories are partially addressed; none closed.

[V-79](runtime-refresh-2026-11-05-r21.md) compiled 544 files, passed 331 scripts and matched 545 required blobs before and after at `c961e9064fbb07217c8c7af64adf909e399f165f`. Chapter 19: 41 compiled files and 31 passing scripts. Independent review, supported platforms and release approval remain pending.

Next substantive item: [Section 19.6 RK4 range baseline](chapter-19-rk4-stage-range-baseline.md) records two observed failures involving a finite weighted increment and a finite callback stage. Derive exact stage inputs and outputs and check actual fixed/adaptive consumers; treat adaptive estimator/scale range as a separate obligation. Wider capstone provenance and manual reviews remain open.

## RK4 stage and adaptive trial range — V-80

[Section 19.6 RK4 range](chapter-19-rk4-range-followup.md) preserves 15 baseline mismatches, an intermediate half-step failure and a 23-case pass. It checks actual callbacks and fixed/adaptive consumers plus controlled adaptive acceptance and controller inputs. Finite complete stages, states, error and tolerance ratios are retained; an unrepresentable equal half-step split is reported without callbacks. This adds selected COV-82 evidence. Thirty-five selected COV categories are partially addressed; none closed.

[V-80](runtime-refresh-2026-11-05-r22.md) compiled 545 files, passed 332 scripts and matched 546 required blobs before and after at `eaed8250b3400bedc612aa415c3cecb8f23b2af5`. Chapter 19: 42 compiled files and 32 passing scripts. Independent review, supported platforms and release approval remain pending.

Next substantive item: [Fixed RK4 horizon baseline](chapter-19-rk4-fixed-grid-baseline.md) reproduces two fixed-grid false completed results, one beyond and one short of the reported horizon. Check representable grid alignment against independently derived constant-derivative balances and callback times. Wider floating-time behavior, capstone provenance and manual reviews remain open.

## Fixed RK4 horizon alignment — V-81

[Fixed RK4 grid correction](chapter-19-rk4-fixed-grid-followup.md) preserves nine baseline mismatches and a 19-case pass. The fixed solver integrates adjacent rounded endpoints, reaches the requested horizon and rejects collapsed grids before callbacks. Actual traces and independently derived balances cover overshoot, undershoot, ordinary non-dyadic grids and constant, linear and quadratic slopes. This adds selected COV-82 evidence. Thirty-five selected COV categories are partially addressed; none closed.

[V-81](runtime-refresh-2026-11-05-r23.md) compiled 546 files, passed 333 scripts and matched 547 required blobs before and after at `22336bded4cb65dce8a0557561e7095978fd403f`. Chapter 19: 43 compiled files and 33 passing scripts. Independent review, supported platforms and release approval remain pending.

Next substantive item: [Adaptive RK4 clock baseline](chapter-19-rk4-adaptive-grid-baseline.md) reproduces a state/time discrepancy when the proposed interval and represented time advance differ, even with an equal representable split in step-length arithmetic. Check common full and doubled endpoints, elapsed state and explicit resolution failures; preserve controller and evaluation-count behavior. Wider capstone provenance and manual reviews remain open.

## Adaptive RK4 clock alignment — V-82

[Adaptive RK4 clock correction](chapter-19-rk4-adaptive-clock-followup.md) retains eight baseline mismatches and a 21-case pass. The two trial paths use a common represented endpoint and the same elapsed interval. Near-ulp, no-progress, midpoint collapse and clipped final intervals are checked using real derivative callbacks and independently derived balances. Existing acceptance/rejection and range checks pass. This adds selected COV-82 evidence. Thirty-five selected COV categories are partially addressed; none closed.

[V-82](runtime-refresh-2026-11-06-r01.md) compiled 547 files, passed 334 scripts and matched 548 required blobs before and after at `f462da2d7ff63750780e72884557ccfd4fa7df98`. Chapter 19: 44 compiled files and 34 passing scripts. Independent review, supported platforms and release approval remain pending.

Next substantive item: [Section 19.6 account reference baseline](chapter-19-rk4-account-reference-baseline.md) reproduces three finite-result failures in the benchmark used by the Section 19.6 assessment. Check complete balances and actual assessment fields against independent references; reconcile true range failures with this helper’s contract. Wider capstone provenance and manual reviews remain open.

## Analytical account reference range — V-83

[Section 19.6 analytical account reference](chapter-19-rk4-account-reference-followup.md) retains 13 baseline mismatches, intermediate failures and a 28-case pass. It exercises the actual Section 19.6 assessment, complete balance arithmetic, signed underflow and Section 19.8’s stricter contract. This adds selected COV-84 evidence. Thirty-five selected COV categories are partially addressed; none closed.

[V-83](runtime-refresh-2026-11-06-r02.md) compiled 548 files, passed 335 scripts and matched 549 required blobs before and after at `b5ed61885fc661feb72e9c27c8eb9f9ae220fecd`. Chapter 19: 45 compiled files and 35 passing scripts. Independent review, supported platforms and release approval remain pending.

Next substantive item: [Section 19.5 Euler range and grid baseline](chapter-19-euler-range-grid-baseline.md) records a false Euler overflow, horizon overshoot and callbacks at zero horizon. Validate the distinct Euler driver against independent complete updates and represented time grids, and reconcile its step metadata. Wider capstone provenance and manual reviews remain open.

## Euler complete updates and represented time grid — V-84

[Section 19.5 Euler range and grid](chapter-19-euler-range-grid-followup.md) retains 13 baseline mismatches (including newly specified metadata) and a 21-case pass. It checks complete updates, independently derived represented endpoints, derivative calls and interval metadata. Existing Euler stability and convergence checks pass. This adds selected COV-84 evidence. Thirty-five selected COV categories are partially addressed; none closed.

[V-84](runtime-refresh-2026-11-06-r03.md) compiled 549 files, passed 336 scripts and matched 550 required blobs before and after at `c7fb27159683d94cdf41aa1f6bd8a1cb6e5bd946`. Chapter 19: 46 compiled files and 36 passing scripts. Independent review, supported platforms and release approval remain pending.

Next substantive item: [Euler amplification boundary baseline](chapter-19-euler-amplification-boundary-baseline.md) reproduces three discrepancies at the strict stability or cancellation boundaries. Verify complete-factor rounding separately from the exact classification and observed rounded trajectories. Wider capstone provenance and manual reviews remain open.

## Euler analytical boundaries — V-85

[Euler analytical boundaries](chapter-19-euler-analytical-boundary-followup.md) retains eight baseline mismatches and a 34-case pass. It checks exact stability separately from the rounded factor and observed Euler paths, and verifies the complete account benchmark and actual assessment fields. Existing Euler checks pass. This adds selected COV-84 evidence. Thirty-five selected COV categories are partially addressed; none closed.

[V-85](runtime-refresh-2026-11-06-r04.md) compiled 550 files, passed 337 scripts and matched 551 required blobs before and after at `5621a516346213dd09780c0eba7c49a402aee143`. Chapter 19: 47 compiled files and 37 passing scripts. Independent review, supported platforms and release approval remain pending.

Next substantive item: [Section 19.9 event order baseline](chapter-19-project-event-order-boundary-baseline.md) reproduces two deposits skipped because the rounded depletion time matched the jump time, although the deposits occurred strictly earlier. Verify ordering before timestamp rounding, keeping the exact-equality and time-zero policies, with actual event logs and independent zero- and nonzero-rate references. Wider capstone provenance and manual reviews remain open.

## Depletion and jump ordering — V-86

[Section 19.9 event ordering](chapter-19-project-event-order-followup.md) retains seven baseline mismatches and an 11-scenario pass. It checks event order before timestamp rounding, exact represented elapsed intervals, both time-zero and coincidence policies, and actual statuses, balances and event logs. This adds selected COV-83 evidence. Thirty-five selected COV categories are partially addressed; none closed.

[V-86](runtime-refresh-2026-11-06-r05.md) compiled 551 files, passed 338 scripts and matched 552 required blobs before and after at `ab4dfb16846ebe7dff9867b9a0864870d7893f0f`. Chapter 19: 48 compiled files and 38 passing scripts. Independent review, supported platforms and release approval remain pending.

Next substantive item: [Section 19.7 terminal jump and interpolation baseline](chapter-19-jump-policy-crossing-baseline.md) reproduces a strictly later deposit that incorrectly rescues a terminal simulation and a finite interpolation rejected by intermediate overflow. Verify actual terminal and nonterminal behavior, keeping Section 19.7's distinct exact-tie policy. Wider capstone provenance and manual reviews remain open.

## Terminal jump ordering and interpolation — V-87

[Section 19.7 terminal jump and interpolation](chapter-19-jump-policy-crossing-followup.md) retains seven baseline mismatches and a 17-case pass. It checks event order before timestamp rounding, exact represented elapsed intervals, exact-coincidence and time-zero rescue, signed nonterminal continuation, and finite crossing interpolation. Section 19.9’s distinct depletion-first tie policy is unchanged. This adds selected COV-83 evidence. Thirty-five selected COV categories are partially addressed; none closed.

[V-87](runtime-refresh-2026-11-06-r06.md) compiled 552 files, passed 339 scripts and matched 553 required blobs before and after at `f8e663fe51f1105dff594e5219320214076bafa8`. Chapter 19: 49 compiled files and 39 passing scripts. Independent review, supported platforms and release approval remain pending.

Next substantive item: [Section 19.7 standalone depletion baseline](chapter-19-standalone-depletion-boundary-baseline.md) reproduces a false no-crossing classification and infinity from the standalone Section 19.7 helper. Check the exact threshold, finite range and actual assessment fields. Wider capstone provenance and manual reviews remain open.

## Standalone depletion and equilibrium transition follow-ups — V-88–V-89

[Section 19.7 standalone depletion](chapter-19-standalone-depletion-boundary-followup.md) retains five baseline mismatches and a 24-case pass for the threshold, time range and actual assessment. The simulator policy is unchanged. [V-88](runtime-refresh-2026-11-06-r07.md) recorded 553 compiled files, 340 passing scripts and 554 required blobs verified. Its manifest was re-fetched and matched the starting main tree. This adds selected COV-83 evidence.

[Section 19.4 transition range](chapter-19-equilibrium-transition-range-followup.md) retains nine baseline mismatches and a 22-case pass against independent mean-reversion, reciprocal logistic and half-life references, including the actual assessment. This adds selected COV-84 evidence. Thirty-five selected categories remain partially addressed; none closed.

[V-89](runtime-refresh-2026-11-06-r08.md) compiled 554 files, passed 341 scripts and matched 555 required blobs before and after at `2dccee14e57ace03c2fc58a3226ff7d4d19fc7d5`. Chapter 19: 51 files and 41 passing scripts. Independent review, supported platforms and release approval remain pending.

Next: [Section 19.3 applied range baseline](chapter-19-linear-applied-range-baseline.md) records three finite results rejected by the actual Section 19.3 variable-rate, piecewise and Euler entry points. Check complete exponents, ordered segment balances and whole Euler updates. Wider capstone provenance and manual reviews remain open.

## Applied linear-account follow-up — V-90

[Section 19.3 applied range follow-up](chapter-19-linear-applied-range-followup.md) retains 12 baseline mismatches, an identical replay and a 27-case corrected pass. Independent references cover complete exponents, ordered segment states, affine Euler updates and actual assessment fields. This adds selected COV-84 evidence. Thirty-five selected categories remain partially addressed; none closed.

[V-90](runtime-refresh-2026-11-06-r09.md) compiled 555 files, passed 342 scripts and matched 556 required blobs before and after at `bf9d4fccf807a1ee631a737cb4b20e507808e0cc`. Chapter 19: 52 compiled files and 42 passing scripts. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [Section 19.1 introductory model baseline](chapter-19-introductory-range-baseline.md) records finite growth, equilibrium and Euler failures, a rate endpoint boundary and an assessment output gap. Resume with independently derived expected results and reconcile the rate policy with Section 19.1. Wider capstone provenance and manual reviews remain open.

## Introductory account range and assessment — V-91

[Section 19.1 range and assessment](chapter-19-introductory-range-followup.md) retains 21 baseline mismatches, an identical replay, one intermediate signed-zero mismatch, and a 39-case final pass. This adds selected COV-84 evidence for complete balances, the effective-rate endpoint and actual Euler error fields. Thirty-five selected categories remain partially addressed; none are closed.

[V-91](runtime-refresh-2026-11-06-r10.md) compiled 556 Python files, passed 343 scripts and verified 557 required blobs before and after at `b8d9ad694136393a36aca2c06d9c0798062cb21c`. Chapter 19: 53 compiled files and 43 passing scripts. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [Section 20.7 execution provenance baseline](chapter-20-execution-provenance-baseline.md) starts the outstanding COV-86 checks for actual source, environment, command and output provenance. The synthetic example’s pending fields are verified and intentional. Wider Chapter 19 capstone provenance and manual reviews remain open.

## Actual execution provenance — V-92

[Section 20.7 actual provenance](chapter-20-execution-provenance-followup.md) records an actual local child execution, observed Git source state, interpreter and argv, input hash, output and result. All 21 expanded cases passed; the baseline's 20 missing-behavior observations and initial reruns are retained. The original synthetic template still records pending execution. This adds selected COV-86 evidence. Thirty-five selected categories remain partially addressed; none are closed.

[V-92](runtime-refresh-2026-11-06-r11.md) compiled 557 files, passed 344 scripts and verified 558 required blobs before and after at `641c6ad0304d242fd3a780b12908726b4778d724`. Chapter 20: 34 compiled files and 23 passing scripts. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [Section 20.7 interrupted-write baseline](chapter-20-manifest-interrupted-write-baseline.md) reproduces a partial final JSON artifact and blocked retry after an injected write error. Check publication and no-overwrite behavior separately from durability and authenticity. Wider capstone provenance and manual reviews remain open.

## Complete manifest publication — V-93

[Section 20.7 manifest publication](chapter-20-manifest-publication-followup.md) retains seven baseline mismatches and ten passing corrected observations. Injected write and close failures leave the final path available for retry; competing writers retain a single complete document. This adds selected COV-86 evidence for local visibility and no replacement. Durability, authenticity and wider platform behavior remain open. Thirty-five selected categories remain partially addressed; none are closed.

[V-93](runtime-refresh-2026-11-06-r12.md) compiled 558 files, passed 345 scripts and verified 559 required blobs before and after at `7b2430e2a88336993306dd6b1394ee250cb357e2`. Chapter 20: 35 compiled files and 24 passing scripts. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [Chapter 21 integrated execution baseline](chapter-21-integrated-provenance-baseline.md) records actual deterministic CLI output. Check an external run record binding command, dependency source bytes and stdout under COV-88, while keeping the teaching payload's pending fields. Wider capstone requirements and manual reviews remain open.

## Integrated capstone execution evidence — V-94

[Chapter 21 integrated run receipt](chapter-21-integrated-provenance-followup.md) records actual Section 21.9 CLI bytes, source hashes, command and exit. All ten checks passed, including changed-source and altered-output detection and a retained real import failure. The report itself remains unchanged and retains pending status. This adds selected COV-88 evidence. Thirty-five selected categories remain partially addressed; none are closed.

[V-94](runtime-refresh-2026-11-06-r13.md) compiled 559 files, passed 346 scripts and verified 560 required blobs before and after at `44c6a0bcd5d5e8e6ab8ac84e9691c89610d3ed3e`. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [Section 21.4 central-difference baseline](chapter-21-central-difference-range-baseline.md) reproduces two finite complete stencil values rejected by the actual helper. Check COV-90 centered-difference arithmetic, existing perturbation guards and the actual integrated diagnostic. Wider capstone requirements and manual reviews remain open.

## Complete central-difference evaluation — V-95

[Section 21.4 complete central difference](chapter-21-central-difference-range-followup.md) retains 14 baseline mismatches, an identical replay, and a 24-case corrected pass including the actual integrated diagnostic. The 14-method existing regression passes with the former denominator-rejection test replaced by an independent finite-result reference. This adds selected COV-90 evidence. Thirty-five selected categories remain partially addressed; none are closed.

[V-95](runtime-refresh-2026-11-07-r01.md) compiled 560 files, passed 347 scripts and verified 561 required blobs before and after at `a3f898d3824e5287da47129b18f58d6ec16af05b`. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [Implemented-interface baseline](chapter-21-implemented-interface-baseline.md) records actual callable signatures and report fields versus the intentional design catalog. Reconcile the implemented COV-88 contract without claiming that the draft's general interfaces already exist. Wider capstone requirements and manual reviews remain open.

## Implemented versus planned interfaces — V-96

[Implemented-interface reconciliation](chapter-21-implemented-interface-followup.md) retains eleven missing-map baseline observations, an identical replay, and 26 passing actual interface checks. Seven selected entry points are described separately from the unchanged six-area draft. This adds selected COV-88 evidence; it does not count reused numerical examples as new coverage. Thirty-five selected categories remain partially addressed; none are closed.

[V-96](runtime-refresh-2026-11-07-r02.md) compiled 561 files, passed 348 scripts and verified 562 required blobs before and after at `00fd462aa3a0da15d5babd6c26dc6e49c072e425`. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [CF-04 splitting-property baseline](chapter-21-splitting-property-baseline.md) records subnormal rounding and individual-term overflow boundaries for the plan's same-date splitting claim. Reconcile its acceptance domain and tolerance with the implemented aggregation policy. Wider capstone requirements and manual reviews remain open.

## Cash-flow splitting acceptance — V-97

[CF-04 acceptance reconciliation](chapter-21-splitting-property-followup.md) specifies the represented-amount identity, finite-term domain and rounding comparison for CF-04. All 23 final checks passed; the two missing-policy baseline observations, exact replay and initial checker-assumption correction are retained. The valuation aggregation policy is unchanged. This adds selected COV-88 evidence. Thirty-five selected categories remain partially addressed; none are closed.

[V-97](runtime-refresh-2026-11-07-r03.md) compiled 562 files, passed 349 scripts and verified 563 required blobs before and after at `12de5ae82ef9155593bf2b97ebfd034524bef0b5`. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [INT-01 equivalent-factor baseline](chapter-21-equivalent-factor-property-baseline.md) records two finite long-horizon discrepancies after rounded rate conversion. Specify INT-01 acceptance using independently derived conversion-error propagation and convention references. Wider capstone requirements and manual reviews remain open.

## Equivalent-rate factor acceptance — V-98

[INT-01 factor acceptance](chapter-21-equivalent-factor-property-followup.md) specifies finite positive factors and conversion-error propagation for INT-01. All 33 checks passed, with two baseline policy gaps and an identical replay retained. Conversion and valuation implementations remain unchanged. This adds selected COV-88 evidence. Thirty-five selected categories remain partially addressed; none are closed.

[V-98](runtime-refresh-2026-11-07-r04.md) compiled 563 files, passed 350 scripts and verified 564 required blobs before and after at `2a87994b660c5ea1f600a9187edf097d3ca70dce`. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [Section 8.1 earlier-helper baseline](chapter-08-earlier-derivative-guards-baseline.md) addresses the register's COV-51 earlier copies: Section 8.1 invokes callbacks on collapsed perturbations and returns an infinite estimate from finite samples. Check actual callback/preflight and complete-stencil range behavior without repeating Section 8.8 cases as new coverage. Other capstone requirements and manual reviews remain open.

## Earlier derivative-helper guards — V-99

[Section 8.1 earlier-helper follow-up](chapter-08-earlier-derivative-guards-followup.md) retains ten baseline mismatches, an identical replay, an initial checker serialization failure and 25 passing corrected cases. Section 8.1 now preflights represented perturbations before callbacks and evaluates complete sampled quotients before final rounding. This adds selected COV-51 evidence. Thirty-five selected categories remain partially addressed; none are closed.

[V-99](runtime-refresh-2026-11-07-r05.md) compiled 564 files, passed 351 scripts and verified 565 required blobs before and after at `d702d2761735c11ab501900c899cae4557742a09`. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [Section 8.3 product/quotient baseline](chapter-08-product-quotient-range-baseline.md) records finite analytic product/quotient derivative results lost to intermediate overflow. Check complete expressions, callbacks and true final range without attributing completed sampled-stencil cases to those separate helpers. Remaining financial-PV and copied-helper ranges and manual review remain open.

## Complete product and quotient derivatives — V-100

[Section 8.3 analytic derivative follow-up](chapter-08-product-quotient-range-followup.md) retains eleven baseline mismatches, an identical replay and 34 passing corrected observations. Exact local-series references check complete results while actual callback traces check validation, order and single evaluation. The existing Section 8.3 suite passes. This adds selected COV-51 evidence. Thirty-five selected categories remain partially addressed; none are closed.

[V-100](runtime-refresh-2026-11-07-r06.md) compiled 565 files, passed 352 scripts and verified 566 required blobs before and after at `2f6b47559fc7baa82e59772bbdfbd6445e5374e1`. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [Section 8.3 financial rational baseline](chapter-08-financial-rational-range-baseline.md) records finite average-cost and coverage-derivative results lost to separate float terms. Reconcile complete rational-expression ranges and denominator-domain guards for the financial examples. Discounted-payment and copied finite-difference helpers and manual review remain open.

## Financial rational-expression range — V-101

[Section 8.3 financial rational follow-up](chapter-08-financial-rational-range-followup.md) retains eleven baseline mismatches, an identical replay and 41 passing corrected observations. Complete polynomial-quotient references check finite results, true range failures and adjacent-pole behavior; the exact represented coverage denominator is documented separately from its financial interpretation. The existing Section 8.3 suite passes. This adds selected COV-51 evidence. Thirty-five selected categories remain partially addressed; none are closed.

[V-101](runtime-refresh-2026-11-07-r07.md) compiled 566 files, passed 353 scripts and verified 567 required blobs before and after at `e674373645a4b9787b3a412fd8262ff9a4c30fdf`. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [Discounted-payment baseline](chapter-08-discounted-payment-range-baseline.md) records finite/zero values and a finite derivative lost to separate exponential/coefficient arithmetic. Check actual payment callbacks and complete scaling; preserve the value wrapper's unused derivative-argument behavior. Copied finite-difference and Section 8.1 financial helpers and manual review remain open.

## Discounted-payment callback range — V-102

[Section 8.3 discounted-payment follow-up](chapter-08-discounted-payment-range-followup.md) retains eleven expanded baseline mismatches, an identical replay, earlier screen/rerun and 32 passing final cases. Independent separate discounted-term references check complete coefficient scaling, zero/cancelled identities, genuine final overflow and actual callback arguments/order. The existing Section 8.3 suite passes. This adds selected COV-51 evidence. Thirty-five selected categories remain partially addressed; none are closed.

[V-102](runtime-refresh-2026-11-07-r08.md) compiled 567 files, passed 354 scripts and verified 568 required blobs before and after at `0b109a17f2ee256a3cdffeeeffb0417720bcf3ed`. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [Section 8.1 initial-PV baseline](chapter-08-initial-pv-range-baseline.md) records finite PV/derivative/stable-quotient results lost to premature underflow in Section 8.1's distinct financial functions. Preserve their domains and derive complete references. The copied Section 8.3 centered difference and other early derivative helpers and manual review remain open.

## V-103 checkpoint — 2026-11-07

[Section 8.1 financial range](chapter-08-initial-pv-range-followup.md): forty corrected checks pass; seventeen baseline mismatches and valid baseline replay retained. [Section 8.3 centered wrapper](chapter-08-centered-copy-followup.md): eight checks pass; six baseline observations retained, including two new delegation requirements. The invalid missing-directory replay setup and corrected harness are disclosed separately.

[V-103](runtime-refresh-2026-11-07-r09.md) at `a6441d707337946a76e059c6cf53a5b05291afa0`: 569 Python files compiled, 356 scripts passed, 570 required source/fixture hashes verified before/after. Counts derive from this pinned tree. Thirty-five selected COV categories remain partial, none closed; this is not a completion percentage or independent sign-off.

Next substantive work: [Section 8.2 polynomial range baseline](chapter-08-polynomial-range-baseline.md), including two confirmed finite-result failures and the remaining centered-difference copy. Resume there without repeating completed Section 8.1 financial or Section 8.3 wrapper examples. Reviewer, supported-platform, release and canonical decisions remain pending.

## V-104 checkpoint — Section 8.2

[Polynomial and centered-copy follow-up](chapter-08-polynomial-range-followup.md): 64 checks pass, with 22 baseline mismatches and a byte-identical replay retained. Exact power-sum references independently check rational Horner evaluation and point-specific derivatives; the coefficient API rejects unrepresentable outputs and the centered wrapper uses the guarded Section 8.1 helper. Initial checker serialization failure and reruns are disclosed. Existing Section 8.2 reference checks also pass.

[V-104](runtime-refresh-2026-11-07-r10.md) at `78b09101177563c3511c1932f6a4e7469567e7bc`: 570 files compiled, 357 scripts passed, 571 required hashes verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer sign-off, supported platforms, release acceptance and canonical approval remain pending.

Next substantive obligation: [Section 8.2 financial cost-output baseline](chapter-08-cost-output-baseline.md), where a finite accepted quantity returns infinity. Derive complete financial references and establish the finite-output contract; do not repeat the completed polynomial or centered-copy corpus.

## V-105 checkpoint — Section 8.2 cost output

[Cost-output follow-up](chapter-08-cost-output-followup.md) retains four baseline mismatches and an identical replay; all 50 corrected checks pass. Thirty-two independent Decimal value/derivative references establish complete-expression rounding, twelve guard checks preserve quantity domains, and six composition regressions preserve profit call relationships. Three returned infinities now raise OverflowError; one one-ulp difference is reconciled under the explicit new rounding policy. No marginal-cost baseline failure is claimed. Existing Section 8.2 and polynomial-range suites pass.

[V-105](runtime-refresh-2026-11-07-r11.md) at `7db1525c2f390b0eb9afa431c08648b6450737d3`: 571 files compiled, 358 scripts passed, 572 required blobs verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [Section 8.4 callback and centered-copy baseline](chapter-08-chain-callback-baseline.md). Actual probes retain a nonfinite chain product, an identity quotient yielding NaN instead of 1, and collapsed perturbations that still invoke callbacks. Preserve callback order/count and derive full sampled quotient/error contracts; do not repeat completed Section 8.2 cost/polynomial examples.

## V-106 checkpoint — Section 8.4 callback and centered copy

[Chain callback follow-up](chapter-08-chain-callback-followup.md): all 55 checks pass; ten baseline mismatches and an identical original-source replay retained. Independent Decimal products and exact sampled quotient references check actual Section 8.4 calls. Callback arguments/order/counts, short circuit, exception identity, signed zero/underflow, default step and callable-before-controls precedence are checked. Nonfinite final chain products reject and invalid perturbations reject before callbacks. The existing Section 8.4 suite also passes.

[V-106](runtime-refresh-2026-11-07-r12.md) at `9d138bf2bd1fa0ab5806d0ec3e9202b0f26f2cf1`: 572 files compiled, 359 scripts passed, 573 required blobs verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [Section 8.4 variable-rate PV baseline](chapter-08-variable-rate-pv-baseline.md). Actual probes lose finite complete PV/sensitivity results to underflow and return NaN for zero amount. Independent 200/400-digit references agree for the returned represented rate. Establish complete scaling and zero identities while preserving the intended factor-rate convention; do not repeat completed callback/centered-copy examples.

## V-107 checkpoint — Section 8.4 variable-rate PV

[Variable-rate PV follow-up](chapter-08-variable-rate-pv-followup.md): all 63 checks pass; sixteen baseline mismatches, an identical replay and corrected rerun retained. Independent 1800/2400-digit log-scale references check complete coefficients/exponents, zero identities and finite sensitivity recovery when PV rounds to zero. Six independently rounded affine-rate cases preserve the public rate convention. Input domains, signed zeros and validation precedence remain checked. The strengthened validation-priority discriminator did not change observation JSON. Existing Section 8.4 and callback suites also pass.

[V-107](runtime-refresh-2026-11-07-r13.md) at `21ebbc28a1b08b93c9103d791c90d6bab15ec815`: 573 files compiled, 360 scripts passed, 574 required blobs verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [Section 8.4 discrete-compounding baseline](chapter-08-discrete-compounding-range-baseline.md), with [three retained value/sensitivity probe pairs](chapter-08-discrete-compounding-range-baseline.json). Actual intermediate overflow/underflow loses finite complete values and zero-principal identities. Preserve the intended nominal-rate/base/exponent conventions while deriving full results; do not repeat completed variable-rate PV examples.

## V-108 checkpoint — Section 8.4 discrete compounding

[Discrete-compounding follow-up](chapter-08-discrete-compounding-range-followup.md): all 74 expanded checks pass; sixteen expanded baseline mismatches and a byte-identical replay retained. The initial 69-case baseline/corrected run is also retained. Exact rational integer powers and independent Decimal direct powers at 1600/2200 digits check complete values/sensitivities. Selected rounded bases, exact n·t and n·t−1 behavior near 2^53, signed zero identities, final output/error policy and invalid base/count/quantity behavior are checked. Existing Section 8.4 and variable-rate PV suites pass.

[V-108](runtime-refresh-2026-11-07-r14.md) at `df9ac9bf2952edc78ec5264a25d7caf7f90a21e5`: 574 files compiled, 361 scripts passed, 575 required blobs verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [large integer period-count baseline](chapter-08-large-period-count-baseline.md), with [three retained value/sensitivity probe pairs](chapter-08-large-period-count-baseline.json). Count 10**400 is accepted by the positive-integer guard but base division raises OverflowError despite finite rounded-base expectations. Extend conversion while preserving already working base conventions; do not repeat completed power-scaling examples.

## V-109 checkpoint — Section 8.4 large period counts

[Large-count follow-up](chapter-08-large-period-count-followup.md): all 78 checks pass; forty-two baseline observations and a byte-identical replay retained. Fourteen base/value/sensitivity triples fail at the same original conversion point; this is not forty-two distinct defects. Independent Decimal count conversion and direct powers at 1600/2200 digits check conversion thresholds, huge counts with nonzero quotients and working 2^53+1 denominator rounding. The fallback is used only when float/int division overflows. Existing Section 8.4 and 74-case compounding suites pass.

[V-109](runtime-refresh-2026-11-07-r15.md) at `a93acb89609087281b4e1872c6420313ddf7adca`: 575 files compiled, 362 scripts passed, 576 required blobs verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [nested-power range baseline](chapter-08-nested-power-range-baseline.md), with [five exact-polynomial/actual probe pairs](chapter-08-nested-power-range-baseline.json). Actual finite outputs differ from one-rounding references and nonfinite outputs/errors are inconsistent; establish the accuracy/overflow contract before editing. Price/log-growth, other earlier copies and independent review remain open. Do not repeat completed count-conversion or compounding examples.

## V-110 checkpoint — Section 8.4 nested-power derivative

[Nested-power follow-up](chapter-08-nested-power-range-followup.md): all 45 checks pass; seventeen baseline mismatches and an identical replay retained. Independent expanded rational monomials check a factored rational implementation with one final rounding. An oracle-only monotone float-bit search finds adjacent finite/overflow inputs; both signs, tiny values, seeded magnitudes and type/domain guards are checked. Six baseline infinities now raise OverflowError; eleven finite differences are reconciled under the explicit accuracy contract. Existing Section 8.4 and 78-case large-count suites pass.

[V-110](runtime-refresh-2026-11-07-r16.md) at `76208b8f944cf6ab706ae75f94cc0329d1f3dbfe`: 576 files compiled, 363 scripts passed, 577 required blobs verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [price/log-growth baseline](chapter-08-price-log-growth-baseline.md), with [five retained probe pairs](chapter-08-price-log-growth-baseline.json). Price returns infinity at 1e104 while larger unrepresentable cases raise OverflowError; selected log-growth outputs match their represented-ratio references. Establish price output/accuracy consistency and preserve or explicitly reconcile the rounded base and represented coefficient convention. Do not repeat completed nested-power/count examples.

## V-111 checkpoint — Section 8.4 price/log-growth contracts

[Price/log-growth follow-up](chapter-08-price-log-growth-followup.md): all 62 checks pass; nine baseline price mismatches and an identical replay retained. Two returned infinities now raise OverflowError; seven finite differences are reconciled under the explicit complete-cubic rounding contract. Independent two-stage affine bases, exact Decimal cubic products, rational growth ratios and an oracle-only adjacent price boundary search preserve existing represented-base semantics. Log-growth code is unchanged; its endpoint/monotonicity finite-output argument states binary64 rounding assumptions. Existing Section 8.4 and nested-power suites pass.

[V-111](runtime-refresh-2026-11-07-r17.md) at `99ef9ddc1fab5e20ca83df6254d639720ff23b36`: 577 files compiled, 364 scripts passed, 578 required blobs verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [Section 8.5 exponential-derivative baseline](chapter-08-exponential-derivative-range-baseline.md), with [four retained probes](chapter-08-exponential-derivative-range-baseline.json). Separate coefficient/exponential arithmetic loses finite signed results and zero-scale identities. Establish complete represented-input scaling and final output/error conventions while preserving type/domain behavior; other Section 8.5 helper/copy and independent review obligations remain open. Do not repeat completed Section 8.4 price/nested-power examples.

## V-112 checkpoint — Section 8.5 exponential derivative

[Exponential-derivative follow-up](chapter-08-exponential-derivative-range-followup.md): all 34 checks pass; fourteen baseline mismatches and a byte-identical replay retained. Independent log-amplitude references at 1600/2200 digits and exact special cases check complete coefficient/exponent scaling, signed zeros, tiny inputs and true final overflow. One ordinary rounding difference is reconciled under the explicit complete-expression contract. Zero-sign flags and raw stdout hashes preserve sign details across JSON serialization. Existing Section 8.5 checks pass.

[V-112](runtime-refresh-2026-11-07-r18.md) at `8a23628022d832fbd80422aaf6ca582b28917de6`: 578 files compiled, 365 scripts passed, 579 required blobs verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [logarithm-derivative baseline](chapter-08-logarithm-derivative-range-baseline.md), with [four retained probes](chapter-08-logarithm-derivative-range-baseline.json). Three positive-argument examples lose finite complete ratios; a cancellation-domain example requires explicit reconciliation of exact represented versus rounded argument policies. Derive signed/zero/overflow quotient expectations and preserve validation behavior. Other Section 8.5 financial and copied-helper obligations remain open. Do not repeat completed exponential-derivative or Section 8.4 examples.
