# Section20.12 — Documentation and runtime contract alignment (scoped)

Based on `5ada3da82c869410cdc54311b187fe51e695fdcf`. One formal workflow,[40 answer reviews](answer-records.json),[12 lab-step contracts](lab-step-records.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-20-docs-review/review.py
```

[Four failed baseline predicates](baseline.json),[identical actual replay](baseline-replay.json),[actual failing exits/output](baseline-runs.json),[32 corrected source predicates/six commands](results.json) retained. F213 fixes two noniterable inputs that raised TypeError despite the documented ValueError contract;each also lacked the expected cause,so four predicate failures are not four unique defects. Only obtaining iter(cashflows) is translated with TypeError cause;late TypeError/RuntimeError identity and consumption-before-rate-validation are retained. Docstring now specifies strict rate type and precise iterator/resource limits.

Exact source executes direct,module unittest,compilation,quiet import,help rendering and optimized. Twelve existing unique methods ran36 invocations;zero new historical methods. Six independent represented-rate Fraction NPV references cover normal values,signed flow,zero rate and t0 identity. Four separate docstring/help visibility observations do not certify financial accuracy. Actual printed docstring/help output retained.

Provenance,source truth,availability/look-ahead,unit migration,rounding policy,copyright/editorial/independent model acceptance remain conceptual/manual scope. All-range NPV/intermediate exponential rejection,underflow,cancellation,resource/collection ordering(F209),20.11 static-checker gap,F28 notebook/platform,F32 shared-input integration,F165 tail limits,F185 integration and independent/platform/release acceptance remain open. Chapter20 now12 scoped workflows/480 local answers. Next:Section20.13 Reproducibility.
