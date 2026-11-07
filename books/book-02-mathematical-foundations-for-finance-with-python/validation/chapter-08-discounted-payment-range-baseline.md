# Section 8.3 discounted-payment callbacks: range baseline

The [rational financial examples](chapter-08-financial-rational-range-followup.md) are separate from the discounted-payment callback wrappers. COV-51 leaves those helpers' numerical range open.

At [pinned source `e674373645a4b9787b3a412fd8262ff9a4c30fdf`](https://github.com/sssamant21/python-financial-mathematics/blob/e674373645a4b9787b3a412fd8262ff9a4c30fdf/books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/section_8_03.py), blob `32a2e11547ddee386176a8388f80294987e58b13`:

| Entry point and constant callbacks | Independent expectation | Actual |
|---|---:|---|
| discounted_value(1000,1,payment=M,payment_derivative=0) | approximately 9.125016462967946e−127 | 0 |
| discounted_value(1000,−1,payment=0,payment_derivative=0) | 0 | OverflowError from the unscaled exponential |
| discounted_value_derivative(0,M,payment=2,payment_derivative=M) | −M | negative infinity |

M is the largest finite float. The first expectation scales a 100-digit Decimal exponential by the represented M before converting to float. The second is the zero-payment identity. The third is the exact complete product-rule coefficient M−2M at a zero horizon.

```python
import sys
from decimal import Decimal as D, localcontext
from section_8_03 import discounted_value, discounted_value_derivative

M=sys.float_info.max
with localcontext() as c:
    c.prec=100
    print(float(D(M)*D(-1000).exp()))
for function,args in [
    (discounted_value,(1000.,1.,lambda t:M,lambda t:0.)),
    (discounted_value,(1000.,-1.,lambda t:0.,lambda t:0.)),
    (discounted_value_derivative,(0.,M,lambda t:2.,lambda t:M)),
]:
    try:
        print(function.__name__,function(*args))
    except Exception as exc:
        print(function.__name__,type(exc).__name__,str(exc))
```

Next: check complete discount scaling and product-rule coefficients against independent references, actual callback arguments/count/order, zero identities, invalid preflight and genuine final overflow. Preserve the value wrapper's unused derivative-argument behavior; do not add callback execution merely for validation. The copied centered-difference and Section 8.1 financial helpers remain separate obligations.
