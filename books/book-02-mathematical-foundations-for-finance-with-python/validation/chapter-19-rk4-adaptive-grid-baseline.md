# Section 19.6 — Adaptive RK4 represented-clock checkpoint

The actual adaptive driver at `22336bded4cb65dce8a0557561e7095978fd403f` (lab blob `09663f87e719cbd81c8e4ab37934b9ae8969ce6a`) can report a time advance different from the interval used by its accepted state, even when the two represented half-step lengths are exactly equal and sum to the proposal. This controlled probe replaces only the controller multiplier to isolate the clock; the solver and its callback stages are real.

For `y'=1`, `y(0)=-1`, the exact state at a reported time `t` is `t-1`. The first accepted trial lands at `t=1`. The next proposes three quarters of `ulp(1)`, which rounds the endpoint up by a whole ulp. Observed: two accepted trials, 24 evaluations, final time `1.0000000000000002` and state `1.6653345369377348e-16`. The exact state at that reported time is `2.220446049250313e-16`. All eight half-path callback times of the second trial are `1.0`; only its full-path endpoint reaches the reported time.

Replay from the book root:

```python
import math, sys
from unittest.mock import patch
sys.path.insert(0, "chapter-19/code")
import section_19_06 as lab

u = math.ulp(1.)
seen = []
def rhs(t, y):
    seen.append(t)
    return 1.
with patch.object(lab, "_step_factor", return_value=.75*u):
    out = lab.adaptive_rk4(rhs, -1., 1.+4*u, initial_step=1.,
                           min_step=u/8, max_attempts=2)
print(out, seen[12:], out["final_time"]-1.)
```

Next: require the full and doubled trials to share the represented endpoint and account for the same elapsed interval, or report an explicit resolution limit when a usable split cannot be made. Check no-progress and final-interval cases, and preserve acceptance, rejection and evaluation-count behavior. This checkpoint does not change the adaptive driver.
