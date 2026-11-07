# Next checkpoint: Section 8.4 callback and centered copy

Revision `7db1525c2f390b0eb9afa431c08648b6450737d3`; unchanged Section 8.4 source blob `c48e262b311561edccd42deaaf8407054baed103`.

Actual source probes:

```python
import sys
from section_8_04 import chain_derivative, centered_difference
M = sys.float_info.max
chain_derivative(lambda _: M, lambda x: x, lambda _: 2.0, 0.0)  # inf
centered_difference(lambda x: x, 0.0, M)  # nan
calls = []
def identity(x):
    calls.append(x)
    return x
centered_difference(identity, M, 1.0)  # 0.0; calls == [M, M]
```

The independently derived sampled identity quotient is (M - (-M))/(2M) = 1, while the copied float expression produces infinity/infinity and NaN. At x=M, a unit step collapses both represented perturbations to the same input; callbacks nevertheless run twice and a zero estimate is returned. The chain-rule callback product is mathematically 2M and cannot round to finite binary64; current code returns infinity. An actual instrumented call recorded inner, outer derivative and inner derivative once each, in that order, all at 0.0.

Next batch should establish the chain callback finite-output/error policy, retain callback evaluation ordering/counts and exception propagation, and test the actual Section 8.4 centered wrapper with independently derived quotient expectations. This is a substantive earlier-copy obligation under COV-51, not a repetition of Section 8.2's closed scoped examples. Variable-rate/discrete-compounding helpers, other earlier copies and manual range/domain review remain open. No reviewer or release gate is closed by this baseline.
