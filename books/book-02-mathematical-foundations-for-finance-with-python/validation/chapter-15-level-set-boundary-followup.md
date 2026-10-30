# Chapter 15 — Selected level-set boundary follow-up

**Date:** 2026-10-30  
**Inspected revision:** `032a7f8242946770588a8cb288ee95cf03f20104`  
**Disposition:** COV-72 partially addressed; implementation unchanged.

The [new checker](../chapter-15/code/check_level_set_boundaries.py) directly covers the previously unasserted iso-variance denominator branches. For weights (9,-1), the exact decimal-coefficient relation .02*9+.18*(-1)=0 agrees with the represented gradient denominator. The slope rejects this vertical-tangent case and the critical point (0,0). Adjacent represented second weights give finite slopes on opposite sides; these are selected represented-float observations, not a continuous conditioning guarantee.

Four same-sign rate changes have exact rational adjusted maturities and revalue to the original future value within relative tolerance 2e-15. Both positive-to-negative and negative-to-positive rate crossings reject at positive maturity; landing exactly on zero rate also rejects. At zero maturity a sign crossing is accepted because adjusted maturity zero still preserves the zero-time level. Negative maturity rejects. This distinction prevents overclaiming that all sign crossings are forbidden.

All 24 Chapter 15 Python files compiled and all 14 scripts passed on Python 3.12.14/Linux, assertions enabled and 15-second timeout per script. No defect was confirmed in these selected boundary cases; implementation was preserved. These checks are included in the subsequent [V-37 full-book refresh](runtime-refresh-2026-10-30.md), whose machine evidence retains source hashes and raw outputs.

Remaining COV-72 scope includes applied differential/Taylor/ellipse examples, covariance symmetry/PD contracts, held-fixed/unit interpretation, numerical range and independent review. Twenty-six selected COV categories are now partially addressed; none is closed by this follow-up.

Next executable item: Section 15.8 finite rate-shock addition and extreme intermediate range, checking level preservation against an exact/high-precision reference before any change.
