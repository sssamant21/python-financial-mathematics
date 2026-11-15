# Section20.13 — Reproducibility (scoped)

Based on `4b182d1e0aee83789733233f2f8ae151d989aa3f`. One formal workflow,[40 answer reviews](answer-records.json),[12 lab-step contracts](lab-step-records.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-20-repro-review/review.py
```

[Passing baseline](baseline.json),[actual identical replay](baseline-replay.json),[actual command exits/output](baseline-runs.json),[current44 source predicates/seven source commands](results.json) retained. No baseline failure and [no executable fence change](source-scope-comparison.json);no new defect claimed. Twelve existing unique methods ran36 invocations;zero new historical methods.

Four separate literal-byte/hash oracle commands use sha256sum on independently specified UTF8 JSON literals,then compare source input_bytes and manifest SHA256. [Exact synthetic input](synthetic-input.json) retained. Two separate manifest/representation observations show that revision labels are not covered by input digest and signed-zero bytes can differ;these are design limits,not defects. Six ordinary NPV references use independent represented-rate Fraction discount sums. Strict input types,optional bad revision labels,generator consumption,caller immutability and iterator error identity checked.

[Fresh process1](replay-process-1.json) and [process2](replay-process-2.json) have identical output bytes in this single candidate runtime. Source quiet import,compilation,direct/module/optimized methods also pass. Source revision labels remain unverified;actual executed fence identity is recorded separately by QA. No external provenance,availability/history,random stream/parallel replay,full environment/artifact capture,universal JSON canonicalization,cross-version/platform replay or independent financial acceptance claimed.

F28 notebook/platform,F32 shared-input integration,F209 iterable policy,20.11 static checker,F165 tail limits,F185 integration and broad NPV range/underflow/resources/provenance/independent acceptance remain open. Chapter20 now13 scoped workflows/520 local answers. Next:Section20.14 Model Validation vs.Software Validation.

[Initial harness serialization observation](harness-serialization-note.json) retains both passing original records:an unordered set repr changed order across processes. The QA observer now records sorted keys;this was a harness-output issue,not a source or financial predicate failure.
