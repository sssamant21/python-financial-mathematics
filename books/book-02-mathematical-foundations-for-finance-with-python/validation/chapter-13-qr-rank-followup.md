# Chapter 13 — Selected QR rank-screen follow-up

**Date:** 2026-10-29  
**Inspected source snapshot:** `ce1ceaa789fc0ea43f7928a277d78968eea9ea98`  
**Disposition:** COV-64 partially addressed; independent review pending.

## Evidence

The new [rank-screen checks](../chapter-13/code/check_qr_rank_screen.py) use diagonal matrices to isolate the existing normalized-pivot threshold. At tolerance 2^-20, pivots zero, half the tolerance and exactly the tolerance are rejected; pivots twice and four times the tolerance are accepted with known positions (1,1). Cases use common scales 1, -1, 2^100 and 2^-100. These are selected exact binary boundary cases, not a proof for arbitrary near-dependent matrices.

A separate overdetermined example checks the rational minimizer (7/3,10/3), achieved exposures (7/3,10/3,17/3) and objective 1/6 under both instrument-column orders and a permuted target-label order. Expected constants follow the independent normal equations 2x+y=8 and x+2y=9.

All 22 Chapter 13 Python files compiled and all 12 check scripts exited zero on Python 3.12.14/Linux, assertions enabled and a 15-second timeout per script. This scoped run follows the [third full-book refresh](runtime-refresh-2026-10-29-r3.md); that earlier full run does not include this new checker. Solver implementation unchanged.

## Limits

The solver screens an unpivoted Householder process after common maximum-entry scaling. The threshold is an algorithmic rejection policy, not a singular-value rank certificate. These tests do not exercise every near-dependent orientation, independently reconstruct reordered basis spans, inspect Q/R identities (factors are not returned), establish general conditioning bounds or complete the chapter's proofs.

COV-64 remains partially open. Independent mathematical/editorial review, broader platform validation and release approval remain pending.
