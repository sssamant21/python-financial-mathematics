# Section 19.4 — Equilibrium transition range checkpoint

The unchanged Section 19.4 source blob `2d611a1b29bc475a12c219e05e86a962ae0ff9f3` at executable revision `08e154d93ba1c3d413ab625a6680825f5121a3e0` produced three boundary discrepancies. M is the largest finite float and d is the smallest positive float.

| Call | Independently derived result | Observed |
|---|---|---|
| `mean_reversion(M,-M,1,0)` | M, by the zero-time identity | `ValueError: balance must be finite` |
| `logistic(d,1,M,0)` | d, by the zero-time identity | 0.0 |
| `half_life(d)` | `ln(2)/d` exceeds finite float range | infinity |

Replay from the book root:

```python
import math, sys
sys.path.insert(0, "chapter-19/code")
from section_19_04 import mean_reversion, logistic, half_life

m,d = sys.float_info.max,math.ulp(0.)
for fn,args in [(mean_reversion,(m,-m,1.,0.)),
                (logistic,(d,1.,m,0.)), (half_life,(d,))]:
    try:
        print(fn.__name__, fn(*args))
    except ValueError as error:
        print(fn.__name__, type(error).__name__, error)
```

Next: check the actual Section 19.4 trajectories and assessment fields, including complete convex weighting in mean reversion and the logistic reciprocal form under extreme scales. Distinguish representable subnormal states from true range failures and reuse compatible arithmetic where it fits. No Section 19.4 behavior changed in this batch.
