# Section 19.6 — Exact account reference range checkpoint

The account reference used by the Section 19.6 assessment has its own numerical path. Three finite-result cases failed at revision `f462da2d7ff63750780e72884557ccfd4fa7df98` (lab blob `a37d8f4fe5221536d50877dc8be4d51d07195d48`).

| Inputs | Independently derived expectation | Observed |
|---|---|---|
| `(3, 900, -2700, 1)` | 3, since `r*a+u=0` gives an exact equilibrium | `OverflowError: math range error` |
| `(-M/2, 0, M/2, 3)` | M by the zero-rate affine identity; M is the maximum float | `ValueError: balance must be finite` |
| `(d, 735, 0, 1)` | `7.947469241534912e-05`, using the smallest positive float d times the high-precision exponential | `OverflowError: math range error` |

Replay from the book root:

```python
import math, sys
from decimal import Decimal, localcontext
sys.path.insert(0, "chapter-19/code")
from section_19_06 import exact_account

m, d = sys.float_info.max, math.ulp(0.)
with localcontext() as ctx:
    ctx.prec = 100
    scaled = float(Decimal(d)*Decimal(735).exp())
for args, expected in [((3.,900.,-2700.,1.),3.),
                       ((-m/2,0.,m/2,3.),m), ((d,735.,0.,1.),scaled)]:
    try:
        actual = exact_account(*args)
    except (ValueError, OverflowError) as error:
        actual = f"{type(error).__name__}: {error}"
    print(expected, actual)
```

Next: correct the complete finite balance calculation and check the actual Section 19.6 assessment reference fields against independent expectations. Reuse validated arithmetic where its contract fits, and explicitly reconcile true overflow and underflow behavior. No account-reference code changed in this batch.
