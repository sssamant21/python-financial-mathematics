# Chapter 14 — Substantive coverage map

**Date:** 2026-10-28
**Inspected revision:** `f9f0c0e63d5cb2a9c34ecde9cd53e4f961d02532`
**Status:** Ten sections mapped; independent review pending.

Compared 180 worked questions in 14.1–14.9, twenty final exercises, five applied problems and acceptance gates with actual assertions. No new runtime execution. See [historical pinned pass](pinned-revision-runtime-validation.md). Reference cases, a general numerical library, and independent financial review have different scopes.

## Assertion and exercise map

| Section | Actual evidence | Exercise disposition |
|---|---|---|
| 14.1 | [Checks](../chapter-14/code/check_section_14_01.py): eigenvalues 3/1, trace/determinant 4/3, unit eigenvectors, actual Av=lambda-v equations, mutual orthogonality; diagonal/repeated/zero cases; asymmetric/shape/NaN/bool rejection. | E5–10 have direct or sign-invariant eigenpair evidence. E12–13 identities have matching reference numbers, not broad matrices. E16–17 have zero/repeated examples. E1–4, E11, E14–15 and E18–20 require definitions, characteristic/sign/covariance reasoning. A symmetric 2x2 helper does not handle general nonsymmetric spectra. |
| 14.2 | [Checks](../chapter-14/code/check_section_14_02.py): entrywise reconstruction, orthogonality and eigenpair residuals, trace/determinant, product (4,2), quadratic 8; diagonal/repeated/zero/negative examples; asymmetry/Inf/vector-length failures. | E3, E5–6, E11–12 and E14 have direct example evidence. E7–8 eigenvector directions indirectly supported by reconstruction and earlier equation checks; rank-one terms E9–10 and coordinates E13 not individually asserted. E1–2, E4, E15–20 general spectral/economic statements remain manual. Applied numerical reference values are covered. |
| 14.3 | [Checks](../chapter-14/code/check_section_14_03.py): quadratic and polynomial 14, Ax=(5,4), gradient (10,8), Hessian, scaling to 56, eigenbasis quadratic 14; three other symmetric forms; asymmetry/vector/NaN/bool rejection. | E8–10, E13–14, E17–18 direct. E5–7 individual terms and E16 coordinates are not separately asserted. E1–4, E11–12, E15 and E19–20 require symbolic/general review. Nonsymmetric quadratic identity is taught, but helper intentionally requires exact symmetry; this is a restricted API, not a general nonsymmetric implementation. |
| 14.4 | [Checks](../chapter-14/code/check_section_14_04.py): six classification labels including numerical zero, PD/PSD reference eigenvalues, determinant3, PSD/NSD zero-first-pivot cases, small +/- eigenvalues and threshold-induced zero; invalid tolerance/asymmetry/Inf. | E5–7 have example classifications rather than proofs. E8–12 use related matrices with different diagonal values/order; E13 maps to numerically_zero, not two separate PSD/NSD booleans. E15 direct; E16 rank-one PSD supported. E1–4, E14 and E17–20 need definitions/Sylvester/financial/optimizer reasoning. Applied q(2,1)=14 is covered in 14.3, not this classification suite. |
| 14.5 | [Checks](../chapter-14/code/check_section_14_05.py): L entries, LL-transpose entrywise, determinant8, solution(1,1), solve/reconstruction residuals; diagonal solve; PSD/indefinite/asymmetric/zero/NaN/bad RHS rejection. | E4, E6–12 and E15–17 direct or formula-special-case evidence; E19 direct rejection. E1–3, E5, E13–14, E18 and E20 need derivation/triangular/quadratic/covariance interpretation. Forward intermediate solution is returned but not asserted. Only 2x2 systems are supported. |
| 14.6 | [Checks](../chapter-14/code/check_section_14_06.py): diagonal-column singular values3/2, rank2, condition1.5, positions(2,2), achieved(6,4,0), residual(0,0,5), objective12.5; rank-deficient/threshold/zero cases; bad magnitudes/target/tolerance/NaN. | E9–11, E13–17 direct. E12 pseudoinverse is sampled, not a general implementation. E1–8 and E18–20 need SVD shape/directions/conditioning interpretation. U/Sigma/V reconstruction and orthogonality are not asserted here. The helper explicitly supports only nonnegative diagonal-column 3x2 matrices. |
| 14.7 | [Checks](../chapter-14/code/check_section_14_07.py): rank0/1/2 errors, spectral/Frobenius norms, retained energy, rank-one matrix, actual rank; swapped magnitude selection, tie error, zero energy None; bad rank/magnitude/NaN. | E8, E10–13 and E15–16 direct. E9 total squared norm20 is implicit in error/energy values. E14 zero approximation is not independently inspected. E1–7 and E17–20 require definition/optimality/uniqueness/risk review. Applied portfolio exposure-error inequality is not asserted; matrix errors alone do not check it. |
| 14.8 | [Checks](../chapter-14/code/check_section_14_08.py): five near-zero diagnostic fields; singular values/condition, low-rank error/energy, one nonzero Frobenius error and shape/empty/NaN failures. | E2, E4, E6, E8 and E15–18 have reference diagnostic support. E11–14 matrices/factors are embedded constants, not outputs of decomposition solvers in this lab. E1, E3, E5, E7, E9–10 and E19–20 remain definition/interpretation/general validation review. SVD reconstructed matrix is copied from its original literal; zero reconstruction error therefore does not test a computed factorization. |
| 14.9 | [Checks](../chapter-14/code/check_section_14_09.py): weight sum, variance/volatility/gradient, determinant/PD flag, Cholesky entries/reconstruction/recovered weights/residual, singular values/condition, replication/residual/objective, compression errors/energy/lost exposure, pending flags. | E2, E4–11, E13–15 and E17–18 direct. E1 weights are indirectly checked through recovery, not input-field assertions. E3 cross term0.0048 not separately asserted. E12 dimension and E16/E19–20 attainability/model-risk statements remain manual. All sixteen stated numeric acceptance gates have matching reference assertions; no general arbitrary-data project interface is offered. |
| 14.10 | [Checks](../chapter-14/code/check_section_14_10.py): reference eigenvalues/reconstruction, quadratic/gradient/Hessian, determinant, covariance/variance/volatility, Cholesky values/reconstruction, singular values/rank/condition, replication/residual/objective, compression error/energy and pending flags. | E2, E4–7, E9 and E11–19 have direct numeric fields; E14 lower-right entry supported by reconstruction norm, not separately inspected. E1 characteristic polynomial, E3 vector values, E8/E10 definiteness proofs and E20 interpretation remain manual. Several returned answers are hardcoded literals rather than solver calls. Applied A–E are not explicitly exercised: B/C have related earlier classification/rejection cases, D lost-exposure vector is checked in14.9 but its norm bound is not; E condition4e8 is unasserted. |

