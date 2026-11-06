# Section 21.7 — Account transition baseline checkpoint

Four preliminary probes at source revision `bc29b0d67dfd61b3d522d36d956b768101fee0ab` (Section 21.7 lab blob `463b82ea88ea1e0ca318fe65f2e519914a60a1de`) all raised `OverflowError` even though the analytic final balance is finite.

| Inputs (initial, rate, flow, years), with `M = sys.float_info.max` | Expected | Derivation |
|---|---:|---|
| `(-M, 0, M, 2)` | `M` | At zero rate the full expression is `-M + 2M = M`. |
| `(1, 1024, -1024, 1)` | `1` | The initial balance is exactly at equilibrium, so the exponential coefficient is zero. |
| `(1, -M, M, 2)` | `1` | The initial balance again equals the equilibrium, even though the exponent cannot be stored as a float. |
| `(0, M, 0, 2)` | `0` | The zero state with zero flow is identically zero. |

Replay from the book root at the pinned revision:

```python
import sys
sys.path.insert(0, "chapter-21/code")
from section_21_07 import transition

M = sys.float_info.max
for inputs, expected in [
    ((-M, 0., M, 2.), M),
    ((1., 1024., -1024., 1.), 1.),
    ((1., -M, M, 2.), 1.),
    ((0., M, 0., 2.), 0.),
]:
    try:
        actual = transition(*inputs)
    except (ValueError, OverflowError) as error:
        actual = type(error).__name__
    print(inputs, expected, actual)
```

Next: build the independent account oracle and retain these baseline failures with its own rerun. Add non-equilibrium scaled growth/flow and genuine overflow cases, preserve the unconstrained final-state model and the pending status fields, and test the actual Section 21.9 account field. Reconcile the output underflow policy against the Section 21.7 contract before borrowing behavior from another chapter. These probes have no correction or acceptance disposition.
