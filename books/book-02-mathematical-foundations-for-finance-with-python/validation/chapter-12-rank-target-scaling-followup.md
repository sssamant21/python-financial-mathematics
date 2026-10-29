# Chapter 12 — Target-scale rank follow-up

**Date:** 2026-10-29
**Scope:** Section 12.5 portion of COV-61.
**Status:** Confirmed defect corrected; scoped runtime pass complete; independent review pending.

## Reproducer and intended contract

For A equal to the 2-by-2 identity, the exact rank is two and Ax=b has the unique solution x=b for every finite target. The old classifier reported ranks 2/2 for b=(1,-1), but ranks 0/1 and no_solution for b=(1e200,-1e200). Its shared threshold was tolerance times the largest augmented entry, allowing b to suppress every coefficient pivot.

The corrected teaching convention divides each nonzero column by its maximum absolute entry, leaving zero columns zero. Elimination then uses the disclosed tolerance on both normalized arrays. Coefficient columns are normalized identically with or without the target, so rank_A no longer depends on b. The report includes rank_scaling, and manuscript section 6 explains the convention.

Nonzero column scaling preserves exact rank because it is multiplication by an invertible diagonal matrix. Normalizing the appended target likewise preserves exact consistency classification. Finite-precision rank remains tolerance-dependent: this convention measures dependence after column equilibration and changes how very small independent columns are treated. It is not an SVD certification, an equation-row-scaling guarantee or an exact existence oracle near a tolerance boundary. Division can lose components with an extreme within-column dynamic range; elimination and conditioning limitations remain.

## Regression evidence

New assertions cover 21 selected outcomes:
- Identity matrix with zero, tiny, ordinary and huge targets: ranks 2/2 and unique.
- Proportional columns with six signed target magnitudes, each attainable and unattainable: rank_A remains one, with augmented rank one or two respectively.
- Zero matrix with zero and tiny nonzero targets: infinite versus inconsistent.
- A near-dependent matrix at two tolerances: the expected rank transition is explicit.
- Independently scaled identity columns at 1e-200 and 1e200: rank two.

Expected identity, proportional and zero-matrix results follow directly from their equations; the tolerance-transition case tests the stated numerical policy rather than proving exact rank.

## Runtime and publication

Baseline tree: `79f143f803a5b5d0ed6d6a224ce9e7801b74dd79`. All 21 Chapter 12 Python sources were fetched from that revision. The local run replaced only section_12_05.py and check_section_12_05.py with the published changes below.

Python 3.12.14/Linux: 21/21 files compiled with py_compile, and 11/11 check scripts exited zero. Scripts ran from the chapter code directory with assertions enabled and a 15-second per-script timeout. This includes the inverse-scaling regression script. A separate execution of the old helper reproduced the incorrect identity classification above.

| File | Commit | Blob |
|---|---|---|
| [section_12_05.py](../chapter-12/code/section_12_05.py) | `a89b794470d0de64d805c9bd36753780af4b45b4` | `49474925f12f5dee35697c90427aa16b3311518a` |
| [check_section_12_05.py](../chapter-12/code/check_section_12_05.py) | `f380eb6e7ce5ae52ed4ab5fb44e3b3a0cec01d4e` | `9b09e8fc79cd058dbbefc2bacae7cc6d45f111ca` |
| [12.05-rank-and-existence-of-solutions.md](../chapter-12/12.05-rank-and-existence-of-solutions.md) | `62fa143e8990c0d56a07a8e4483859a040598f57` | `957d34990bb805000f53cad03d873c7084e13caa` |

COV-61 is partially remediated; larger pivoting/scaling examples and independent numerical review remain open. This scoped run does not replace the historical full-book run. See the [coverage map](coverage-chapter-12.md), [queue](substantive-coverage-index.md) and [tracker](PROGRESS.md).
