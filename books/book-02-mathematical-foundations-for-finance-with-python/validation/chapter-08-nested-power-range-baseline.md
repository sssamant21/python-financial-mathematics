# Next checkpoint: Section 8.4 nested-power derivative

Revision `a93acb89609087281b4e1872c6420313ddf7adca`; Section 8.4 source blob `269a5196af7f37d5bd998a717c5baddaba04db8a`. Count-conversion changes do not alter `nested_power_derivative`. [Five actual probes and exact rational polynomial references](chapter-08-nested-power-range-baseline.json).

For x=±4e43, finite outputs differ from one-final-rounding references from the expanded polynomial. This is an accuracy-contract question, not a claim that a previous one-rounding requirement existed. For x=±4.5e43, actual outputs are ±infinity although the exact complete derivative cannot round to finite binary64. At x=1e100, the helper instead raises OverflowError. The next batch should establish consistent finite-output/overflow behavior and reconcile the accuracy contract.

Independently expand 24x(3x²+2)³ into 648x⁷+1296x⁵+864x³+192x. Evaluate with Fraction(x) and exact integer coefficients, then convert the complete sum to float. This yields finite references ±1.0616832e308 for x=±4e43 and an OverflowError reference for the three larger selected magnitudes.

Reproduce actual behavior with `nested_power_derivative(x)` at the five JSON inputs. Preserve finite input validation and derive signed subnormal, ordinary and boundary references before editing. Price/log-growth, remaining earlier copies and independent manuscript/math review remain open under COV-51. Resume here without repeating completed period-count or compounding cases. No reviewer or release/platform gate is closed by this baseline.
