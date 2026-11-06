# Section 12.9 — Duration review

Baseline: `06adf5880dc121bf35e30785971b1149d94552d9`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Answers](ANSWERS.md).

The runner executes the named script from the sole exact Python fence and compiles it in isolation. Both documented commands and all 12 existing methods passed on the original and corrected source in the recorded Linux CPython runtime. Eight of 47 additional predicates failed initially, including exact three-year zero-coupon duration (ordinary float rounding drift). All 47 passed after correction. Counts: one workflow, 18 local answers, one separately scoped mini-project and no historical unique additions.

The independent backward valuation gives exact rational prices. Symmetric differences of the backward values supply a benchmark for modified and Macaulay duration; direct individual-flow PV checks every source weight. The five project coupons run through the source at 6% and at the +50-bp repricing point. The exact demo covers one coupon only.

F86: boolean shocks passed the input contract. F54 recurred in weighted-sum and shock intermediate range loss, discount underflow and unsupported float results. The source now uses normalized rational weights, applies the shock before float reporting and rejects invalid inputs. The strict zero-coupon time identity now holds for the exact three-year fixture.

Python 3.9+ and its standard library suffice, without prior files. This is an equal-period teaching model for fixed promised flows. The approximator is linear; actual bumped prices must be calculated separately. Callable, default-sensitive and nonparallel-curve scenarios, other platforms and independent acceptance were not tested. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-12-duration-review/review.py
```

Next: 12.10 — Modified Duration.
