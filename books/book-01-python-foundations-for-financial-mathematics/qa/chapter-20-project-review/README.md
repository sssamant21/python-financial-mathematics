# Section20.15 — Educational finlib project (scoped)

Based on `78b2ddb63e3bef63f54b89e6e879ef2c4ea46f2c`. One project workflow,[40 local answer reviews](answer-records.json),[12 lab-step reviews](lab-step-records.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-20-project-review/review.py
```

[42 passing baseline predicates](baseline.json),[actual passing replay](baseline-replay.json),[command outputs](baseline-runs.json),[current42 source predicates/six commands](results.json) retained. [Four executable fences unchanged](source-scope-comparison.json);no implementation defect claimed. Twelve existing unique methods ran36 invocations:documented discovery,alternate root-context reference main and optimized discovery. Both package files,test and provided example compiled. The actual provided example prints NPV4.132231. Root import/call logging state and tested no-output behavior preserved;not installation or broad security validation.

[Initial QA oracle correction](oracle-correction.json),[initial failed probe](initial-oracle.json),[identical failed replay](initial-oracle-replay.json),[actual initial exits/output](initial-oracle-runs.json) retained. Relative-only tolerance was incorrectly used for the near-zero break-even vector;the published absolute1e−10 monetary tolerance is now applied to that vector. Other tiny nonzero probes retain zero absolute slack. This is a QA tolerance-contract correction,not a source numerical fix. Ten independent represented-rate Fraction NPV references differ from Horner evaluation.

One separate actual range observation retains a finite exact final1e308 rejected because the Horner intermediate overflows;the manuscript explicitly documents this policy. It is not an added failed predicate or all-range solution. Ordering/type/rate contracts,caller immutability,scaling/additivity and conditional monotonicity checked. [Draft release-scope assessment](release-scope.json) does not approve packaging,installation,production or independent model suitability.

Chapter20 now14 core workflows/560 answers plus one project workflow/40 local answers (15 scoped workflows/600 local answers). Next:20.16 Exercises and Applied Problems with embedded solutions. 20.11 static checker,F28 notebook/platform,F32 shared-input integration,F209 iterable policy,F165 tail limits,F185 integration and broader numerical/provenance/model/platform/release acceptance remain open.

Executed source/checker bytes verified against `248b67271091d210fa62d3fb68cdbfb09a5c6793`;[source manifest](publication-verification.json).