## Project and numerical scope

The 14.9 project calls actual Cholesky/solve helpers and restricted diagonal SVD/compression helpers. Its fixed covariance calculation independently yields variance and gradient values asserted by the check. It does not accept arbitrary project inputs, label metadata, timestamps or unit declarations. “Reject invalid dimensions/nonfinite inputs” is implemented in the underlying functions and tested in their separate suites, not a project-level data ingestion interface.

The learning outcome asking to verify covariance eigenvalues is not implemented by the project report: definiteness uses the 2x2 principal-minor test; Cholesky is computed; covariance eigenpairs are not reported. This distinction should be reconciled during final revision. Documentation of units, tolerances, provenance and assumptions largely lives in prose/test code; report metadata does not capture all of it.

14.8 and14.10 are deterministic reference calculations, not full solver integrations. Literal eigenvalues, Cholesky factors, rank/condition and compression errors can agree with literal expected answers while a separate solver regresses. Earlier suites mitigate this for selected cases, but aggregate report success cannot replace them.

The SVD helper reports singular values sorted descending while singular directions stay in factor order, as its docstring explicitly states. Consumers must not zip these as matched triples when the second magnitude exceeds the first. No swapped-order reconstruction test is present in14.6 (14.7 separately tests compression selection). Rank thresholding and exact full-column-rank condition are separate fields: a positive singular value below threshold is dropped from positions but may still yield a finite condition number. These conventions require interpretation, not an assumed general SVD contract.

The eigen helper allows small asymmetry relative to max(1,magnitude) and averages the off-diagonal entries; quadratic and Cholesky helpers require exact symmetry. No adjacent symmetry-policy tests establish consistent cross-section semantics. Eigenvalue cancellation for highly unequal spectra, scaled determinant/trace range, near-SPD pivots and relative diagnostic normalization remain open.

## Additional boundary evidence

[Decomposition regressions](../chapter-14/code/check_decomposition_boundaries.py) verify Frobenius errors at1e200/1e-200, 3-4-5, unrepresentable subtraction rejection, one-shot matrix iteration in the Cholesky solve, and malformed iterator shape. See [focused review](chapter-14-decomposition-boundary-review.md). This does not establish large/small range behavior for every duplicate reconstruction norm or retained-energy calculation; several still square raw entries.

## Open gap register

