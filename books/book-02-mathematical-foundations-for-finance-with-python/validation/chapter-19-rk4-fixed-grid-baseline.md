# Section 19.6 — Fixed RK4 grid horizon checkpoint

These probes ran against Section 19.6 blob `184997ea83472d3ddaace41a4293aeea39e12318`, published at `eaed8250b3400bedc612aa415c3cecb8f23b2af5`. The adaptive driver now checks that equal represented halves cover its proposed step; the fixed driver still rounds a single uniform step and reports the requested horizon independently of the actual grid.

Let `d` be the smallest positive float and `M` the maximum finite float. For `y'=M` from zero, the exact terminal balance at `T` is `M*T`. These cases quantify both directions of the error:

| Requested horizon | Steps | Expected balance at that horizon | Actual balance | Last callback time |
|---|---:|---:|---:|---|
| 3d | 2 | 2.6645352591003753e-15 | 3.5527136788005005e-15 | 4d |
| 5d | 4 | 4.440892098500625e-15 | 3.5527136788005005e-15 | 4d |

Both reports say `completed` and return the requested horizon as `final_time`. The first overshoots and the second stops short. Replay from the book root:

```python
import math, sys
sys.path.insert(0, "chapter-19/code")
from section_19_06 import fixed_rk4

d, m = math.ulp(0.), sys.float_info.max
for units, count in ((3, 2), (5, 4)):
    seen = []
    def rhs(t, y):
        seen.append(t)
        return m
    horizon = units*d
    print(m*horizon, fixed_rk4(rhs, 0., horizon, count), seen[-1])
```

Next: establish when a represented fixed grid can cover its horizon with strictly increasing endpoints. Independently check callback times and complete constant-derivative integration, including inexact and degenerate partitions, while retaining the ordinary convergence and evaluation-count checks. This checkpoint does not change fixed-grid behavior.
