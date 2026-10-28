# Book 02 — Chapter 4 Growth Recovery Source Review

**Date:** 2026-10-27  
**Status:** Source changes authored; runtime validation blocked by unavailable execution environment.

## Scope and source

Reviewed selected logarithm, rate-conversion and growth-project source at tree `8e83acebcc2f369c6f61763ce810c01cfd1e90be`. The Section 4.9 code and new check source were published through `f6d3675d7b79bdcfb0433b199535db0988b9d5c5`; its manuscript was subsequently clarified.

## Source finding and change

Both periodic_result and continuous_result compute a growth factor with exp and then recover present value by dividing future value by that factor. A sufficiently negative exponent can underflow the factor to zero, leaving the recovery division undefined. The functions now raise an explicit OverflowError when the growth factor is zero. This defines a supported numerical recovery range; it does not say the mathematical model is undefined.

The new [regression source](../chapter-04/code/check_growth_recovery_boundaries.py) specifies underflow rejection for continuous rate -1000 over one year and annual periodic rate -0.5 over 2000 periods, plus ordinary known-value, zero-horizon and zero-principal cases.

## Evidence and limitation

No Python compilation, regression execution, chapter-wide rerun or new runtime pass is claimed. A command attempt returned “No usable execution environment is available.” The source conclusion follows from the evaluation order and floating-point underflow semantics; the specified cases have not been reproduced in the current pass.

## Required follow-up

1. Compile the changed module and new check, then run the new regression and all Chapter 4 checks in a recorded environment.
2. Review remaining rate-conversion overflow, recovery after partial underflow, very large period counts and CLI error behavior.
3. Reconcile the existing Section 4.7–4.8 title/scope discrepancies through the documented curriculum policy.
4. Obtain independent mathematical review and rerun the final agreed revision on supported platforms.

The chapter remains not certified.
