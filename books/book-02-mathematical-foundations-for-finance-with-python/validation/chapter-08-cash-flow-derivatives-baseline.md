# Next checkpoint: signed Section 8.6 cash-flow derivatives

Executable revision `37b29e56354a02fbccb747ff0c77bbd45cd67edd`. [Five actual aggregate probes and references](chapter-08-cash-flow-derivatives-baseline.json).

Opposite same-horizon flows cancel exactly but derivative sums become NaN after term overflow. Three zero-horizon flows have exact aggregate value equal to maximum float, yet one order overflows while a reordered control works. Signed tiny payments at large discount-growth horizons have finite complete aggregate derivatives but raise OverflowError. Two discounted unit flows have a zero-rounded price alongside nonzero subnormal first/second derivatives that are lost.

Independent complete signed aggregate references agree at Decimal 200/400 digits. Zero-rate cancellation/order references also follow exact signed sums. Actual calls use one-shot iterators and replay identically beside the pinned hash-verified source/dependency. JSON retains runnable code and explicit zero signs; zero-sign policy itself remains to be reconciled.

Next establish complete aggregate scaling/output contracts before term rounding, preserving signed payments, nonnegative horizons, rate-first/empty-input validation and one-shot iterator behavior. Do not impose the single-payment nonnegative restriction on signed cash flows or assume finite aggregates require individually representable terms. Polynomial, sampled-second-difference, resource-limit and independent-review obligations remain open.
