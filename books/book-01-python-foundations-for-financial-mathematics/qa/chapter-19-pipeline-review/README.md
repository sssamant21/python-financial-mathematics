# Section 19.12 — Reproducible pipeline scoped review

Baseline `5106894e21bb783f3a895eb6df58e0f66bc9aed9`. [Manuscript](../../chapter-19/19.12-reproducible-data-pipelines.md) · [40 answer records](answer-records.json) · [exact raw input](input.json) · [canonical output](output.json) · [source manifest](manifest.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-pipeline-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-pipeline-review/review.py 5106894e21bb783f3a895eb6df58e0f66bc9aed9
```

The baseline intentionally exits1. [Initial failures](baseline.json) and[identical predicate replay](baseline-replay.json) retain four return-cancellation mismatches. [Corrected results](results.json):37 predicates and three actual source commands passed (demo/12 existing tests,compile,quiet import). One workflow,40 local answers and12 lab-step records reviewed;zero new historical unique methods claimed.

## F198 — complete return while preserving the active-context contract

The source explicitly uses the active Decimal context,so this review does not replace it with a private context. End/start−1 lost a representable1e-30 increment;under precision2 it also reported0 instead of.015,and.3/.4 instead of.33/.34 for the controlled FLOOR/CEILING reports of(4−3)/3. The transform now forms the exact represented-input difference/quotient before one Decimal division under the active context. Precision,rounding,exponent limits and traps still affect reporting,as documented;extreme-input exceptions and coefficient/exponent resources remain outside this scope.

Independent benchmark:(101.50−100)/100=3/200=.015. Raw fixture bytes match the exact-source demo's input SHA256. The independently specified canonical output has sorted keys,fixed separators and return string0.015;its digest matches the source manifest. Replaying identical bytes/rules under the same controlled context reproduces bytes and manifest. Appending input whitespace changes input hash but preserves output bytes/hash;indenting JSON does likewise. Duplicate object keys and nonstandard JSON constants reject before transformation. Any schema/type/date/price/instrument/currency/order failure rejects the batch,without a partial return.

This is not context-independent replay or byte compatibility across code revisions. Rational reduction can change Decimal text scale for other inputs;serialization uses str of the result under the stated context. The source manifest still lacks Decimal-context identity,source/retrieval/publication/code/dependency metadata. The QA record separately retains the active context,Python/platform,source hashes and exact fixtures;it does not retrofit those missing fields into the source API or prove provider completeness,authenticity or availability. No external write or idempotent database retry is performed.

## Twelve lab-step records

| Step | Actual evidence / prerequisite limit |
|---|---|
|1| Exact two records,one normalized instrument,USD,positive finite decimal-text closes,increasing canonical dates. Comparable price/source assumptions remain external. |
|2| Verbatim source fence,Python/platform,active Decimal context and source hashes recorded. |
|3| Benchmark3/200=.015 checked from canonical output;four controlled-context failure cases corrected. |
|4| Exact raw/output fixtures and actual source manifest retained;hash identity does not prove truth. |
|5| Same bytes/rules/context replay matches output and manifest. |
|6| Trailing whitespace/JSON indentation change raw identity but preserve canonical output. |
|7| Duplicate keys,nonstandard constants,malformed encoding/JSON,wrong shape/types/fields,prices/dates/currency/order all reject. |
|8| Deterministic in-memory transformation does not demonstrate idempotent append/update/transaction behavior. |
|9| Missing source/retrieval/publication/revision/context/code/dependency metadata identified;not implemented. |
|10| A hypothetical watermark must retain late arrivals/revisions and define sink keys/availability;conceptual design only. |
|11|12 unchanged reference methods and three commands executed;37 predicates counted separately. |
|12| Versioned source,raw/output identity,context,counts and scoped limits recorded;no resource/platform/operational certification. |

## Forty prompt-to-answer records

| Exercise | Topic | Worked answer | Scope |
|---|---|---|---|
|1|Determinism:|Same logical result.|Actual reference transform/hash/serialization execution and arithmetic|
|2|Replay:|Rerun from identified inputs and configuration.|Actual reference transform/hash/serialization execution and arithmetic|
|3|Idempotence:|Repeating an operation has the same intended effect.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|4|Append:|No.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|5|Input hash:|Hashed raw bytes.|Actual reference transform/hash/serialization execution and arithmetic|
|6|Hash:|No.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|7|Whitespace:|Yes.|Actual reference transform/hash/serialization execution and arithmetic|
|8|Canonical JSON:|To obtain a consistent output representation.|Actual reference transform/hash/serialization execution and arithmetic|
|9|Key order:|Yes, under the stated serialization.|Actual reference transform/hash/serialization execution and arithmetic|
|10|Timestamp:|No.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|11|Return:|.015 or 1.5%.|Actual reference transform/hash/serialization execution and arithmetic|
|12|Missing row:|No.|Actual reference transform/hash/serialization execution and arithmetic|
|13|Duplicate JSON key:|Reject.|Actual reference transform/hash/serialization execution and arithmetic|
|14|NaN:|No.|Actual reference transform/hash/serialization execution and arithmetic|
|15|Currency:|No.|Actual reference transform/hash/serialization execution and arithmetic|
|16|Date ordering:|No.|Actual reference transform/hash/serialization execution and arithmetic|
|17|Code revision:|It identifies transformation logic.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|18|Decimal context:|Precision and rounding can affect results.|Actual reference transform/hash/serialization execution and arithmetic|
|19|Source:|No.|Actual reference transform/hash/serialization execution and arithmetic|
|20|Availability:|No.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|21|Watermark:|Yes.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|22|Revision:|To reconstruct what was available when.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|23|Retry:|No.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|24|Sink key:|To support documented duplicate and update handling.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|25|Partial failure:|No.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|26|Counts:|To reconcile inputs, outputs and failures.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|27|Secrets:|No.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|28|Raw input:|For lineage and reprocessing.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|29|Hash:|No.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|30|Version:|To support compatible replay.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|31|Floating point:|Yes.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|32|Tolerance:|When numerical equivalence is required rather than exact bytes.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|33|Schema:|Yes.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|34|Market calendar:|No.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|35|Corporate actions:|No.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|36|External writes:|No.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|37|Reproducible:|No.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|38|Resource limits:|Yes, according to the environment.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|39|Tests:|No.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|
|40|Production:|No.|Conceptual/design review;no idempotent sink,provider,revision or independent acceptance|

F28/F32/F165/F185 and broader integration/platform/independent acceptance remain open. Next:Section19.13 Avoiding Look-Ahead and Data Leakage formal workflow/local-answer review.
