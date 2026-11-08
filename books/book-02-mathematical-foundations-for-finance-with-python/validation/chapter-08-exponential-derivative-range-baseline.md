# Next checkpoint: Section 8.5 exponential-derivative scaling

Revision `99ef9ddc1fab5e20ca83df6254d639720ff23b36`; unchanged Section 8.5 blob `f4354c95dc4c355b20ed2407f9f0e706a7c75e83`. [Four actual probes and independent complete references](chapter-08-exponential-derivative-range-baseline.json).

```python
import sys, math
from section_8_05 import exponential_derivative
M, T = sys.float_info.max, math.ulp(0.0)
exponential_derivative(-500.0, M, 2.0)  # nan
exponential_derivative(1000.0, T, 1.0)  # OverflowError
exponential_derivative(M, 0.0, M)  # nan
exponential_derivative(-500.0, -M, 2.0)  # nan
```

Complete references are respectively 1.8250032925935892e-126, 9.733444573000164e110, zero, and -1.8250032925935892e-126. Decimal evaluations at 200 and 400 digits agree for nonzero cases. The zero-scale case follows algebra without forming the enormous exponential.

The actual helper forms a*k and exp(k*x) separately, losing finite results to intermediate overflow/underflow and the zero identity to zero times infinity. Next batch should derive complete scaling, true final overflow, signed output and zero-growth/zero-scale cases while preserving all finite input/type domains. Establish exact represented product versus earlier exponent-rounding semantics explicitly. This is a distinct earlier helper, not a replay of completed Section 8.4 PV functions.

Section 8.5 logarithm, accumulation/PV, return and copied centered-difference obligations and independent review remain open under COV-51. Resume here without repeating completed Section 8.4 price or nested-power examples. No reviewer or release/platform gate is closed by these probes.
