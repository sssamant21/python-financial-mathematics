# Section 21.4 central-difference range: baseline

Next COV-90 obligation: the finite-difference helper still forms each PV and the denominator as separate floats. The prior [analytical scaling checks](chapter-21-capstone-sensitivity-range-followup.md) left the stencil guards unchanged.

On [pinned source `44c6a0bcd5d5e8e6ab8ac84e9691c89610d3ed3e`](https://github.com/sssamant21/python-financial-mathematics/blob/44c6a0bcd5d5e8e6ab8ac84e9691c89610d3ed3e/books/book-02-mathematical-foundations-for-finance-with-python/chapter-21/code/section_21_04.py), blob `bf4700160749afdf39d28a21ecda3d5c981f0adf`, two probes have finite complete stencil values but raised `OverflowError`.

| Amount, rate, years, step | Independent complete stencil | Actual |
|---|---:|---|
| maximum finite float, 0, 0.5, 0.5 | −9.08238855415417e+307 | result exceeds float range |
| 1, 0, 1e−308, 1e308 | −1.1752011936438015e−308 | central-difference denominator exceeds float range |

Run from `chapter-21/code` at the pinned revision:

```sh
python - <<'PY'
import sys
from decimal import Decimal as D, localcontext
from section_21_04 import central_difference

for a, t, h in [(sys.float_info.max, .5, .5), (1., 1e-308, 1e308)]:
    with localcontext() as c:
        c.prec = 90
        z = D(t) * D(h)
        expected = float(D(a) * ((-z).exp() - z.exp()) / (2 * D(h)))
    try:
        result = central_difference(a, 0., t, h)
    except OverflowError as exc:
        print(expected, type(exc).__name__, exc)
    else:
        print(expected, result)
PY
```

Resume with independent Decimal stencil references, including cancellation, genuine range failures and the actual Section 21.9 diagnostic. Reconcile perturbation rounding and domain guards explicitly. No stencil correction is claimed in this checkpoint.
