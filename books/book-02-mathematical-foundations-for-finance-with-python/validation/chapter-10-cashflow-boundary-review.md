# Book 02 — Chapter 10 Cash-Flow Boundary Review

**Date:** 2026-10-27  
**Scope:** Selected continuous cash-flow integral and rate-sensitivity cases; not comprehensive quadrature coverage or independent mathematical review.

The local Chapter 10 code matched tree `58957cacba183afcc0a9495d6541bc2eec53533f` except for two modified modules and a new regression script. Changes were published through `ea0639c80a1819750f37a65aefc8bf3dfdd63e27`.

## Findings and corrections

- Sections 10.5 and 10.9 evaluated the exponential integral as scale × time × expm1(x) / x. At a subnormal exponent, the product rounded before the division, giving approximately 0.333333 rather than the near-zero limit 0.3 in a synthetic case. The expm1(x)/x factor is now formed before multiplication.
- Section 10.9 consumed stream and payment iterators during the positive-bump valuation, so the negative-bump valuation could see empty inputs. A one-year payment of 100 at zero rate produced a positive derivative of about 499950 instead of approximately -100. The function now materializes inputs once and reuses them for both valuations.
- The sensitivity function now rejects indistinguishable/non-finite rate shifts and an overflowing central-difference denominator.
- Regression checks cover small positive and negative exponents, independent one-payment rate sensitivity, iterator/sequence equivalence, and invalid bump range.

## Runtime evidence

All ten Section 10.1–10.10 check scripts and the new cash-flow-boundary script exited zero on Python 3.12.14/Linux. Each was invoked from its code directory with a 15-second timeout. This scoped execution does not establish full book-wide, cross-platform or final-revision validation.

## Remaining work

- Independently assess extreme-range weighted integrals, intermediate products, cancellation and rate-bump accuracy.
- Review quadrature grids for representable spacing and correct behavior at zero horizon and very narrow intervals.
- Check documented iterator contracts, all manuscript examples and exercises, then rerun the final agreed revision on supported environments.
