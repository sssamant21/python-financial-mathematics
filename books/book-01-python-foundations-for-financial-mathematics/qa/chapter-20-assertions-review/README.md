# Section20.2 — Assertions and known-value tests (scoped)

Based on `9392004a95ed37258177ee1cf1018d9170cbb3b3`. One formal workflow, [40 individual answers](answer-records.json), [12 lab-step records](lab-step-records.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-20-assertions-review/review.py
```

Optional revision argument replays baseline. [Nine source-call baseline failures](baseline.json), [identical predicate replay](baseline-replay.json), [34 corrected predicates/five source commands](results.json) retain actual outcomes. Both exact manuscript Python fences executed/compiled;quiet import and optimized reference suite passed. Twelve existing unique methods run24 normal/optimized invocations;selected mutation/control add2,for26 total. Zero new historical unique methods.

F202: finite oversized integers leaked OverflowError;end/start−1 lost the28th significant digit for1/3 and erased ±1e−29 returns;caller traps and small exponent bounds leaked errors/infinity. Complete represented Decimal-input Fraction return now receives one fresh Context(prec28,HALF_EVEN) report;range errors/nonzero-to-zero reporting reject. Caller settings are not inherited. Positive-payment answer now requires t>0,with t0 constant. NPV remains limited float/log/exp code,not a complete-range discount/sum implementation.

Independent ordinary-case NPV references use rational discount powers;Decimal expectations use an independent150-digit Decimal difference/quotient followed by the stated28-digit reporting rule;selected finite inputs are exact at that working precision except the recurring quotient. Comparison semantics are explicitly checked:math.isclose uses max(relative scale,absolute tolerance),unlike the asymmetric tolerance sum. Conceptual model/currency/date/fee/seed/production claims are not execution acceptance.

[Initial mutation observation](initial-mutation-observation.json) retains the first supplemental timing-shift copy that was NOT detected by a zero-NPV test:all flows were multiplied by the same discount factor,so zero stayed zero. This is a real weak-case observation,not a source failure. The final supplemental omitted-investment variant is detected (exit1),unchanged source control passes (exit0). Separate assert-False normal/optimized probes have expected exits1/0. [Faulty variant](faulty_variant.py.txt) is never published as the reference implementation.

Decimal Fraction conversion has no input-size/exponent resource cap;large-ingestion/reporting-range policies and broader NPV extremes/underflow remain open. F28 notebook/platform,F32 shared-input integration,F165/F185 and independent/source/resource/release acceptance remain open. One Linux assistant review is not certification. Chapter20 now2 scoped workflows/80 local answers. Next:Section20.3 Unit Testing.
