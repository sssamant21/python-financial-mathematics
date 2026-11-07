# Section 8.3 analytic product and quotient range: baseline

COV-51 still includes other derivative helpers and numerical ranges. On [pinned source `d702d2761735c11ab501900c899cae4557742a09`](https://github.com/sssamant21/python-financial-mathematics/blob/d702d2761735c11ab501900c899cae4557742a09/books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/section_8_03.py), blob `b744c9664be06c85e976a7e84a2d34fdf0bfb1c4`, these distinct analytic helpers fail finite complete-result cases:

| Helper inputs at x=0 | Exact expectation | Actual |
|---|---|---|
| u=1, du=M, v=2, dv=−M | M·2 − M = M | infinity |
| u=du=v=dv=M | (M²−M²)/M² = 0 | OverflowError during denominator squaring |

Here M is the largest finite float and each callback returns the stated constant. The first case should preserve a finite complete derivative; the second has a nonzero denominator and an exact cancellation before division. These are separate functions from Section 8.1's sampled-stencil helpers.

```python
import sys
from section_8_03 import product_derivative, quotient_derivative

M=sys.float_info.max
for function,args in [
    (product_derivative,(lambda x:1.,lambda x:M,lambda x:2.,lambda x:-M,0.)),
    (quotient_derivative,(lambda x:M,lambda x:M,lambda x:M,lambda x:M,0.)),
]:
    try:
        print(function.__name__,function(*args))
    except Exception as exc:
        print(function.__name__,type(exc).__name__,str(exc))
```

Next: derive exact complete product/quotient expectations, check callback validation and single-evaluation order, zero-denominator rejection and genuine final overflow. Preserve the public domain and distinguish these helper changes from the financial average-cost/coverage/PV variants and the remaining copied centered difference.
