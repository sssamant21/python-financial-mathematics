# Section19.13 — Look-ahead and leakage scoped review

Baseline `953fa30f7a29cc4a27a2817238e5b72f25c635ef`. [Source](../../chapter-19/19.13-avoiding-look-ahead-and-data-leakage.md) · [Synthetic revisions](synthetic-revisions.json) · [40 answer records](answer-records.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-leakage-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-leakage-review/review.py 953fa30f7a29cc4a27a2817238e5b72f25c635ef
```

Baseline intentionally exits1. [Initial failures](baseline.json) and[identical predicate replay](baseline-replay.json) retain five timestamp mismatches. [Corrected results](results.json):39 predicates and three source commands passed (demo/12 existing tests,compile,quiet import). One workflow,40 local answers and12 lab-step records reviewed;zero new historical unique methods claimed.

## F199 — as-of timestamp-copy bounds

The as-of copy accepted invalid offset minutes+01:60,−01:60,+00:99 through Python normalization and leaked OverflowError at the UTC year1/year9999 boundaries. It now enforces hours00–23/minutes00–59 and raises ValueError for invalid or unrepresentable UTC instants,matching Section19.9's restricted fixed-offset policy. No named-zone/history/source-trust validation is added. Seconds and explicit offsets remain required;overprecision,leap-second and trailing-newline controls reject.

Independent timeline:the March31 period is unpublished on April15;the May1 publication of100 is ingested at12:01,so12:00:30 cannot select it but12:01 can. It supplies100 on May5. The May10 correction105 is not eligible at12:00:59.999999 but is at12:01,and supplies105 on May12. A correction delayed in ingestion until May20 leaves100 selected on May12. Equality is inclusive for both timestamps.08:00−04:00 adds four hours to12:00UTC;microseconds remain ordered.

Selection ranks by latest eligible publication,not latest ingestion or list order. A tie at the latest eligible publication rejects;an older tie does not block a unique later winner. Input order reversal/generators preserve the result and caller rows remain unchanged. All rows are parsed,so an invalid irrelevant row rejects the request. Generic finite values may be zero or negative;this is not the positive-close schema from earlier sections. No expected revision history,source truth,market calendar,corporate-action or training/test policy is verified.

## Twelve lab-step records

|Step|Evidence / prerequisite limit|
|---|---|
|1| Effective March31,publication,ingestion and decision instants are distinct;source definitions remain prerequisites.|
|2| April15=None,May5=100,May12=105 independently derived and executed.|
|3| Verbatim fence,Python/platform and source/manuscript digests retained.|
|4| Actual source demo matches the three-decision table;synthetic fixture retained.|
|5| Published-but-not-ingested boundary checked for initial and corrected revisions.|
|6| Equality at ingestion accepted;one microsecond earlier excludes the correction.|
|7| Latest eligible tie rejects;older tie with unique later winner does not.|
|8| Naive timestamp rejects;offset equivalence,component bounds and UTC range checked.|
|9| Conceptual chronological split sketch below;no training/evaluation code executed.|
|10| Centered window sketch below identifies a future observation;no rolling-feature implementation claimed.|
|11|12 unchanged reference methods and three commands executed;39 supplemental predicates separate.|
|12| Versioned code,synthetic revisions,timestamp policy and missing source/calendar/history assumptions retained.|

For lab9,a hypothetical seven-calendar-day label horizon could use training through March31,validation starting April8 and ending April30,and a final test starting May8. The two seven-day gaps prevent those assumed labels from crossing the next partition;actual feature/label/availability definitions could require different boundaries. These are illustrative calendar dates,not exchange-session or independent model acceptance. For lab10,a centered window at t using[t−1,t,t+1] includes future t+1. A trailing window removes that future index but is still unsafe if its newest observation is unavailable at the decision time.

## Forty prompt-to-answer records

|Exercise|Topic|Worked answer|Scope|
|---|---|---|---|
|1|Quarter end:|No.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|2|April 15:|No.|Actual source as-of/time/parse execution plus contract review|
|3|May 5:|100.|Actual source as-of/time/parse execution plus contract review|
|4|May 12:|105.|Actual source as-of/time/parse execution plus contract review|
|5|Correction:|Look-ahead.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|6|Publication:|Not necessarily.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|7|Delay:|Not eligible.|Actual source as-of/time/parse execution plus contract review|
|8|Equality:|Eligible.|Actual source as-of/time/parse execution plus contract review|
|9|Offset:|12:00Z.|Actual source as-of/time/parse execution plus contract review|
|10|Naive timestamp:|No.|Actual source as-of/time/parse execution plus contract review|
|11|Tie:|Reject as ambiguous.|Actual source as-of/time/parse execution plus contract review|
|12|Effective date:|No.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|13|Current snapshot:|No.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|14|Revision history:|To reconstruct eligible versions.|Actual source as-of/time/parse execution plus contract review|
|15|Close at open:|Generally no.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|16|Signal time:|To compare with data availability and execution.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|17|Centered rolling window:|It can include future observations.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|18|Trailing window:|No; current value may not yet be available.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|19|Backward fill:|Uses a later observation for an earlier gap.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|20|Forward fill:|No; freshness and availability rules matter.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|21|Scaling:|Can leak evaluation-period information.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|22|Training scaler:|Apply parameters fitted on training data.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|23|Random split:|No.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|24|Overlapping labels:|Yes.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|25|Gap:|To limit information overlap.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|26|Survivorship:|Failed or delisted instruments.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|27|Today's index members:|Not automatically.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|28|Adjusted prices:|Yes.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|29|Corporate action:|Yes.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|30|Timezone:|To compare instants correctly.|Actual source as-of/time/parse execution plus contract review|
|31|Calendar:|No.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|32|Source truth:|No.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|33|Duplicate version:|No; use a contract or reject.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|34|Irrelevant invalid row:|Rejects it while parsing all rows.|Actual source as-of/time/parse execution plus contract review|
|35|Decimal:|No.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|36|Missing history:|Not without sufficient evidence.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|37|Test set:|No.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|38|Latency:|The system may receive published data later.|Actual source as-of/time/parse execution plus contract review|
|39|Tests:|No.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|
|40|Reproducibility:|No.|Conceptual/design only;not source truth,complete revision history or train/test acceptance|

F28/F32/F165/F185 and broader integration/platform/independent acceptance remain open. Next:Section19.14 Financial Data Pipeline project and chapter-wide answers.
