# Next checkpoint: Section 8.5 logarithm derivative

Revision `8a23628022d832fbd80422aaf6ca582b28917de6`; Section 8.5 blob `cc61abb6a366aaf6d95ae87e12d4807314d4a003`. The exponential correction does not change `logarithm_derivative`. [Four actual probes and exact represented-input references](chapter-08-logarithm-derivative-range-baseline.json).

For x=maximum float, offset=1 and slope=maximum float, the helper returns zero while the complete ratio slope/(offset+slope·x) rounds to 5.562684646268003e-309. Its signed counterpart x=-maximum, slope=-maximum returns negative zero rather than -5.562684646268003e-309.

For x=nextafter(1,+infinity), offset=-maximum and slope=maximum, the helper returns zero while complete cancellation leaves a finite positive argument and ratio 4503599627370496. These positive-argument examples lose finite ratios through separate denominator arithmetic.

The fourth input x=10, offset=-1, slope=represented(0.1) raises ValueError because the rounded argument is zero. Its exact represented-input argument is positive and would give ratio 1801439850948198.5. This is explicitly a domain-policy question: a decimal-real 0.1 model or rounded affine-argument policy is not the same as an exact represented-input predicate. Do not silently call acceptance mandatory under the old contract.

Reproduce actual outputs with `logarithm_derivative(x, offset, slope)`; derive independent references with `Fraction(offset)+Fraction(slope)*Fraction(x)` and divide Fraction(slope) by that complete argument. Next batch should establish quotient scaling, true final overflow, signed results/zero slopes, and reconcile the intended argument-domain convention before editing. Preserve finite/type validation and document any explicit contract change.

Section 8.5 accumulation/PV/shock, log-return, stable exponential quotient and centered-copy obligations and independent review remain open under COV-51. Resume here without repeating completed exponential-derivative or Section 8.4 examples. No reviewer or release/platform gate is closed by these probes.
