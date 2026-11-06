# Section 19.1 introductory model range: initial failures

[Section 19.3 follow-up](chapter-19-linear-applied-range-followup.md) checks the applied Section 19.3 entry points. The next COV-84 obligation concerns the separate introductory implementation in Section 19.1.

Observed on source [`bf9d4fccf807a1ee631a737cb4b20e507808e0cc`](https://github.com/sssamant21/python-financial-mathematics/blob/bf9d4fccf807a1ee631a737cb4b20e507808e0cc/books/book-02-mathematical-foundations-for-finance-with-python/chapter-19/code/section_19_01.py), module blob `6a7c1ab15f03113cbe1ca6933d3dcf822a936374`:

| Probe | Expected or observed boundary | Actual |
|---|---|---|
| `growth(math.ulp(0.0), 800.0, 1.0)` | Decimal scaling gives a finite balance of approximately `1.3470080137759474e+24` | `OverflowError: math range error` |
| `account(1.0, 800.0, -800.0, 1.0)` | The initial state is the exact equilibrium, so balance stays `1.0` | `OverflowError: math range error` |
| `effective_from_continuous(-1000.0)` followed by its inverse | The mathematical effective rate is strictly greater than `-1`; binary64 rounds it to the inverse's excluded endpoint | Forward conversion returns `-1.0`; inverse raises `ValueError: effective rate must exceed -1` |

```sh
cd books/book-02-mathematical-foundations-for-finance-with-python/chapter-19/code
python - <<'PY'
import math
from decimal import Decimal, localcontext
import section_19_01 as m

least = math.ulp(0.0)
with localcontext() as context:
    context.prec = 90
    print("growth reference:", float(Decimal(least) * Decimal(800).exp()))
for operation, args in (
    (m.growth, (least, 800.0, 1.0)),
    (m.account, (1.0, 800.0, -800.0, 1.0)),
    (m.effective_from_continuous, (-1000.0,)),
    (m.continuous_from_effective, (-1.0,)),
):
    try:
        print(operation.__name__, operation(*args))
    except (ValueError, OverflowError) as exc:
        print(operation.__name__, type(exc).__name__, str(exc))
PY
```

The first two probes reproduce numerical defects. The rate pair exposes a contract boundary: reconcile the published policy before choosing the forward behavior and test the nearest valid effective rate as well. Extend the follow-up to genuine overflow, the introductory Euler path and actual assessment fields. These probes are a baseline; no Section 19.1 fix or comprehensive review is claimed.

### Additional baseline observations at the same source

- `euler_account(2.0, 1e308, -1e308, 0.5, 1)` raised `ValueError: Euler balance must be finite`. The exact affine step is `2 + (2r-r)/2 = 2+r/2` with the represented rate `r=1e308`, which rounds to `5e307`.
- `math.nextafter(-1.0, 0.0)` successfully round-trips; the intermediate continuous rate is approximately `-36.7368005696771`.
- The actual `assessment()` returns the Euler balances but no absolute errors, which the manuscript's Numerical comparison asks readers to report. The analytic growth and the geometric Euler values, evaluated with the represented rate in 80-digit Decimal, give absolute errors of about `0.5487926644431149`, `0.27534088891683794` and `0.1379079465768582` for 10, 20 and 40 steps. Determine whether the source report should include those fields and test them if added.
