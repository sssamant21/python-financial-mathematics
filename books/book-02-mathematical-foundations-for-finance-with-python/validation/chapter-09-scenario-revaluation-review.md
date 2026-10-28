# Book 02 — Chapter 9 Scenario Revaluation Review

**Date:** 2026-10-27  
**Scope:** Selected rate-shock valuation cancellation; not comprehensive Taylor-bound or independent mathematical review.

The local Chapter 9 code matched tree `516de89a0f14772a6b4a7e2539ac1763874ca5f6` except for the modified Section 9.9 module and a new regression script. Changes were published through `423cb9ed14215ff330d29e3612b425395c882513`.

## Finding and correction

For a payment of 100 in one year, zero initial rate and a synthetic +40 decimal-rate shock, the former report reconstructed its exact value as baseline plus change and returned zero. Direct evaluation gives approximately `4.248354255291589e-16`, which is representable. The very large shock is a numerical stress case, not an economically typical scenario.

The exact-value field now directly discounts the cash flows at the validated shifted rate. The stable expm1 expression for the exact-change field is retained, because it is useful for small changes. These fields need not reconcile by subtraction at every floating-point scale.

New checks cover cancellation after a large shock, a zero-shock analytic anchor, a two-payment known value and ordinary change reconciliation.

## Runtime evidence

All ten Section 9.1–9.10 check scripts and the new revaluation script exited zero on Python 3.12.14/Linux, each from its code directory with a 15-second timeout. This is scoped execution, not complete numerical coverage, independent review, cross-platform validation or a whole-book final-revision run.

## Remaining work

- Independently review mathematical Taylor bounds versus floating-point allowances, including underflow and large shocks.
- Assess elasticity and normalized-sensitivity ratios at extreme scales, denominator underflow and intermediate overflow.
- Review all examples, exercises and scenario assumptions; rerun the final agreed suite on supported environments.
