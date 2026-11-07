# Section 21.8 CF-04 splitting property: numerical domain checkpoint

The remaining COV-88 requirement evidence includes interpreting the plan's CF-04 statement, “same-date cash-flow splitting preserves PV,” against the actual monetary-term rounding and range contract. The normal-scale split test already exists and must not be counted again.

Reproduced at [pinned source `00fd462aa3a0da15d5babd6c26dc6e49c072e425`](https://github.com/sssamant21/python-financial-mathematics/blob/00fd462aa3a0da15d5babd6c26dc6e49c072e425/books/book-02-mathematical-foundations-for-finance-with-python/chapter-21/code/section_21_03.py), module blob `ebf9d4733542fb11b5c8121fb9ec8725d2b260c4`:

| Rows at one year | Rate/convention | Observed split representation | Observed merged representation |
|---|---|---|---|
| Two least-positive-float amounts | 1, continuous | 0 | least positive float |
| Two least-positive-float amounts | 2, effective annual | 0 | least positive float |
| Maximum finite float and its negative | −1, continuous | `OverflowError: cash-flow value exceeds float range` | 0 |

The first two follow independently from rounding each discounted term before adding: each factor is below one-half, while the combined amount discounts to more than one-half of the least positive float. The third follows from exact cancellation before discounting versus rejecting an unrepresentable individual term. The split residual is tiny in the first cases; this is not evidence that the existing ordinary-scale tolerance test fails.

Replay from `chapter-21/code`:

```python
import math
import sys
from section_21_03 import present_value

u = math.ulp(0.0)
for rate, convention in ((1., "continuous"), (2., "effective_annual")):
    print(present_value([(u,1.),(u,1.)],rate,convention).hex())
    print(present_value([(2*u,1.)],rate,convention).hex())
try:
    present_value([(sys.float_info.max,1.),(-sys.float_info.max,1.)],-1.,"continuous")
except OverflowError as exc:
    print(type(exc).__name__,str(exc))
print(present_value([(0.,1.)],-1.,"continuous"))
```

Next: reconcile CF-04's acceptance domain and tolerance with the implemented per-term rounding contract, preserve these observed boundaries and add meaningful assertion-based property checks. Distinguish the mathematical linearity identity from an unconditional binary64 identity; do not silently change the valuation aggregation policy. Wider requirement evidence and manual review remain open.
