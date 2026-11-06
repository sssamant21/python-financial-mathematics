# Section 19.6 — RK4 stage and increment range checkpoint

Probes ran at `43ccada6e1ea5a10e2e571fc72357b20d46978b4` against `section_19_06.py` blob `8a9bac4c4b973db41c0274e0f7ada06ec131d71a`, which is unchanged by the Section 19.8 batch. These investigate the numerical range left open by the [adaptive policy checks](chapter-19-adaptive-policy-followup.md), rather than repeating their rejection and controller fixtures.

| Probe | Independently derived expectation | Observed |
|---|---|---|
| Constant derivative `M = sys.float_info.max`, initial zero, step `2**-1023` | All four slopes are M, so the RK4 weighted increment is exactly `M * 2**-1023`, rounded to `1.9999999999999998`. | `ValueError: RK4 state must be finite` |
| Two-unit step, slopes M, 0, 0, -M by stage time | The first midpoint receives state M (the exact product `2*M/2`); the second midpoint and final stage receive zero; final increment is zero. | Final value zero, but the first midpoint receives infinity. |

Replay at the pin from the book root:

```python
import sys
sys.path.insert(0, "chapter-19/code")
from section_19_06 import rk4_step

M = sys.float_info.max
try:
    print(rk4_step(lambda t, y: M, 0., 0., 2.**-1023))
except ValueError as error:
    print(type(error).__name__, str(error))
seen = []
def rhs(t, y):
    seen.append((t, y))
    return {0.: M, 1.: 0., 2.: -M}[t]
print(rk4_step(rhs, 0., 0., 2.), seen)
```

Next: use exact represented arithmetic to independently derive stage inputs and weighted increments. Check genuine out-of-range callback inputs and states, fixed/adaptive consumers and existing callback and exception contracts. Then evaluate adaptive error/scale range separately; its existing policy assertions remain in force. No Section 19.6 code changed in this batch.
