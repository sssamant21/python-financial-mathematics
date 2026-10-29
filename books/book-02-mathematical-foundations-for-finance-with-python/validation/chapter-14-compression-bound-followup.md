# Chapter 14 — Compression bound and metadata follow-up

**Date:** 2026-10-29
**Scope:** Remaining fixed-example compression/report portion of COV-69.
**Status:** Selected executable obligations addressed; independent review pending.

## Correction and evidence

The capstone previously formed full and compressed exposures from separately hardcoded coordinate formulas. It now multiplies the actual original and approximation matrices returned by the compression helper by the solved positions. The report retains both matrices, the weights, target and illustrative unit labels. It also reports the lost-exposure Euclidean norm and spectral operator bound.

For the reference matrices, \(D=E-E_1=\operatorname{diag}_{3\times2}(0,2)\), so \(\|D\|_2=2\). At \(x=(2,2)\), \(Dx=(0,4,0)\), hence \(\|Dx\|_2=4\) and \(\|D\|_2\|x\|_2=4\sqrt2\). At \(x=(0,1)\), equality holds. The manuscript now derives the bound and distinguishes it from an adequacy threshold.

The checker tests four magnitude pairs (4,2), (2,4), (2,2), (0,0) at ranks zero, one and two. It independently derives retained coordinates, including the declared tie policy, then checks actual returned-matrix residual actions for four position vectors in each case (48 selected actions). It verifies the spectral bound and a coordinate direction attaining its value. These diagonal examples do not constitute a general low-rank approximation or financial adequacy proof.

The fixed capstone's inputs, matrix outputs, measured error norm and expected bound are directly asserted. Unit labels document intended interpretation, not automated dimensional analysis or market-data provenance.

## Runtime and publication

Baseline tree: `bc99402f37ad2de4c8925d7d59138f7a16b596d7`. The other 19 Chapter 14 Python files matched their pinned Git blob hashes; the local snapshot replaced only the capstone and its checker.

Python 3.12.14/Linux: 21/21 files compiled with py_compile; all 11 check scripts exited zero from their code directory with assertions enabled and a 15-second per-script timeout. This scoped run occurred after the latest full-book runtime refresh; that earlier result remains pinned to its own source revision.

| File | Commit | Blob |
|---|---|---|
| [section_14_09.py](../chapter-14/code/section_14_09.py) | `61a5e08e6da37eabe02099ea5829490854b3b17d` | `4f1bfb5a7eea3723274881cc8209c3afad228cee` |
| [check_section_14_09.py](../chapter-14/code/check_section_14_09.py) | `b71c29f77c5b161a828abd1045e0a920bd21aa69` | `e4a7f6faf60c94b6f4e31cc0bbe7948c93bdaf7f` |
| [14.09-chapter-project-quadratic-exposure-and-decomposition-lab.md](../chapter-14/14.09-chapter-project-quadratic-exposure-and-decomposition-lab.md) | `ff810496ca5d5dc237c41480748ae2b83569957d` | `6e7b12c0a4c51aa1b8e51a772fa6366ee14a220d` |

COV-69 remains partially open for independent mathematical/editorial review and broader interface/numerical-range considerations. The original eigenpair follow-up and historical map remain separate evidence records.

[Eigenpair follow-up](chapter-14-covariance-eigenpair-followup.md) · [Chapter 14 map](coverage-chapter-14.md) · [Remediation register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
