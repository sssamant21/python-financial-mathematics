# Section 8.1 earlier derivative helpers: guard baseline

COV-51 explicitly leaves earlier derivative copies open. The completed [Section 8.8 guard follow-up](chapter-08-helper-guards-followup.md) did not change these entry points.

At [pinned source `2a87994b660c5ea1f600a9187edf097d3ca70dce`](https://github.com/sssamant21/python-financial-mathematics/blob/2a87994b660c5ea1f600a9187edf097d3ca70dce/books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/section_8_01.py), blob `a46ea7d910a6ec7bf077ac5c7675d46a2aa8db48`:

- `forward_difference(callback,1.,1e-30)` and `centered_difference(callback,1.,1e-30)`, with callback `x*x`, each return `0.0` and invoke the callback twice at `1.0`. The perturbation has collapsed to the base point. The exact quadratic derivative is 2, but those two identical samples cannot estimate it.
- `centered_difference(lambda x: math.copysign(1e308,x),0.,.5)` returns infinity from finite callback values. The complete stencil is outside finite float range; an explicit range error is needed rather than an unvalidated result.

Replay from `chapter-08/code`:

```python
import math
from section_8_01 import forward_difference, centered_difference

for method in (forward_difference, centered_difference):
    calls=[]
    def quadratic(x):
        calls.append(x)
        return x*x
    print(method.__name__,method(quadratic,1.,1e-30),calls)
print(centered_difference(lambda x: math.copysign(1e308,x),0.,.5))
```

Next: check representability before callback execution, finite returned estimates, actual callback arguments and independent complete-stencil references. Preserve the earlier helper's signed nonzero-step convention unless its manuscript warrants a domain change. Include finite complete results hidden by separate subtraction/denominator overflow and genuine result-range failures. Other Section 8 copies and financial-PV helpers remain separate obligations.
