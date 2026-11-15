# Section20.14 — Model vs.software validation (scoped)

Based on `824ab9a1f874f18f379e8137812958f3a841f15a`. One formal workflow,[40 answer reviews](answer-records.json),[12 lab-step reviews](lab-step-records.json);intended-use/independent governance/outcome decisions remain pending.

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-20-model-review/review.py
```

[Passing baseline](baseline.json),[actual identical replay](baseline-replay.json),[actual exits/output](baseline-runs.json),[28 current source predicates/five commands](results.json) retained. [Executable fence unchanged](source-scope-comparison.json);no source defect invented. Twelve existing unique methods ran36 invocations;zero new historical methods. Nine independent represented-input rational PV references cover ordinary/zero/negative payments/rates,subnormal/large values and near-domain boundary. Strict float inputs,detected overflow,scaling and monotonicity checked. Direct source sensitivity output retained.

Two separate exact-rational hypothetical/unit scenarios demonstrate default/recovery and rate-unit assumptions;they are supplemental conceptual calculations,not an implemented/calibrated credit model or independent financial validation. Governance,actual outcomes,model ownership and approval are conceptual/manual scope,not executed acceptance.

[Primary source-currency check](source-currency-check.json) re-opened the cited Federal Reserve letter on2026-11-15,confirming the date and supersession references. Applicability,attachment/framework adequacy and compliance/legal acceptance not assessed. Historical SR11-7 citation remains explicitly historical;no organization-specific policy inferred.

20.11 static checker,F28 notebook/platform,F32 shared-input integration,F209 iterable policy,F165 tail limits,F185 integration and broad numerical/provenance/model/independent/platform/release acceptance remain open. Chapter20 now14 scoped workflows/560 local answers. Next:Section20.15 Chapter Project—Production-Quality Financial Library.

Executed source/checker bytes verified against `f8aa4390a2cf5bd69b885a099d0da2ad6082216f`;[source manifest](publication-verification.json).