| ID | Gap | Next evidence |
|---|---|---|
| COV-67 | Reference report checks can validate copied matrices or literal factors rather than computed decompositions; restricted diagonal SVD directions and sorted values need explicit consumer conventions. | Keep reference arithmetic distinct from solver integration; verify meaningful reconstruction/orthogonality including swapped singular magnitudes if paired factors are consumed. |
| COV-68 | Near-degenerate eigen/Cholesky and scale/tolerance behavior remains narrow; symmetry policy differs across helpers and raw squared norms remain elsewhere. | Independent scaled/unequal-spectrum and near-pivot benchmarks; review symmetry tolerances and diagnostic units/range. Do not infer full range coverage from the corrected Frobenius helper. |
| COV-69 | Some applied requirements are absent: covariance eigenpairs in project, compression exposure bound, complete report assumptions and additional final problems. | Reconcile project/assessment scope and record manual economic/unit proof review; assert selected missing computations where needed. |

These extend COV-01–COV-66 and overlap prior report/exact-input/shared-oracle categories. No Python or manuscript changes and no runtime execution for this map. Independent review and canonical approval remain pending.

## Subsequent COV-69 remediation — 2026-10-29

The [covariance eigenpair follow-up](chapter-14-covariance-eigenpair-followup.md) adds the promised fixed-covariance eigenpairs to Section 14.9's report and acceptance table. Closed-form eigenvalues, sign-independent projectors, directly recomputed residuals, orthogonality and reconstruction are asserted; four deliberately corrupted reports were detected. All 21 chapter files compiled and all 11 scripts passed. COV-69 remains partially open for compression-bound/report-metadata evidence and independent review. Original mapping statements remain historical.

## Subsequent compression/report follow-up — 2026-10-29

The [compression-bound record](chapter-14-compression-bound-followup.md) adds actual-matrix exposure calculations, the measured error norm and spectral bound, plus fixed-input/unit metadata. Twelve matrix/rank cases check 48 selected actions and attaining coordinate directions. All 21 chapter files compiled and all 11 scripts passed. Selected executable COV-69 obligations are addressed; independent review and broader numerical/interface scope remain open.

## Selected near-repeated spectral follow-up — 2026-10-29

[Section 14.1 evidence](chapter-14-near-repeated-followup.md) partially addresses COV-68 with twelve closed-form value/projector and normalized residual/reconstruction checks. The coordinate-direction fallback below the gap cutoff is explicitly approximate for nonzero off-diagonals. All 22 Chapter 14 files compiled and 12 scripts passed. Broader spectrum/range, symmetry, Cholesky and independent-review obligations remain open. This scoped run follows V-34; twenty-four selected categories are partially addressed.

## Selected near-SPD Cholesky follow-up — 2026-10-29

[Section 14.5 evidence](chapter-14-near-spd-followup.md) extends COV-68 with exact dyadic determinant/pivot references, factor/reconstruction/forward/backward-solve checks and singular/indefinite boundary rejection. All 23 Chapter 14 files compiled and 13 scripts passed. Nondyadic rounding, arbitrary right-hand-side conditioning, broader ranges and independent review remain open. This scoped run follows V-34; twenty-four categories remain partially addressed.

## Selected restricted-SVD ordering follow-up — 2026-10-29

[Section 14.6 evidence](chapter-14-svd-order-followup.md) partially addresses COV-67 with twelve reconstruction, direction-orthonormality, sorted-summary and thresholded-solve cases. Factor-order directions must be paired with original magnitudes, not blindly zipped with the sorted summary. All 24 Chapter 14 files compiled and 14 scripts passed. Reference-report/integration and independent-review scope remains open. This scoped run follows V-34; twenty-five selected categories remain partially addressed.

## Unequal-spectrum correction — 2026-10-29

[Section 14.1 evidence](chapter-14-unequal-spectrum-followup.md) records a confirmed representable-small-eigenvalue cancellation defect, its original regression failure and corrected exact/Decimal references. All 25 Chapter 14 files compiled and 15 scripts passed. This source change follows V-35; a new full-book run is not claimed. COV-68 remains partially open and twenty-five categories remain partially addressed. Next executable item: Section 14.2 duplicate spectral path against the unequal-spectrum references; independent review/platform/release gates remain pending.

## Spectral-report integration and correction — 2026-10-29

[Section 14.2 evidence](chapter-14-spectral-report-followup.md) confirms the shared Section 14.1 solver path and corrects one-shot input reuse and squared-norm underflow. The original checker failure and tiny-error probe are retained; all 26 chapter files compiled and 16 scripts passed after correction. This scoped change follows V-35. Twenty-five categories remain partially addressed. Next executable item: Section 14.1 off-diagonal averaging/symmetry boundary; broader numerical, platform and independent-review gates remain open.
