# Section20.7 — Financial invariants and independent benchmarks (scoped)

Based on `55b8ebef2ca9338976fa27b140aae386e7e0d82b`. One formal workflow,[40 answer records](answer-records.json),[12 lab-step contracts](lab-step-records.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-20-invariants-review/review.py
```

Optional source revision replays baseline. [Eleven initial failed source predicates](baseline.json),[identical actual replay](baseline-replay.json),[39 corrected source predicates/five source commands](results.json) retained. Compilation and quiet import pass. Fourteen existing unique methods run direct/module/optimized:42 invocations;three separate synthetic/control selected-method calls bring total45 invocations,zero new historical methods. Two exact arithmetic controls remain supplemental.

F207: four complete-return accuracy/range cases;two near-budget weight cases incorrectly rejected by rounded sum arithmetic;portfolio output leaked infinity;four oversized-input exceptions. Strict finite checks normalize oversized inputs toValueError;complete represented return and dot product round once and reject final overflow. The weight-sum gate now compares its exact represented sum with the same1e−12 budget,without tolerance widening or renormalization. Accepted near-one weights need not obey every exact fully-invested bound;individual returns still require≥−1.

Independent1800/2400-digit Decimal difference/quotient/dot references agree at float reporting precision. Ordinary NPV uses rational powers;nonzero scaling,append/insertion,future payment signs,time-zero constancy,price scaling,invalid domains and exact weight-boundary decisions retain their assumptions. Future-payment and weight-tolerance worked answers are qualified. Broader log/exp NPV extremes remain outside this scoped fix.

The [deliberate always-zero NPV copy](always_zero_variant.py.txt) passes the existing scaling method (exit0) yet fails the independent known-nonzero method (exit1);unchanged source control passes (exit0). Actual output is saved. This is a supplemental weak-property demonstration,not a defect in the published NPV implementation or a claim that every invariant passes. Separate Decimal compounding/units arithmetic is not a missing financial API implementation.

PSD covariance,FX,fees,calendars/model validation are conceptual here;no covariance or conversion execution claimed. Collection/ingestion resources,broader NPV/underflow,F28 notebook/platform,F32 shared-input integration,F165/F185 and independent/source/platform/release acceptance remain open. Chapter20 now7 scoped workflows/280 local answers. Next:Section20.8 Input Validation.
