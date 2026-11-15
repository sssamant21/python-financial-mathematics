# Section20.8 — Input validation (scoped)

Based on `059e25f0f2b1bf376bad2a973e9703d5f6efe749`. One formal workflow,[40 answer records](answer-records.json),[12 lab-step contracts](lab-step-records.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-20-input-review/review.py
```

Optional source revision replays baseline. [Eight failed source predicates](baseline.json),[identical actual replay](baseline-replay.json),[45 corrected source predicates/five source commands](results.json) retained. One exact-unit arithmetic control is separate. Fourteen existing unique methods run direct/module/optimized:42 invocations,zero new historical methods. Compilation and quiet import pass;no all-input correctness implied.

F208: four oversized-input exception leaks,three complete-return accuracy/range failures and one late iterator TypeError misclassification. Strict finite gates normalize oversized integers toValueError;complete represented return rounds once and rejects true final overflow. Only TypeError while obtaining iter(cashflows) is classified as noniterability;later iterator exceptions propagate. Flow materialization still precedes rate validation,with actual consumed order retained.

Independent normal NPV references use rational represented-rate powers;return references use1600/2000-digit Decimal difference/quotient and agree at float report precision. Valid list/tuple/generator,fresh copy/caller immutability,missing/empty/wrong-type/nonfinite/boundary domains,late TypeError/RuntimeError and validation-consumption controls are explicit. The same14 original methods passed on the baseline despite eight added failures.

F209 is OPEN DESIGN:actual numeric mapping keys,set members and bytes pass element validation. This implementation materializes arbitrary iterable values;it does not establish ordered-sequence-only semantics,financial ordering,provenance or resource bounds. These three observed acceptances are recorded separately under collection_shape_observations,not counted as failed predicates or certified financial inputs. The source now states this limit;surrounding policy/integration remains unresolved.

Currency,price type,dates,availability,quarantine,Decimal extensions and secret-safe caller logging are conceptual/design obligations,not invented executed APIs. Broader NPV range/underflow/resources,F28 notebook/platform,F32 shared-input integration,F165 tail limits,F185 model/converter integration and independent/source/platform/release acceptance remain open. Chapter20 now8 scoped workflows/320 local answers. Next:Section20.9 Exception Handling.

Executable source/checker bytes verified against candidate `2b64f1adaeae6e143e76d7f5570b5d50fecd3dba`;see [source manifest](publication-verification.json).
