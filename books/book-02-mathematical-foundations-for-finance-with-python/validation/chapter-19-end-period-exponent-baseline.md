# Section 19.8 — End-period exponent boundary checkpoint

At executable revision `59f713d346fbcbf14e7125902637cd2f6e2c56e4` (Section 19.8 blob `8300579fb2fe18cb70f6ba73c7308074e2b0de2d`), the actual finite-payment function rejected all four probes below with `ValueError: end-period exponent exceeds supported evaluation range`. This is the current documented restriction. The cases identify possible extensions of the supported domain; they do not misrepresent the existing restriction as an undocumented failure.

For `n` equal end-period payments with `x = rate * years`, the exact balance is initial times `exp(x)`, plus each payment `flow * years / n` times the sum of `exp(j*x/n)` for integers `j` from 0 to `n-1`.

| Inputs (initial, rate, flow, years, n) | Expected rounded balance if the scope is extended | Reference |
|---|---:|---|
| `(1, -4001, 2, 1, 1)` | 2 | The final payment of 2 is undiscounted; the initial term is negligible. |
| `(1, -4001, 2, 1, 2)` | 1 | The final payment of 1 is undiscounted; the preceding payment and the initial term are negligible. |
| `(0, 4001, 2, 1, 1)` | 2 | No initial balance and just one undiscounted final payment. |
| `(1, 4001, -4001, 1, 10**2000)` | 1 | With `z = 4001/n` and `k = z/expm1(z)`, the balance is `1 + (1-k)*(exp(4001)-1)`. Here `0 < 1-k < z` and `exp(4001) < 10**1738`, so the positive correction is below `10**-258`. |

Replay from the book root at the pinned revision:

```python
import sys
sys.path.insert(0, "chapter-19/code")
from section_19_08 import end_period_contributions

for args, expected in [
    ((1., -4001., 2., 1., 1), 2.),
    ((1., -4001., 2., 1., 2), 1.),
    ((0., 4001., 2., 1., 1), 2.),
    ((1., 4001., -4001., 1., 10**2000), 1.),
]:
    try:
        actual = end_period_contributions(*args)
    except (ValueError, OverflowError) as error:
        actual = f"{type(error).__name__}: {error}"
    print(expected, actual)
```

Next: investigate a bounded extension, with separate limits for the final-payment identity, large negative total versus per-period exponents, exact zero or cancellation, and genuinely unrepresentable balances. Retain the Chapter 19 underflow contract and disclose any positive-exponent ranges that remain unsupported. This checkpoint changes no Chapter 19 numerical behavior.
