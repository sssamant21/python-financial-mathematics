# Chapter 8 — Finite-difference helper guards follow-up

**Date:** 2026-10-29 (America/New_York)
**Scope:** Section 8.8 portion of COV-51.
**Status:** Selected output-range defects corrected and helper guards checked; independent review pending.

Finite callback values could previously yield infinite forward/backward/centered/second-difference results. These helpers and Richardson now validate returned estimates through the existing finite validator and raise ValueError for nonfinite results.

Richardson is evaluated as fine+(fine-coarse)/3 rather than (4*fine-coarse)/3. For f(x)=1e308*x at x=0,h=0.25, both centered estimates equal 1e308; the rearrangement returns this representable derivative instead of overflowing the unnecessary multiplication by four. It is an algebraic rearrangement, not a general all-range guarantee.

The checker tests five helpers for zero/negative/lost/boolean/nonfinite/overflowing perturbations, invalid callback values and exact affine derivatives. Observed callback lists establish that invalid full-step controls reject before evaluating functions. Separate cases cover h^2 underflow/overflow, doubled-step overflow, and a full step whose Richardson half-step cannot perturb the base point. Finite callback/output-subtraction overflow cases and the large linear Richardson oracle are asserted.

Baseline tree: `f86f01d1e34d67f1b03059beb81c330728678eda`. All 21 Chapter 8 Python sources were fetched at that revision; the local snapshot replaced only Section 8.8 and its checker. Python 3.12.14/Linux: 21/21 files compiled and 11/11 check scripts exited zero with assertions enabled, own-directory working directories and a 15-second per-script timeout.

| File | Commit | Blob |
|---|---|---|
| [section_8_08.py](../chapter-08/code/section_8_08.py) | `730c7075463bbed9a1c8c072a61aece7e5f3365d` | `a32025f6c4d27520c73e03c4c16624961ec6134f` |
| [check_section_8_08.py](../chapter-08/code/check_section_8_08.py) | `4c9a0dabe2a32c9f06217ee506e9d56fd3ff00c8` | `6c2eed340f7a2900c6e6f199389de37f7a539ca9` |
| [8.08-numerical-derivatives-and-step-selection.md](../chapter-08/8.08-numerical-derivatives-and-step-selection.md) | `ecdd13245c246f1064583a769e0b18fbe7235f6d` | `9f87bb297cbb2f426a2039e1369e957a781acedb` |

COV-51 remains partially open for earlier derivative copies, implicit branch/domain and near-singularity review, broader numerical ranges and independent review. These guards do not certify step accuracy or eliminate cancellation and underflow. This scoped change follows the latest full-book run.

[Chapter 8 map](coverage-chapter-08.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
