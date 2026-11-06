# Section 19.7 — Standalone depletion-time boundary checkpoint

The simulator now uses a separate unrounded event-order calculation, but the public `depletion_time` function still has two reproducible failures at `f8e663fe51f1105dff594e5219320214076bafa8`:

- For initial `1+q`, rate `1-q` and withdrawal 1, with `q=2**-52`, the ratio is exactly `1-q*q`. The crossing is finite: `-ln(q*q)/(1-q)`, which rounds to `72.08730677823432`. The public helper returns `None` because its intermediate product rounds to 1.
- With zero rate, largest finite float as initial balance, and the smallest positive float as withdrawal, the exact quotient is beyond float range. The public helper returns infinity rather than reporting a range failure.

Replay from the book root:

```python
import math, sys
from decimal import Decimal, localcontext
sys.path.insert(0, "chapter-19/code")
from section_19_07 import depletion_time

q = 2.**-52
with localcontext() as ctx:
    ctx.prec = 150
    print(float(-(Decimal(q)**2).ln()/Decimal(1-q)),
          depletion_time(1+q,1-q,1.))
print(depletion_time(sys.float_info.max,0.,math.ulp(0.)))
```

Next: verify public depletion-time classification and finite reporting at both range ends, reconcile standalone rounding policy with the shared kernel, and check the actual Section 19.7 assessment fields. Preserve the separate simulator's time-zero and coincidence rules. No standalone depletion-time behavior changed in this batch.
