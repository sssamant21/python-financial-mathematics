# Section 19.7 — Terminal jump and crossing interpolation checkpoint

These observations use the unchanged Section 19.7 source blob `454bbaf1759b096f88eb0fb2d09d4d9fcd97f22f` at executable revision `ab4dfb16846ebe7dff9867b9a0864870d7893f0f`. This is a separate simulator with a different tie policy: in terminal mode an exactly coincident deposit can rescue the account. A strictly later deposit cannot.

For initial 1, rate −0.25 and withdrawal 1, the crossing is `4*ln(1.25)`. The represented jump time `0.8925742052568391` is strictly later by a high-precision comparison, but the current terminal simulator reports completion and accepts the deposit after its segment balance rounds to zero. Separately, the interpolator fails with `ValueError` for symmetric endpoints `(-M,M,M,-M)` even though the exact crossing is zero, where M is the largest float.

Replay from the book root:

```python
import sys
from decimal import Decimal, localcontext
sys.path.insert(0, "chapter-19/code")
from section_19_07 import simulate_jumps, linear_crossing

t = .8925742052568391
with localcontext() as ctx:
    ctx.prec = 100
    assert Decimal(t) > 4*Decimal("1.25").ln()
print(simulate_jumps(1.,-.25,1.,t,[(t,1.)]))
m = sys.float_info.max
try:
    print(linear_crossing(-m,m,m,-m))
except ValueError as error:
    print(type(error).__name__, error)
```

Next: independently check actual terminal, exact-coincidence and nonterminal behavior, and finite interpolation across extreme endpoints. Reuse compatible arithmetic without importing Section 19.9's different exact-tie policy. No Section 19.7 source changed in this batch.
