# Section 19.9 — Rounded event-time tie checkpoint

The unchanged simulator at `5621a516346213dd09780c0eba7c49a402aee143` (lab blob `844e5e139a6a89790b28f739346b8e1060d38eb4`) compares a rounded depletion time with the next jump interval. Two deposits strictly before depletion were skipped as if coincident:

| Inputs (initial, rate, flow, horizon, jump) | Independent event order | Observed |
|---|---|---|
| `(1, 0, -(1-q), 1+q, +1 at horizon)`, q = 2^-52 | Pre-jump balance is `1-(1-q)(1+q)=q*q>0`; jump occurs first | depleted; zero jumps applied |
| `(1, 0.5, -1, 1.3862943611198906, +1 at horizon)` | Crossing is `2*ln(2)`, strictly above the represented horizon; jump occurs first | depleted; zero jumps applied |
| `(1, 0, -1, 1, +1 at horizon)` | Exact equality; documented future depletion-first policy applies | depleted; zero jumps applied |

Replay from the book root:

```python
import sys
from decimal import Decimal, localcontext
sys.path.insert(0, "chapter-19/code")
from section_19_09 import simulate

q = 2.**-52
with localcontext() as ctx:
    ctx.prec = 100
    assert Decimal(1.3862943611198906) < 2*Decimal(2).ln()
for rate, flow, t in [(0.,-(1-q),1+q), (.5,-1.,1.3862943611198906), (0.,-1.,1.)]:
    result = simulate(1.,rate,flow,t,[(t,1.)])
    print(result["status"],result["applied_jumps"],result["events"])
```

Next: classify event order before rounding reported timestamps, preserve exact-equality and time-zero policies, and check the actual simulation and log against zero-rate and high-precision nonzero-rate oracles. No Section 19.9 behavior changed in this batch.
