# Section19.14 — Integrated financial-data-pipeline review

Baseline `2bd9edae71a0f1def7176b33ec516d3a798393af`. [Source](../../chapter-19/19.14-chapter-project-financial-data-pipeline.md) · [40 answer records](answer-records.json) · [raw input](input.json) · [canonical output](output.json) · [source manifest](manifest.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-project-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-project-review/review.py 2bd9edae71a0f1def7176b33ec516d3a798393af
```

[Expanded baseline](baseline.json) and[identical predicate replay](baseline-replay.json) retain eight failures;[corrected](results.json) has39 passing predicates,three actual source commands (demo/12 existing tests,compile,quiet import). The earlier prepared checkpoint runner was actually executed and retained[six baseline failures](../chapter-19-project-checkpoint/baseline-runtime.json);the two added formal cases expose caller Inexact traps and exponent bounds. No historical failure/checkpoint was removed. One project workflow,40 local answers and12 lab-step records reviewed;zero new historical unique methods claimed.

## F200 scoped resolution

The return is formed from exact represented Decimal differences/quotient before one report in a fresh28-digit HALF_EVEN context with standard bounds/traps. Near-unity1e-30 no longer collapses to zero,and caller Inexact/Emax changes no longer choose the result. Decimal range exceptions and nonfinite/nonzero-to-zero reports raise ValueError. Input prices remain strictly positive;zero terminal prices are not added to this project domain. Timestamp hours00–23/minutes00–59 and UTC calendar range now follow the adjacent reviewed parser policy. These are explicit project arithmetic/time conventions,not arbitrary precision,resource bounds or settlement approval.

Independent return:(10150−10000)/10000=3/200=.015. Actual source raw/output hashes,record count2,schema1,precision28,HALF_EVEN and canonical UTC cutoff are checked. Same bytes/cutoff yield identical output/manifest. Input whitespace changes input identity but not output;an equivalent offset cutoff normalizes to the same manifest time. A cutoff before the second availability rejects;exact equality accepts. Invalid decoding/JSON/duplicate keys/shape/types/schema/date/close/currency/price-type/instrument/order reject without a partial return. Canonical output is independently specified,not copied from the implementation for expected bytes.

## Twelve lab-step records

|Step|Evidence / scope|
|---|---|
|1| Six string fields,USD/unadjusted pair,one normalized instrument,increasing dates and supplied availability contract reviewed.|
|2| Exact3/200=.015 independently derived.|
|3| Verbatim fence,Python/platform/source hashes retained.|
|4| Actual demo and manifest retained in command stdout and fixtures.|
|5| Raw/output SHA256 compared with independently serialized expected bytes.|
|6| Replay and whitespace/equivalent-cutoff identity cases executed.|
|7| Early cutoff rejects and equality accepts.|
|8| Missing/null/nonfinite/type/duplicate JSON cases executed.|
|9| Duplicate/reversed dates and mismatched instruments reject.|
|10| Source/code/retrieval/dependency/revision metadata omissions remain identified.|
|11|12 unchanged reference methods executed;three commands/39 predicates counted separately.|
|12| A hypothetical sink requires source+instrument/date/price-type/revision key,transaction boundary,conflict policy,idempotency token/retry/reconciliation and recovery;design review only,no sink executed.|

The raw data and result remain in memory;hashes prove neither authenticity nor confidentiality. Fixed context does not bound arbitrary coefficients/exponents,input bytes or processing cost. Availability timestamps are assumed truthful;no revision selection,exchange calendar,corporate-action or provider completeness is implemented. Source manifest still lacks a complete code/dependency/provenance contract. F28/F32/F165/F185 and independent/platform acceptance remain open. Next:Section19.15 final50 answers and final lab,then Chapter20.
