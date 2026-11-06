# Section 19.3 — Applied linear-account range checkpoint

The unchanged Section 19.3 source blob `5d369547d21fe5e3c6ed6b5839562944a8740caa` at executable revision `2dccee14e57ace03c2fc58a3226ff7d4d19fc7d5` rejected three finite results. M is the largest finite float.

| Entry point and input | Independent expectation | Observed |
|---|---|---|
| `variable_rate_no_flow(7,-M,M,2)` | 7, since the integrated exponent is exactly `-2*M+2*M=0` | `ValueError: balance must be finite` |
| `piecewise_account(-M,0,[(M,2),(-M,1)])` | Segment balances M then zero, by the zero-rate affine identity | `ValueError: balance must be finite` |
| `euler_account(-M,-2,-M,1,1)` | Zero, since the full Euler increment is M | `ValueError: Euler balance must be finite` |

Replay from the book root:

```python
import sys
sys.path.insert(0, "chapter-19/code")
from section_19_03 import euler_account, piecewise_account, variable_rate_no_flow

m = sys.float_info.max
for fn,args in [(variable_rate_no_flow,(7.,-m,m,2.)),
                (piecewise_account,(-m,0.,[(m,2.),(-m,1.)])),
                (euler_account,(-m,-2.,-m,1.,1))]:
    try:
        print(fn.__name__,fn(*args))
    except ValueError as error:
        print(fn.__name__,type(error).__name__,error)
```

Next: check these actual Section 19.3 callers and assessment outputs against independently derived references. Reuse compatible complete arithmetic while preserving domain, segment order and represented-state boundaries. No Section 19.3 code changed in this batch.
