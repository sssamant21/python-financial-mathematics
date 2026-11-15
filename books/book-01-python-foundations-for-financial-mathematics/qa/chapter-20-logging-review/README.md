# Section20.10 — Logging (scoped)

Based on `c7d5060fc6bf7a8f01f7a91dd6651b7bccb25e1c`. One formal workflow,[40 answer records](answer-records.json),[12 lab-step contracts](lab-step-records.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-20-logging-review/review.py
```

[Four failed baseline predicates](baseline.json),[identical replay](baseline-replay.json),[actual failing command exits/output](baseline-runs.json),[50 corrected source/event predicates/five commands](results.json) retained. F211 fixes two oversized-input cases that leaked OverflowError and emitted numerical rather than invalid_input;each had an exception and an event predicate,so four failures are not four unique defects. [Later scoped disposition](resume-disposition.json) maps both saved logging observations;historical initial/replay records unchanged.

Exact source executed direct,module unittest,compilation,quiet import/root-state and optimized. Twelve existing unique methods ran36 invocations;zero new historical methods. Five independent represented-rate Fraction discount sums test ordinary numeric results separately from fixed event content. Actual captured records retain event order/level/category and absence of synthetic raw data/result/exception-info sentinels. Root handler/level import state remains unchanged. Invalid run IDs emit nothing;unknown iterator RuntimeError propagates after start. The observer restores named logger state and uses local in-memory synthetic handlers only.

Persistence,retention,delivery,clock synchronization,alerting,privacy/access controls,JSON schema and immutable audit records are conceptual/design reviews,not implemented tests or certification. Broad all-range NPV/underflow/resources,arbitrary iterable ordering(F209),F28 notebook/platform,F32 shared-input integration,F165 tail limits,F185 integration and independent/platform/release acceptance remain open. Chapter20 now10 scoped workflows/400 local answers. Next:Section20.11 Type Hints.

Executable source/checker bytes verified against `067c4205c8339341e1f76352f60fdf4fd2615b78`;[source manifest](publication-verification.json).
