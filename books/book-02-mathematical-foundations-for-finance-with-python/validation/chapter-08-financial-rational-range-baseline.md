# Section 8.3 financial rational examples: range baseline

The product/quotient callback helpers are covered by the [preceding follow-up](chapter-08-product-quotient-range-followup.md). COV-51 still leaves the distinct financial examples' ranges open.

At [pinned source `2f6b47559fc7baa82e59772bbdfbd6445e5374e1`](https://github.com/sssamant21/python-financial-mathematics/blob/2f6b47559fc7baa82e59772bbdfbd6445e5374e1/books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/section_8_03.py), blob `fe971b85ef42579e94c7f064e3e2729b5b48cd13`, these two finite represented-input references fail:

| Helper and input | Independent complete result | Actual |
|---|---:|---|
| average_cost(maximum finite float) | approximately 1.7976931348623158e307 | infinity |
| coverage_ratio_derivative(1e154) | approximately 1.111111111111111e−307 | OverflowError during squaring |

The references use exact Fraction arithmetic on the represented input and the represented 0.1 coefficient, rather than separate float numerator or denominator terms.

```python
import sys
from fractions import Fraction as Q
from section_8_03 import average_cost, coverage_ratio_derivative

q=sys.float_info.max
cases=[
    (average_cost,q,float(Q(500)/Q(q)+10+Q(.1)*Q(q))),
    (coverage_ratio_derivative,1e154,float(Q(100)/(50+3*Q(1e154))**2)),
]
for function,value,reference in cases:
    try:
        print(function.__name__,reference,function(value))
    except Exception as exc:
        print(function.__name__,reference,type(exc).__name__,str(exc))
```

Next: examine the average-cost value/derivative and coverage-ratio value/derivative contracts with complete rational references, true final range failures and declared domains. Reconcile the coverage helper's rounded zero-denominator guard separately from exact near-pole arithmetic before choosing behavior. Discounted-payment callbacks and the copied centered-difference helper remain separate work.
