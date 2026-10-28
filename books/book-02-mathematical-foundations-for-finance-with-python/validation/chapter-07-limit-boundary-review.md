# Book 02 — Chapter 7 Limit Boundary Review

**Date:** 2026-10-27  
**Scope:** Selected small-change limits and bond-payment input behavior; not comprehensive continuity or independent mathematical review.

The local Chapter 7 code matched tree `dcb7facbbe28bb88bb465d20fdabc6c21f2e85e7` except for two modified modules and a new regression script. Changes were published through `0e4ec168f56e155bd1c6bdcd2531b5b40890c3df`.

## Findings and corrections

- For h=5e-324 and exponent 0.5, the power quotient returned zero because exponent × log1p(h) rounded to zero before division. Its mathematical small-change limit is 0.5. The expression now factors into the exponent times continuous logarithmic and exponential quotient factors, using the exponential ratio's value 1 at zero.
- The bond-residual function checked the truth value of a payment iterable before consuming it. An empty iterator therefore bypassed the nonempty-input rule and returned minus the price. It now checks the materialized payment list.
- Regression cases cover positive and negative subnormal inputs, several limiting exponents, a polynomial identity, empty iterator rejection and a known payment-iterator result.

## Runtime evidence

All ten Section 7.1–7.10 check scripts and the new limit-boundary script exited zero on Python 3.12.14/Linux, each from its code directory with a 15-second timeout. This is not full book-wide, cross-platform or final-revision validation.

## Remaining work

- Independently assess large exponents, quotient scaling and the difference between numerical samples and proof of a limit.
- Review approach-table perturbations, bisection stopping at adjacent floats, and bond discount powers at extreme rates.
- Review all examples, exercises and continuity assumptions, and rerun the final agreed suite on supported environments.
