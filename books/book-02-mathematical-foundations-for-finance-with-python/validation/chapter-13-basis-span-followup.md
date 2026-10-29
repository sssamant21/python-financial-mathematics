# Chapter 13 — Reordered basis-span follow-up

**Date:** 2026-10-29  
**Implementation blob tested:** `0a6ac018cdef722ee4410ad77f5e468f43040074`  
**Disposition:** Selected COV-64 obligation addressed; category partially open.

The [new checker](../chapter-13/code/check_basis_span.py) tests all six permutations of columns A=(2,1), B=(1,-1), C=(4,2), at common scales 1, 2^40 and 2^-40. For each of eighteen cases, it takes the basis labels actually returned by the implementation, verifies the basis/redundant partition and independently solves coordinates by exact Fraction Cramer's rule.

Every original column is reconstructed exactly from that selected basis; the floating-point achieved-exposure helper then reproduces each column at the reported coordinates. The same procedure reconstructs the separately chosen exposure (5,1), scaled consistently. This supplies 72 selected reconstruction targets rather than merely checking that rank is unchanged by column order.

All 25 Chapter 13 Python files compiled and all 15 check scripts exited zero on Python 3.12.14/Linux with assertions enabled and a 15-second timeout per script. The local implementation blob matched GitHub; implementation unchanged. The scoped run includes the preceding QR, ridge and project-contract checkers and follows the [third full-book run](runtime-refresh-2026-10-29-r3.md).

## Remaining scope

These exact two-factor examples establish the selected reordered-basis reconstruction obligation. They do not establish general numerical-rank invariance, arbitrary near-dependence, all coefficient scales or Q/R identities. Independent proofs and review remain pending. COV-64 is still partially open; the number of partially addressed categories remains twenty-three.
