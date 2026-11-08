# Next checkpoint: Section 8.5 accumulation scaling

Revision `04f45d68c3aaf1c3a25838fba4417df5198614c0`; Section 8.5 blob `1ba84903bf0647de9691a329b1ba4a151601423d`. Logarithm quotient changes do not alter these helpers. [Four actual value/time/rate probe triples](chapter-08-accumulation-range-baseline.json).

The helpers are `accumulation(P,r,t)`, `accumulation_time_derivative(P,r,t)`, and `accumulation_rate_derivative(P,r,t)`.

- P=minimum subnormal, r=1, t=1000: all three raise OverflowError although complete value, time-sensitivity and rate-sensitivity references are finite.
- P=1, r=-1, t=750: value and time sensitivity round to signed zero, while the rate sensitivity is a nonzero subnormal (approximately 1.5e-323); the helper loses it to a rounded zero value.
- P=maximum float, r=minimum subnormal, t=maximum float: value and rate sensitivity are unrepresentable, but complete time sensitivity is finite, approximately 8.88178419700126e-16. All three current outputs are infinity.
- P=0, r=maximum float, t=maximum float: model zero identities are lost to NaN.

Independent complete references P·exp(r·t), P·r·exp(r·t), P·t·exp(r·t) agree at Decimal precisions 200 and 400. Zero-principal identities follow algebra before enormous exponentials are formed; explicit sign records are retained. Treat unrepresentable final values separately from finite sensitivities and establish the output/error policy before editing.

Next batch should combine coefficients and exponents before rounding, preserve finite input and nonnegative principal/horizon guards and validation order, and check actual wrappers independently of any rounded value helper. PV/shock, return, stable quotient and centered-copy obligations and independent review remain open. Resume here without repeating completed exponential/logarithm derivative examples. No reviewer or release/platform gate is closed by this baseline.
