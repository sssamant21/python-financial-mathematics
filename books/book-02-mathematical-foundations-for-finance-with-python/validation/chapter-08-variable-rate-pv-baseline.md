# Next checkpoint: Section 8.4 variable-rate PV scaling

Source revision `9d138bf2bd1fa0ab5806d0ec3e9202b0f26f2cf1`; Section 8.4 blob `8ec9d1318064214866472b83691a602f3d4a5f0e`. The callback/centered changes did not change these financial functions.

Actual source probes:

```python
import sys
from section_8_04 import variable_rate_pv, variable_rate_pv_derivative, rate_from_factor
M = sys.float_info.max
rate_from_factor(485.0)  # 1.0
variable_rate_pv(M, 1000.0, 485.0)  # 0.0
variable_rate_pv_derivative(M, 1000.0, 485.0)  # -0.0
variable_rate_pv(0.0, M, -M)  # nan
variable_rate_pv_derivative(0.0, M, -M)  # nan
```

For the returned represented rate 1.0, an independent complete Decimal reference gives PV 9.125016462967946e-127 and factor sensitivity -1.8250032925935896e-126 using the represented 0.002 coefficient. Both roundings agree at 200 and 400 decimal digits. Separate exponential evaluation currently loses these finite results to underflow. For zero amount, the model's value and sensitivity are zero for finite inputs, while the source forms zero times an overflowing exponential and returns NaN.

Reproduce the independent nonzero reference by computing `Decimal.from_float(M) * Decimal(-1000).exp()` in local contexts at precisions 200 and 400, then multiply that unrounded value by `-1000 * Decimal.from_float(0.002)` before conversion to float. Zero-amount references follow algebraic identities without evaluating the enormous exponential.

Next batch should establish complete value/sensitivity scaling and zero identities while preserving input domains and the intended factor-to-rate rounding convention. The current references deliberately use the helper's returned rate; they do not silently replace that with an exact affine rate. Discrete compounding, nested polynomial, other copies and independent manual review remain open. Resume here rather than repeating completed callback examples. This baseline is exploratory retained failure evidence, not corrected passes or external approval.
