# Section 19.5 — Euler complete-update and grid checkpoint

The unchanged Section 19.5 Euler driver (blob `f6b9ef50437dcd16d784a084a1047de788bd61a2`) was exercised at the Chapter 19.6 corrected source revision `b5ed61885fc661feb72e9c27c8eb9f9ae220fecd`. It is a separate solver path, not covered by the RK4 interval fixes.

| Constant slope M (maximum float) | Independent expectation | Observed |
|---|---|---|
| Initial -M, horizon 2, one step | Final M, by the exact affine update `-M+2*M` | `ValueError: Euler state must be finite` |
| Initial zero, horizon three smallest subnormal time ticks, two steps | Final `2.6645352591003753e-15`, integrating M over the requested horizon | `completed` at `3.5527136788005005e-15`, after two steps each rounded to two ticks |
| Initial 5, zero horizon, three steps | Exact balance 5; no interval to evaluate | Balance 5, but three derivative calls at zero |

Replay from the book root:

```python
import math, sys
sys.path.insert(0, "chapter-19/code")
from section_19_05 import euler

m = sys.float_info.max
for initial, horizon, steps in [(-m,2.,1), (0.,3*math.ulp(0.),2), (5.,0.,3)]:
    seen = []
    def rhs(t, y):
        seen.append(t)
        return m
    try:
        actual = euler(rhs,initial,horizon,steps)
    except ValueError as error:
        actual = f"{type(error).__name__}: {error}"
    print(actual, seen)
```

Next: test and correct the actual Euler driver's complete affine update and represented endpoints, including a time-dependent derivative and collapsed grid. Reconcile zero-horizon behavior and the reported step metadata with the manuscript and preserve ordinary Euler convergence checks. No Section 19.5 source changed in this batch.
