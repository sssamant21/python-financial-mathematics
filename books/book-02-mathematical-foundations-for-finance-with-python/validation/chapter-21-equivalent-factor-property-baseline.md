# INT-01 equivalent-rate factor acceptance: baseline

Next COV-88 obligation: the plan states “equivalent rates produce equivalent factors,” but does not yet declare the conversion-rounding allowance or comparison domain. Existing known-value rate checks are already retained; do not count them again.

Reproduced at [pinned source `12de5ae82ef9155593bf2b97ebfd034524bef0b5`](https://github.com/sssamant21/python-financial-mathematics/blob/12de5ae82ef9155593bf2b97ebfd034524bef0b5/books/book-02-mathematical-foundations-for-finance-with-python/chapter-21/code/section_21_03.py), blob `ebf9d4733542fb11b5c8121fb9ec8725d2b260c4`:

| Effective rate and horizon | Effective factor (float hex) | Factor after rounded continuous conversion | Relative discrepancy |
|---|---|---|---:|
| 0.25, 1000 years | `0x1.0d152311513c3p-322` | `0x1.0d15231151398p-322` | approximately −9.08e−15 |
| −0.5, 1000 years | `0x1.0000000000000p+1000` | `0x1.fffffffffff2fp+999` | approximately −2.32e−14 |

These are finite values and differ after rounding the continuous rate; the observation is not a failure of the existing ordinary tolerance checks. A true convention identity need not be a bitwise identity for independently represented inputs.

```python
from section_21_03 import discount_factor, to_continuous
from section_21_08 import make_plan

for rate, years in ((.25,1000.),(-.5,1000.)):
    converted=to_continuous(rate)
    exact_convention=discount_factor(rate,years,"effective_annual")
    rounded_convention=discount_factor(converted,years,"continuous")
    print(rate,years,converted.hex(),exact_convention.hex(),rounded_convention.hex(),
          exact_convention==rounded_convention,
          (rounded_convention-exact_convention)/exact_convention)
print(next(case for case in make_plan()["cases"] if case["id"]=="INT-01"))
```

Next: derive the factor discrepancy from the rounded rate error times the horizon, evaluate each convention independently, and specify finite/nonzero factor and tolerance boundaries. Retain invalid conversion endpoints and distinguish numerical equivalence from financial suitability. Keep all execution/review/approval placeholders pending.
