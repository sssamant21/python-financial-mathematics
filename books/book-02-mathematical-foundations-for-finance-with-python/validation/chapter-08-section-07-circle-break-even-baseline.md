# Next checkpoint: Section8.7 circle and break-even helpers

[Eight actual observations](chapter-08-section-07-circle-break-even-baseline.json):five mismatches, three ordinary controls. Circle values independently use complete Decimal radius²-x² square roots at200/400 digits; both final floats agree. Break-even quantity and sensitivity use complete exact rational gap/ratio references. These expose squared-radius overflow/underflow, boundary0*infinity NaN, overflowing p-c and a lost finite nonzero sensitivity. They are initial numerical mismatches, not five distinct defects; no fixes or corrected passes claimed.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-07-circle-break-even-probe.txt .
```

Next: reconcile input domains, validation order, complete-output/zero/underflow policies and model interpretation before correction; preserve positive fixed cost and p>c rather than silently narrowing accepted signed prices/costs. Bond, exposure, centered-copy, resource and independent-review obligations remain separate. No COV closure or platform/release approval.
