# Section20.11 — Type hints and runtime contracts (scoped)

Based on `5386dc2e5da136dbb1f31bbcc015a86b4d4fb190`. One formal workflow,[40 answer reviews](answer-records.json),[12 lab-step contracts](lab-step-records.json). Static portions of steps1/11 remain open.

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-20-types-review/review.py
```

[Five failed baseline source predicates](baseline.json),[identical actual replay](baseline-replay.json),[actual failing exits/output](baseline-runs.json),[46 corrected source predicates/five commands](results.json) retained. F212 fixes complete Decimal return cancellation/lost precision and caller trap/range dependence. Complete represented difference/quotient rounds once into private28-digit ROUND_HALF_EVEN;caller context/flags preserved. Independent1600/2000-digit difference/quotient references rounded once at28 digits cover near-unity and repeating thirds. Coefficient/exponent resource limits remain open.

Two exact Python fences compiled;full12-method suite ran direct,module and optimized:36 method invocations,zero new historical methods. Quiet import passes. Four independent ordinary represented-rate Fraction NPV references,strict built-in float rejection,optional prices,generator consumption and caller immutability checked. The introductory float simple_return intentionally has no validation;its zero-start error illustrates runtime behavior rather than a newly validated financial API.

Five runtime annotation/NewType observations are separate from46 source predicates and from static analysis. Neither mypy nor pyright is installed;no configured checker/version/target execution or static acceptance claimed. This specific missing-tool/configuration gap is retained and does not block other runtime reviews. Static int-for-float behavior,units,currency and data-class validation reviewed conceptually only.

Broader NPV range/underflow,Decimal lexical/coefficient/exponent resources,F28 notebook/platform,F32 shared-input integration,F209 iterable policy,F165 tail limits,F185 integration and independent/platform/release acceptance remain open. Chapter20 now11 scoped workflows/440 local answers. Next:Section20.12 Documentation.
