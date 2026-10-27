# Book 02 — Chapter 20 Focused Boundary and Check Review

**Date:** 2026-10-27  
**Scope:** Selected boundary behavior, tolerance comparisons and check scripts; not a complete chapter or independent mathematical review.

The local Chapter 20 code matched tree `d8064d2a0d4fdc674398c9c675319ca261f038c3` except for the two Section 20.4 files modified in this review. The changes were published through `18c0177fdb3130b724d895896bc8e2cd049d8d79`.

## Finding and fix

For `annuity_pv(0.1, 5e-324, 3)`, the previous implementation returned 0.0 because multiplying the small payment by the subnormal intermediate preceded division by the rate. The zero-rate limit and three-payment sum are approximately 0.3. The implementation now forms the annuity factor before multiplying by payment, and the check includes this regression case.

This improves one numerical regime; it does not prove accuracy across all inputs. Forming the factor can itself overflow or lose precision for extreme parameters even where a differently scaled calculation might represent a final value. Independent numerical review remains required.

## Runtime evidence

- Python 3.12.14 on Linux; the ten Section 20.1–20.10 check scripts ran from their code directory with a 15-second per-script limit and all exited zero.
- The rerun includes the new regression and the earlier Section 20.5 exact-float tolerance changes.
- Counts refer to script exits, not the number or quality of independent tests. No full book-wide or cross-platform rerun was performed.

## Remaining coverage questions

- Assess stable annuity and present-value evaluation across extreme valid rates, large horizons, underflow, overflow and cancellation, including an independent high-precision reference.
- Review Section 20.6's bounded teaching example for consistent treatment of Boolean inputs, non-finite results and overflow; its current checks do not establish a complete public input contract.
- Review exercises, formulas, source references and tolerances beyond the selected cases. Python assertions may be disabled under optimized execution; use a documented non-optimized test command or explicit checks where appropriate.
- Independently review all changes and rerun the full suite on the final agreed revision.
