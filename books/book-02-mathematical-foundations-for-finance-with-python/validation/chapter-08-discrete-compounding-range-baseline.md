# Next checkpoint: Section 8.4 discrete-compounding scaling

Source revision `21ebbc28a1b08b93c9103d791c90d6bab15ec815`, Section 8.4 blob `92b39e5b48954d60285ed86629d29443ed85b841`. Variable-rate PV corrections did not change the discrete-compounding functions. [Actual probes and independent references](chapter-08-discrete-compounding-range-baseline.json).

With principal maximum float, periods_per_year=1, years=1000 and factor=-672.1205588285577, the returned base is 0.36787944117144233. Actual value is 0 and sensitivity NaN; complete references are approximately 9.125016462968255e-127 and 2.480436643567624e-126.

With principal minimum subnormal, periods_per_year=1, years=1000 and factor=1678.281828459045, the returned base is 2.718281828459045. Both helpers raise OverflowError even though complete value/sensitivity references are approximately 9.733444572999646e110 and 3.580734150188318e110.

With zero principal, periods_per_year=1, years=1000 and factor maximum float, the accepted base is positive but both helpers raise OverflowError instead of preserving the model's zero identities.

References evaluate p·b^1000 and p·1000·represented(0.001)·b^999 with Decimal at precisions 200 and 400; rounded results agree. The zero-principal references follow algebra without forming huge powers. These references deliberately use the current returned base; the next batch must reconcile nominal-rate/base and exponent rounding conventions before changing behavior.

Reproduce each probe with `discrete_future_value(p, 1, 1000.0, factor)` and `discrete_future_value_derivative(p, 1, 1000.0, factor)`; derive b as `1 + nominal_rate(factor)`. Preserve invalid base, period-count and quantity behavior while deriving complete scaling and true final overflow expectations. Large integer period counts, nested polynomial, price/log-growth helpers and independent manual review also remain open under COV-51. Resume here rather than repeating completed PV examples.
