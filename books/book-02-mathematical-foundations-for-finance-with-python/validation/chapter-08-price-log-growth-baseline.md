# Next checkpoint: Section 8.4 price and log-price growth

Revision `76208b8f944cf6ab706ae75f94cc0329d1f3dbfe`; Section 8.4 blob `7fc5617f5953e85890d0b61bffa92f383b6148f9`. Nested-derivative changes do not alter these functions. [Five actual price/log-growth probe pairs](chapter-08-price-log-growth-baseline.json).

At time 1e104, `price` returns infinity; at maximum finite time it raises OverflowError. Exact rational 100·b³ cannot round to finite binary64 in either case, where b is the helper's currently rounded base 1+represented(0.02)·t. Ordinary time zero, 1e103 and the first float above -50 give finite outputs matching the selected complete-price references.

Selected `log_price_growth` outputs all match exact represented(0.06)/b references, including a nonzero subnormal at maximum finite time. No log-growth defect is claimed from this screen. The next batch should establish the price finite-output/overflow and accuracy policy, test adjacent price overflow inputs, preserve the t>-50 domain, and document the shared base/coefficient convention.

Reproduce actual outputs with `price(t)` and `log_price_growth(t)` at the five JSON times. References use Fraction(b) and Fraction(0.06), so they deliberately preserve the current rounded affine base. Near -50, changing that base to an exact affine expression would materially change results and must not be done silently. Distinguish the model's represented 0.06 coefficient from any newly proposed exact 3·represented(0.02) numerator policy.

Remaining earlier helper copies and independent manuscript/math review stay open under COV-51. Resume here without repeating completed nested-power or count-conversion cases. No reviewer or release/platform gate is closed by these observations.

## Finite-output bound to verify in the next batch

For binary64 inputs under the current rounded affine convention, the smallest accepted time is nextafter(-50,+infinity), whose actual base is 2^-53. Multiplication by positive represented 0.02 and addition of one are monotone, so larger accepted times cannot produce a smaller base. The largest accepted time is maximum float, whose actual base is 3.595386269724631e306, safely finite. Consequently represented(0.06)/b stays between approximately 1.668805393880401e-308 and 5.404319552844595e14: positive and finite, including the subnormal lower endpoint. This supplies an endpoint/monotonicity argument for the log-growth finite-output scope; the next batch should retain actual guard and endpoint checks and explicitly state its binary64 rounding assumptions.
