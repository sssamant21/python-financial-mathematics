# Book 02 — Validation Progress Tracker

**Updated:** 2026-10-30  
**Overall status:** In progress — latest full pinned-revision runtime pass complete (478 compiled files; 267 successful script exits); coverage, independent review and final release/platform validation remain pending.

This tracker records evidence and open work. A passed script is not a validated chapter, an independent review, or canonical approval. Update the evidence and revision whenever a status changes; do not treat a draft, missing result, or an unchecked item as a pass.

## Current evidence

| Workstream | Status | Progress / evidence |
|---|---|---|
| Numbered manuscript inventory | Initial inventory complete | 215/215 section files found across 21 chapters at revision `a20484672beae64e7c61037af0b11baba2fd7e54`; content completeness and index consistency not yet audited. |
| Python compilation | Pinned-revision pass complete | 478/478 files compiled at `0e2f5e4eebc9b3e0328a3bba2c6e0d7f88954db3` on Python 3.12.14/Linux. [Latest evidence](runtime-refresh-2026-10-30-r9.md). |
| Automated script execution | Pinned-revision pass complete | 267/267 check/test scripts exited zero at `0e2f5e4eebc9b3e0328a3bba2c6e0d7f88954db3`. Aggregate scripts repeat checks; counts do not measure independent coverage. [Latest evidence](runtime-refresh-2026-10-30-r9.md). |
| Initial failures | Fixed and rerun locally; independent review pending | Six failed checks were addressed; the follow-up pass returned zero exits. Numerical and cross-platform review remains open. |
| Test coverage and dependencies | Mapping complete; gaps open | Filename mapping covers 215 sections; substantive mapping covers 215/215 sections (all Chapters 1–21), with ninety recorded gap categories and no coverage certification. [4.1–4.6 map](coverage-sections-04-01-06.md) · [4.7–4.8 map](coverage-sections-04-07-08.md). Focused [Chapter 21](chapter-21-capstone-review.md), [Chapter 20](chapter-20-boundary-review.md) [Chapter 19](chapter-19-continuous-time-review.md) and [Chapter 18](chapter-18-solver-boundary-review.md) reviews identified fixes; gap remediation and dependency review remain pending. [All-section coverage index](substantive-coverage-index.md). [Inventory](section-check-inventory.md). |
| Mathematical and numerical review | Pending | Review derivations, examples, solutions, assumptions, error bounds and numerical edge cases, including the six fixes. |
| Links and index consistency | In progress — sampled rendered markup passed | Latest static scan: 270 Markdown files, 2,743 recognized local destinations, zero missing paths; no local fragment destinations or reference definitions detected. Rendered navigation, external scan checked 102 distinct URLs (99 HTTP 200, three 404); MathWorld corrected; Federal Reserve/NIST references subsequently resolved. [Source resolution](source-reference-resolution.md). Section 4.7–4.8 titles/scope reconciled. Six pinned GitHub pages retrieved; 14 rendered-markup navigation checks passed. Browser/visual and full-book navigation remain pending. [Rendered sample](rendered-navigation-sample-review.md). [External audit](external-url-audit.md). [Anchor/reference audit](anchor-reference-link-audit.md) · [Earlier index audit](link-index-audit.md). |
| Editorial, source and copyright review | Pending | Review manuscript quality, attribution and source policy. |
| Final-revision and platform validation | Candidate Linux pass complete; release/platform checks pending | Full candidate snapshot passed on Python 3.12.14/Linux; rerun after relevant review changes and assess supported Python versions and Windows. [Evidence](pinned-revision-runtime-validation.md). |
| Canonical approval | Not granted | Requires documented review, resolved findings and the authorized decision. |

## Latest full-book runtime refresh — V-39

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

- **Latest full run:** [V-39 eighth refresh](runtime-refresh-2026-10-30-r3.md): 467 sources compiled, 256 scripts passed and 468 required hashes verified before/after at `18be350b40cc2a0a963e0c5fd91b793cf0c3c634`.

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
