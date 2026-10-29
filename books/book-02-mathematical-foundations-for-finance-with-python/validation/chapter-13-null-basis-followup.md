# Chapter 13 — Selected null-basis follow-up

**Date:** 2026-10-29  
**Implementation blob tested:** `a9c26dee5f9ffc7dcbbfbc11648924e8f9ff0de8`  
**Disposition:** COV-64 remains partially open.

The [new checker](../chapter-13/code/check_null_basis.py) covers four known matrices: rank-one rows (1,2,4)/(2,4,8), rank-two rows (2,1,4)/(1,-1,2), a zero two-by-three matrix and the three-by-three identity. Known ranks follow respectively from proportional nonzero rows, the nonzero first-two-column minor, all-zero entries and identity structure.

All six column permutations and three common scales (1, 2^20, 2^-20) yield 72 cases. Each checks rank/nullity, returned basis size and label coverage. Exact Fraction arithmetic applied to the actual returned float components verifies Az=0. The identity submatrix at the nonpivot coordinates proves independence of the returned vectors in each selected case. Combined with the independently known nullity, this establishes their completeness for these cases.

A selected linear combination of returned null vectors is added to an initial holdings vector; achieved exposures remain exactly equal. Full-rank cases have an empty null basis; zero matrices return three independent directions.

All 26 Chapter 13 Python files compiled and all 16 check scripts exited zero on Python 3.12.14/Linux with assertions enabled and a 15-second per-script timeout. Local and GitHub implementation blob hashes matched; implementation unchanged. This scoped run includes previous Chapter 13 follow-ups and follows the [third full-book refresh](runtime-refresh-2026-10-29-r3.md).

## Limits

The exact identities use selected dyadic/integer examples; they do not imply exact null vectors for arbitrary floating-point matrices. General near-dependence, tolerance-policy behavior, Q/R identities, conditioning and proofs/reviewer sign-off remain open. The count remains twenty-three partially addressed COV categories; no category is closed here.
