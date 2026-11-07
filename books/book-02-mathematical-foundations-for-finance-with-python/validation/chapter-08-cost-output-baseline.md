# Next checkpoint: Section 8.2 cost output

Revision `78b09101177563c3511c1932f6a4e7469567e7bc`, Section 8.2 source blob `a497e6c64b4964effda0326f1bb2ddcff66648ab`.

Actual probe:

```python
import sys
from section_8_02 import cost
print(cost(sys.float_info.max))  # inf
```

The existing helper accepts this finite nonnegative quantity but returns nonfinite output. All terms in 1000 + 20q + 0.05q² are positive here; even 20q exceeds maximum finite binary64. Thus no cancellation can recover a representable final cost. Next batch should establish the financial helper's finite-output/overflow contract, derive independent complete cost and marginal references, check actual near-boundary quantities, and preserve invalid quantity behavior. This is a retained failure to be addressed, not a passing validation claim.

Other earlier Chapter 8 copies and implicit-domain/range review remain open under COV-51. Resume this obligation without repeating completed polynomial and centered-copy examples. External review/approval gates remain separate.

## Adjacent-boundary screen retained

[Four actual observations and independent references](chapter-08-cost-output-baseline.json) locate the positive cost boundary with a 120-digit Decimal quadratic root, then evaluate adjacent binary64 quantities using exact rational monomial sums. At q = 5.996153992122475e154, the finite complete reference matches. At q = 5.996153992122476e154, the current value differs from the complete rounded reference by one ulp; acceptance requires an explicit accuracy contract. At the next float, q = 5.996153992122477e154, the complete reference overflows while the helper returns infinity. Maximum float also returns infinity. These are exploratory observations for the next batch; no cost contract is closed.
