# Section 8.1 initial PV helpers: range baseline

The completed Section 8.1 callback guards left its distinct financial functions unchanged. COV-51 still includes those ranges.

At [pinned source `0b109a17f2ee256a3cdffeeeffb0417720bcf3ed`](https://github.com/sssamant21/python-financial-mathematics/blob/0b109a17f2ee256a3cdffeeeffb0417720bcf3ed/books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/section_8_01.py), blob `5b7721f38b5c4416c184df1a6d013c9d4394ec6d`, three finite results are lost:

| Entry point | Independent expectation | Actual |
|---|---:|---:|
| present_value(M,1,1000) | 9.125016462967946e−127 | 0 |
| present_value_derivative(M,1,1000) | −9.125016462967946e−124 | negative zero |
| stable_present_value_difference_quotient(1000,0,u,0.5) | −4.94e−321 | negative zero |

M is the largest finite float; u is the least positive float. The first references scale the full expression before converting to float. The last retains the exact represented product of horizon and step rather than rounding that product to zero before expm1.

```python
import math
import sys
from decimal import Decimal as D, localcontext
from section_8_01 import (present_value, present_value_derivative,
                         stable_present_value_difference_quotient)

M=sys.float_info.max
u=math.ulp(0.)
with localcontext() as c:
    c.prec=1000
    print(float(D(M)*D(-1000).exp()))
    print(float(-1000*D(M)*D(-1000).exp()))
    print(float(D(1000)*((-D(u)*D(.5)).exp()-1)/D(.5)))
print(present_value(M,1.,1000.))
print(present_value_derivative(M,1.,1000.))
print(stable_present_value_difference_quotient(1000.,0.,u,.5))
```

Next: independently derive complete PV, derivative and stable difference-quotient references, preserve the nonnegative amount/horizon and signed nonzero-step domains, and distinguish zero identities, representable underflowed terms and true final overflow. The copied Section 8.3 centered difference and other early derivative functions remain separate obligations.
