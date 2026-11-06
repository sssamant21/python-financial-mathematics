# Section 19.5 — Amplification boundary checkpoint

Three discrepancies were reproduced in the unchanged amplification functions at executable revision `c7fb27159683d94cdf41aa1f6bd8a1cb6e5bd946`. The decay inequality is strict on the complete mathematical factor for the represented inputs; the displayed factor can round to a boundary.

| Rate and step | Exact factor, with q = 2^-52 and d the smallest positive float | Observed factor / stable |
|---|---|---|
| `(-2*(1-q), 1+q)` | `-1 + 2*q*q` (stable) | -1 / false |
| `(-d, d)` | `1 - d*d` (stable) | 1 / false |
| `(-(1-q), 1+q)` | `q*q` (stable) | 0 / true |

Replay from the book root:

```python
import math, sys
from fractions import Fraction
sys.path.insert(0, "chapter-19/code")
from section_19_05 import linear_amplification, stable_linear_decay

q, d = 2.**-52, math.ulp(0.)
for r, h in [(-2*(1-q),1+q), (-d,d), (-(1-q),1+q)]:
    factor = 1+Fraction(r)*Fraction(h)
    print(float(factor), abs(factor)<1,
          linear_amplification(r,h), stable_linear_decay(r,h))
```

Next: check complete-factor rounding separately from exact stability classification; include true equality, just-outside boundaries and actual represented Euler paths whose iterates can still round to neutral behavior. The current batch does not change these functions.
