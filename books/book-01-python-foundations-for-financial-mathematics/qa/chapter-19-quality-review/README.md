# Section 19.11 — Data quality checks scoped review

Source revision `da173ca7e4bffb6ec72bf861f30b242dda78f910`. [Manuscript](../../chapter-19/19.11-data-quality-checks.md) · [40 answer records](answer-records.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-quality-review/review.py
```

[Initial execution](initial.json),[results](results.json) and[actual predicate replay](replay.json) retain36 passing predicates and three source commands:demonstration with12 existing methods,compilation and quiet import. No source defect or source change was warranted in this scope;no failed run is invented. One workflow,40 local answers and12 lab-step records reviewed;zero new historical unique methods claimed.

## Independent counts and contract

The two-row source demonstration has one missing close:1/2=.5. The worked exercise's distinct four-row fixture has one missing close:1/4=.25. It has submitted4,accepted3,rejected1,completeFalse;these are different denominators,not conflicting answers. A generator works and caller rows are unchanged. Empty input returns submitted0,rejected0,rateNone,completeFalse. Nonempty valid sparse dates can yield completeTrue;the code has no expected-session/calendar coverage API and does not prove provider completeness.

Missing/None/empty close is the primary reason before schema. Remaining priority is schema,type,instrument,currency,date,close. Each rejected row contributes one reason,not every possible defect. Extra fields reject;compact/week dates reject through canonical ISO comparison;NaN/sNaN/infinity/zero/negative/malformed closes reject. Numeric parsing is Decimal syntax,not Section19.7's width/scale schema. Accepted instrument whitespace normalizes before duplicate checking. Only accepted keys reserve instrument/date identity:an invalid earlier close does not make a later valid row a duplicate. Counts retain a reason summary but no per-rejected-row quarantine payload;quarantine governance remains conceptual here.

No source accuracy,freshness,independent reconciliation,revision completeness,publication gate,market-calendar coverage,financial price semantics or memory/resource bound is implemented or inferred by completeTrue. F28/F32/F165/F185 and independent/platform acceptance remain open.

## Twelve lab-step records

| Step | Evidence / scope |
|---|---|
|1| Four exact fields;positive finite decimal-text close,USD,canonical date,key instrument/date. Source identity and use case remain external. |
|2| Verbatim fence extracted;Python/platform and manuscript/source hashes retained. |
|3| Valid and missing-close rows executed;type/schema/domain cases also checked. |
|4| Actual demo1/2=.5 versus separate worked fixture1/4=.25;submitted rows are denominator. |
|5| Normalized accepted-key duplicate and invalid-earlier-key-not-reserved cases checked. |
|6| Nonfinite close,invalid/compact/week dates and unexpected currency rejected. |
|7| Empty rateNone and incompleteFalse flag verified;no division by zero. |
|8| Sparse valid dates still completeTrue;freshness/expected sessions absent. |
|9| Reconciliation requires independent matched units,time,price type and tolerance;conceptual proposal only. |
|10| Owner/threshold/publication decision must be defined externally;no publication-control implementation claimed. |
|11|12 unchanged existing methods and three commands ran;36 supplemental predicates counted separately. |
|12| Rule source hashes,counts,reasons,denominator and limits retained;no external raw-byte authenticity claim. |

## Forty local prompt-to-answer records

| Exercise | Topic | Worked answer | Scope |
|---|---|---|---|
|1|Completeness:|25% under that definition.|Actual source rule/count/denominator execution plus contract review|
|2|Empty batch:|Undefined in the reference code.|Actual source rule/count/denominator execution plus contract review|
|3|Empty batch:|No.|Actual source rule/count/denominator execution plus contract review|
|4|Missing key:|missing_close when close is absent.|Actual source rule/count/denominator execution plus contract review|
|5|Null close:|missing_close.|Actual source rule/count/denominator execution plus contract review|
|6|Empty close:|missing_close.|Actual source rule/count/denominator execution plus contract review|
|7|NaN:|close.|Actual source rule/count/denominator execution plus contract review|
|8|Zero close:|close.|Actual source rule/count/denominator execution plus contract review|
|9|Negative yield:|No.|Conceptual/design review;not independent source or point-in-time acceptance|
|10|Duplicate:|Instrument/date.|Actual source rule/count/denominator execution plus contract review|
|11|Duplicate:|No.|Conceptual/design review;not independent source or point-in-time acceptance|
|12|Venue:|Yes.|Conceptual/design review;not independent source or point-in-time acceptance|
|13|Revision:|Yes.|Conceptual/design review;not independent source or point-in-time acceptance|
|14|Keep latest:|No.|Conceptual/design review;not independent source or point-in-time acceptance|
|15|Date:|No.|Conceptual/design review;not independent source or point-in-time acceptance|
|16|Freshness:|No.|Conceptual/design review;not independent source or point-in-time acceptance|
|17|Availability:|Not necessarily.|Conceptual/design review;not independent source or point-in-time acceptance|
|18|Outlier:|No; investigate.|Conceptual/design review;not independent source or point-in-time acceptance|
|19|Split:|Yes.|Conceptual/design review;not independent source or point-in-time acceptance|
|20|Currency:|No.|Actual source rule/count/denominator execution plus contract review|
|21|Schema:|No.|Actual source rule/count/denominator execution plus contract review|
|22|Counts:|No; one primary reason is reported.|Actual source rule/count/denominator execution plus contract review|
|23|Duplicate detection:|Earlier accepted records.|Actual source rule/count/denominator execution plus contract review|
|24|Quarantine:|Separate invalid records for review.|Conceptual/design review;not independent source or point-in-time acceptance|
|25|Partial batch:|No.|Actual source rule/count/denominator execution plus contract review|
|26|Threshold:|To make the response consistent and reviewable.|Conceptual/design review;not independent source or point-in-time acceptance|
|27|Accuracy:|Yes.|Conceptual/design review;not independent source or point-in-time acceptance|
|28|Reconciliation:|To compare equivalent quantities.|Conceptual/design review;not independent source or point-in-time acceptance|
|29|Hash:|No.|Conceptual/design review;not independent source or point-in-time acceptance|
|30|Lineage:|To identify the transformation and rules used.|Conceptual/design review;not independent source or point-in-time acceptance|
|31|Expected dates:|No.|Actual source rule/count/denominator execution plus contract review|
|32|Calendar:|No.|Conceptual/design review;not independent source or point-in-time acceptance|
|33|Look-ahead:|Yes.|Conceptual/design review;not independent source or point-in-time acceptance|
|34|Rounding:|Yes.|Conceptual/design review;not independent source or point-in-time acceptance|
|35|Missing:|No.|Conceptual/design review;not independent source or point-in-time acceptance|
|36|Stale quote:|Yes.|Conceptual/design review;not independent source or point-in-time acceptance|
|37|Sensitive data:|No.|Conceptual/design review;not independent source or point-in-time acceptance|
|38|Memory:|Yes.|Actual source rule/count/denominator execution plus contract review|
|39|Tests:|No.|Conceptual/design review;not independent source or point-in-time acceptance|
|40|Quality checks:|No.|Conceptual/design review;not independent source or point-in-time acceptance|

Next:Section19.12 Reproducible Data Pipelines formal workflow/local-answer review. Broader Book1 validation remains in progress.
