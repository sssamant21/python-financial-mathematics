# Book 02 — Chapter 5 Recurrence Boundary Review

**Date:** 2026-10-27  
**Scope:** Selected floating-point recurrence and withdrawal boundaries; not comprehensive sequence or independent mathematical review.

The local Chapter 5 code matched tree `dd3b9ea2931a37f0ab541f12fcf31b41eb8af693` except for two modified modules and a new regression script. Changes were published through `2d5c4d0c29c8cc067bfaba61506e7327383592e2`.

## Finding and correction

At initial balance 1e16 and the representable rate immediately above -1, adding initial balance to separately rounded interest produced 2.0. Multiplying by the positive growth factor gives approximately 1.1102230246251565. This difference could incorrectly permit a withdrawal of 1.5.

Sections 5.3 and 5.9 now calculate balances with the multiplicative growth-factor recurrence. The rounded interest remains recorded, and a separate `rounding_adjustment` field reconciles its numerical difference from the chosen balance calculation. Reconciliation helpers include this adjustment; it is numerical metadata, not a financial fee or cash flow. Ordinary float arithmetic and aggregate reconciliation can still round.

New checks cover the near-minus-one balance, an independent product-form reference, correct withdrawal rejection and beginning-period contributions.

## Runtime evidence

All ten Section 5.1–5.10 check scripts and the new recurrence-boundary script exited zero on Python 3.12.14/Linux, each from its code directory with a 15-second timeout. This is not a full book-wide, final-revision or cross-platform run.

## Remaining work

- Independently assess rounding-adjustment semantics and reconciliation across long schedules and extreme magnitudes.
- Review no-overdraft and withdrawal timing policies, closed-form intermediate range, and very large depletion-period calculations.
- Complete example/exercise coverage and mathematical review, then rerun the final agreed revision on supported environments.
