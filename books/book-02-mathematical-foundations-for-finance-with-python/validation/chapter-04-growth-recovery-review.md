# Book 02 — Chapter 4 Growth Recovery Source Review

**Date:** 2026-10-27  
**Status:** Focused runtime follow-up passed; independent review and final-revision validation pending.

## Scope and source

Reviewed selected logarithm, rate-conversion and growth-project source at tree `8e83acebcc2f369c6f61763ce810c01cfd1e90be`. The Section 4.9 code and new check source were published through `f6d3675d7b79bdcfb0433b199535db0988b9d5c5`; its manuscript was subsequently clarified.

## Source finding and change

Both periodic_result and continuous_result compute a growth factor with exp and then recover present value by dividing future value by that factor. A sufficiently negative exponent can underflow the factor to zero, leaving the recovery division undefined. The functions now raise an explicit OverflowError when the growth factor is zero. This defines a supported numerical recovery range; it does not say the mathematical model is undefined.

The new [regression source](../chapter-04/code/check_growth_recovery_boundaries.py) specifies underflow rejection for continuous rate -1000 over one year and annual periodic rate -0.5 over 2000 periods, plus ordinary known-value, zero-horizon and zero-principal cases.

## Runtime follow-up — 2026-10-27

Execution became available again. All 21 Chapter 4 Python files were fetched at repository revision `94f7ad43cb5200826a97d3184691cd7d652849dd` into an isolated local snapshot.

- Environment: Python 3.12.14, Linux.
- Compilation: 21/21 files compiled successfully using `py_compile.compile(path, doraise=True)`.
- Execution: each `check*.py` file ran with the Python interpreter from its code directory, with captured output and a 15-second timeout per script.
- Outcome: 11/11 scripts exited zero: the ten numbered section checks and `check_growth_recovery_boundaries.py`.
- The new boundary script ran five unittest cases, all passing. These include both growth-factor underflow rejections and the ordinary-value, zero-horizon and zero-principal cases.

This supersedes the earlier unavailable-environment status for this scoped run. It does not establish substantive manuscript coverage, independent mathematical review, cross-platform behavior or a final-revision book-wide pass.

## Required follow-up

1. Preserve this scoped result and repeat the agreed checks if relevant source changes before the final-revision run.
2. Review remaining rate-conversion overflow, recovery after partial underflow, very large period counts and CLI error behavior.
3. Reconcile the existing Section 4.7–4.8 title/scope discrepancies through the documented curriculum policy.
4. Obtain independent mathematical review and rerun the final agreed revision on supported platforms.

The chapter remains not certified.
