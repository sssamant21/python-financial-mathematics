# Book 02 — Remaining Review and Release Checklist

**Date:** 2026-10-30  
**Full-runtime candidate source revision:** `54c73a8f98043676edad54efc5725e80f4af883c`  
**Latest scoped source revision:** `015137295af393e4f1783474fc1d24a7cb1c1c7b`  
**Disposition:** Earlier V-50 full candidate runtime plus subsequent final-study integration scoped evidence; independent review and release approval pending.

## Reconciled evidence

[V-50 nineteenth refresh](runtime-refresh-2026-10-30-r14.md):489 compiled,278 scripts passed,490 required hashes verified before/after. Includes the project-error checker and final solver/curve integration/checker. Current candidate execution; G2–G8 unchanged.

[V-49 eighteenth refresh](runtime-refresh-2026-10-30-r13.md):487 compiled,276 scripts passed,488 required hashes verified before/after. Includes complete-stencil corrections and all three recent Chapter18 checkers. Current candidate execution; G2–G8 unchanged.

[V-48 seventeenth refresh](runtime-refresh-2026-10-30-r12.md):484 compiled,273 scripts passed,485 required hashes verified before/after. Includes Section18.5 root-scan correction/checker and Section18.9 trace checker. Current candidate execution; G2–G8 unchanged.

[V-47 sixteenth refresh](runtime-refresh-2026-10-30-r11.md): 482 sources compiled, 271 scripts passed, 483 required hashes verified before/after. Includes Section17.9 report and Section17.10 LP integration with both checkers. Current candidate execution; G2–G8 unchanged.

[V-46 fifteenth refresh](runtime-refresh-2026-10-30-r10.md) includes the Section17.4 boundary correction and degenerate-multiplier checker: 480 files compiled, 269 scripts passed, 481 required hashes verified before/after. Current candidate execution; G2–G8 unchanged.

[V-45 fourteenth refresh](runtime-refresh-2026-10-30-r9.md) includes normalized-loss corrections and the rank-deficient lab with two checkers: 478 files compiled, 267 scripts passed, 479 required hashes verified before/after. Latest candidate execution; G2–G8 unchanged. Earlier records below are historical.

[V-44 thirteenth refresh](runtime-refresh-2026-10-30-r8.md) includes Section16.10 candidate assessment and distinct exercise objectives with two checkers: 476 files compiled, 265 scripts passed, 477 required hashes verified before/after. Historical candidate execution; G2–G8 unchanged. Earlier records below are historical.

[V-43 twelfth refresh](runtime-refresh-2026-10-30-r7.md) includes raw-price and normalized calibration changes and two checkers: 474 files compiled, 263 scripts passed, 475 required hashes verified before/after. Historical candidate execution; G2–G8 unchanged. Earlier records below are historical.

[V-42 eleventh refresh](runtime-refresh-2026-10-30-r6.md) includes Sections 16.8–16.10 metric changes and two checkers: 472 files compiled, 261 scripts passed, 473 required hashes verified before/after. Historical candidate execution; G2–G8 unchanged. Earlier records below are historical.

[V-41 tenth refresh](runtime-refresh-2026-10-30-r5.md) includes both subsequent Section 16.6 corrections and two checkers: 470 files compiled, 259 scripts passed, 471 required hashes verified before/after. Historical candidate execution; G2–G8 unchanged. Earlier records below are historical.

[V-40 ninth refresh](runtime-refresh-2026-10-30-r4.md) includes the Sections 16.2–16.4 derivative corrections and new checker: 468 files compiled, 257 scripts passed and 469 required hashes verified before/after. Latest candidate execution; G2–G8 unchanged. Earlier records below are historical.

[V-39 eighth refresh](runtime-refresh-2026-10-30-r3.md) includes three subsequent Chapter 16 checkers: 467 sources compiled, 256 scripts passed and 468 required hashes verified before/after. Historical candidate execution; G2–G8 unchanged. Earlier records are historical.

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
| G1 Candidate compilation/runtime | Passed, scoped | V-50 earlier full pin:489 compiled/278 scripts/490 hashes; subsequent final-study integration has29-file/19-script pass at `015137295af393e4f1783474fc1d24a7cb1c1c7b` | Automated run recorded |
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
