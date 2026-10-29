# Chapter 11 — Projection diagnostic follow-up

**Date:** 2026-10-29 (America/New_York)
**Scope:** Section 11.6 projection-report portion of COV-60.
**Status:** Selected scalar/residual diagnostics checked; scoped runtime passed; independent review pending.

The fixed assessment report now retains Euclidean residual norm and relative residual norm. Independently expected values are sqrt(1650) USD and sqrt(1650/12900). The coefficient is 75 USD; the signed scalar projection is 150/sqrt(2) USD, separately asserted.

For four exposure/direction pairs and five direction scales (1,2,-2,1e150,1e-150), the checker derives the coefficient from exact rational dot products of the represented float inputs. It checks projected coordinates, reconstruction, orthogonality with the unscaled direction, energy decomposition, label ordering, axis and units. The examples include zero and orthogonal exposure vectors and sign-reversed projection lengths.

The relative diagnostic is defined only for the assessment's fixed nonzero exposure. No general zero-reference relative-distance convention, arbitrary-range accuracy, unit governance or financial adequacy guarantee is added. The projection algorithm itself is unchanged.

Baseline tree: `952c0fafef95cfa68bd267d6e9ff15572b62074a`. All 21 Chapter 11 Python files were fetched at that revision; the local snapshot replaced only Section 11.6 and its checker. Python 3.12.14/Linux: 21/21 files compiled and 11/11 check scripts exited zero with assertions enabled, own-directory working directories and a 15-second per-script timeout.

| File | Commit | Blob |
|---|---|---|
| [section_11_06.py](../chapter-11/code/section_11_06.py) | `ed019315834cd76d070d4abb4645f17a05836aa5` | `92d235ef10ed782f4b2b681572ca167e0dcd9642` |
| [check_section_11_06.py](../chapter-11/code/check_section_11_06.py) | `b17c05f9afa19d191e3c6f732e8db7eee800fb12` | `e634c32241a02ba9741b287ecd1f106bb126b667` |
| [11.06-projection-onto-a-direction.md](../chapter-11/11.06-projection-onto-a-direction.md) | `f8f14b19051f5d8930d836199e375710376a1f96` | `e208c62d25f9710fe950ed41452ac74bdc050a0e` |

COV-60 remains partially open for other report fields, general relative-distance behavior, cumulative scope and independent review. This scoped change follows the recorded full-book run.

[Chapter 11 map](coverage-chapter-11.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
