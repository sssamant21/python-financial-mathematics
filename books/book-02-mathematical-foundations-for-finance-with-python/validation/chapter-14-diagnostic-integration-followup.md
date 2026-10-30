# Chapter 14 — Computed diagnostic integration follow-up

**Date:** 2026-10-29  
**Inspected revision:** `099d3350022df7e636be435a96a96aa18c1eca31`  
**Implementation commit:** `e210fa7da5bc64702fff3df838c79f710f3f3d1a`  
**Implementation blob:** `ed23f00c06f27552a868e51adeb693a91fae4d9f`  
**Disposition:** Selected COV-67 integration gap addressed; category partially open.

## Before and after

Section 14.8 previously constructed eigen/Cholesky reference factors and a literal SVD reconstruction inside its assessment. Its arithmetic was useful as a reference, but a passing report did not demonstrate that the separate decomposition helpers were invoked. The new integration checker fails on that original source because the eigen helper is never called; this is an integration-evidence gap, not proof that the old reference numbers were wrong.

The report now calls the actual eigenpair, Cholesky solve, restricted SVD and restricted low-rank helpers once each. Reconstruction, orthogonality, solve and approximation errors are recomputed from returned factors/directions/solutions/matrices. SVD directions are paired with original factor-order magnitudes rather than blindly with the sorted summary. Existing numeric fields remain, and calculation_source identifies computed_teaching_helpers.

## Independent and injected-failure checks

The existing Section 14.8 checker retains known zero diagnostic references, singular values (3,2), condition 1.5, rank-one error 2 and retained energy 0.8. The [new integration checker](../chapter-14/code/check_diagnostic_integration.py) spies on four actual helper calls and compares diagnostics with those expected values.

Five deliberately corrupted helper outputs are detected: wrong eigenvectors, wrong Cholesky factor, zero solution, wrong SVD direction and zero low-rank approximation. Corruption is scoped with unittest.mock and restored after each case; production code does not contain fault injection. This demonstrates sensitivity of these fixed report checks to selected plausible output errors, not exhaustive mutation coverage.

All 29 Chapter 14 Python files compiled and all 19 scripts passed on Python 3.12.14/Linux, assertions enabled and a 15-second timeout per script. [Raw evidence](chapter-14-diagnostic-integration-followup.json) retains the original integration-check failure and corrected outputs. This source/checker change follows [V-36](runtime-refresh-2026-10-29-r5.md); no new full-book pass is claimed.

## Remaining scope and checkpoint

Section 14.10 still returns several literal reference results and remains the next executable COV-67 item. The restricted helpers remain diagonal/2x2 teaching examples; broader numerical ranges, correlated/general matrices, all fault families and independent mathematical/editorial review are open. Twenty-five selected COV categories remain partially addressed; none is closed.
