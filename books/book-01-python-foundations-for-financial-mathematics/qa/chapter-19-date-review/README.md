# Section 19.9 — Date and timestamp normalization scoped review

Baseline `926330850a54eb97363c131b2d0188e7d7ee0bfa`. [Manuscript](../../chapter-19/19.09-date-and-timestamp-normalization.md) · [40 answer records](answer-records.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-date-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-date-review/review.py 926330850a54eb97363c131b2d0188e7d7ee0bfa
```

The baseline intentionally exits 1. [Initial results](baseline.json) retain five failed predicates and [identical replay](baseline-replay.json). [Corrected results](results.json) retain 38 passing source-call predicates, three source commands (demo with12 existing unittest methods,compile,quiet import), and four separately counted supplemental DST predicates. One workflow,12 lab-step records and40 local answers were reviewed; zero new historical unique methods are claimed.

## F196 — offset bounds and UTC calendar overflow

Python's fromisoformat normalized offsets +01:60,-01:60,+00:99 instead of rejecting the invalid minute fields. The restricted source parser now explicitly requires offset hours00–23/minutes00–59 before parsing. UTC conversion at year1 with a positive offset or year9999 with a negative offset leaked OverflowError; these valid local texts with unreportable UTC instants now raise the parser's documented ValueError. Bounds policy is explicit, not an assertion that every timestamp notation has identical semantics.

Zero offset text -00:00 remains accepted as fixed zero in this teaching contract; no unknown-offset protocol convention is inferred. Seconds and uppercase T/Z are required; up to six fractional digits are accepted. Naive/named-zone text, compact/week dates, leap seconds,24:00,extra fractional precision and trailing newline are rejected. Gregorian leap dates and invalid calendar dates are checked.

Independent expected instants use clock arithmetic:09:30−05:00 adds five hours to14:30UTC;00:15+05:30 subtracts five hours30minutes to18:45 on the previous date;23:45−02:00 adds two hours and crosses to01:45 next day. Microseconds retain ordering. Availability <= decision is inclusive, including equivalent-offset equality; it verifies no external provenance or revision completeness. Original text retention and event/availability field lineage are conceptual obligations, not a reference persistence API.

## Lab9 supplemental DST execution

The reference source deliberately accepts fixed offsets only. A separate zoneinfo implementation in the evidence runner uses the installed America/New_York rules. Autumn2026-11-01 01:30 fold0 maps to05:30UTC and fold1 to06:30UTC. Spring2026-03-08 02:30 fails a UTC/local wall-time roundtrip for both folds, showing the local time is nonexistent under the installed rules. Four actual predicates and installed zone-file SHA256 paths are retained. This executes the lab investigation; it does not add named-zone validation to the reference parser, certify other tzdata versions/platforms, or validate a market calendar.

## Twelve lab-step records

| Step | Evidence / prerequisite limit |
|---|---|
| 1 | Event,availability and ingestion fields have distinct meanings; real source definitions/lineage remain external prerequisites. |
| 2 | Verbatim reference fence extracted; Python/platform and exact manuscript/source digests retained. |
| 3 | Calendar date,leap day and invalid/compact/week spellings executed. A date is not an instant. |
| 4 |09:30−05:00→14:30UTC checked independently; positive/negative offsets and date crossings included. |
| 5 |14:30Z and offset equivalent map to the same aware UTC instant. |
| 6 | Naive text rejected; unsupported syntax and range controls recorded. |
| 7 |14:30 availability before15:00 decision returns True. |
| 8 | Reversed times return False; equality inclusive and microsecond ordering checked. |
| 9 | Four separate supplemental zoneinfo predicates investigate repeated/nonexistent wall times; zone-file hashes retained. |
| 10 | Real venue/calendar/session/precision and tie-breaker policies are design prerequisites,not supplied runtime fixtures. |
| 11 |12 unchanged reference tests and three source commands executed;38 source-call and4 supplemental DST predicates remain separate. |
| 12 | Source digests,zone-rule identity,actual outputs,rejections and boundaries recorded. No provider trust or point-in-time history acceptance. |

## Forty prompt-to-answer records

| Exercise | Topic | Worked answer | Scope |
|---|---|---|---|
| 1 | Date: | No. | Conceptual/design/source-contract review only |
| 2 | Offset: | 14:30Z. | Actual reference-source calls |
| 3 | Equivalent: | Yes. | Actual reference-source calls |
| 4 | Naive: | No. | Conceptual/design/source-contract review only |
| 5 | Event time: | When the event occurred. | Conceptual/design/source-contract review only |
| 6 | Availability time: | When information became available. | Conceptual/design/source-contract review only |
| 7 | Ingestion time: | When the system received it. | Conceptual/design/source-contract review only |
| 8 | Decision: | Available by the comparison. | Actual reference-source calls |
| 9 | Decision: | Not available. | Actual reference-source calls |
| 10 | Equality: | Yes. | Actual reference-source calls |
| 11 | Date validity: | No. | Actual reference-source calls |
| 12 | Compact date: | No. | Actual reference-source calls |
| 13 | Offset: | No. | Actual reference-source calls |
| 14 | Fraction: | Six. | Actual reference-source calls |
| 15 | Leap second: | No. | Actual reference-source calls |
| 16 | Named zone: | No. | Actual reference-source calls |
| 17 | DST spring: | Yes. | Separate supplemental zoneinfo execution plus conceptual review |
| 18 | DST autumn: | Yes. | Separate supplemental zoneinfo execution plus conceptual review |
| 19 | fold: | Repeated local times when used with suitable timezone rules. | Separate supplemental zoneinfo execution plus conceptual review |
| 20 | Attach zone: | No. | Separate supplemental zoneinfo execution plus conceptual review |
| 21 | Fixed offset: | No. | Conceptual/design/source-contract review only |
| 22 | Market date: | No. | Conceptual/design/source-contract review only |
| 23 | Weekend: | Do not assume; use the relevant calendar. | Conceptual/design/source-contract review only |
| 24 | Early close: | Session boundaries differ from ordinary days. | Conceptual/design/source-contract review only |
| 25 | Observation date: | Not necessarily. | Conceptual/design/source-contract review only |
| 26 | Revision: | Yes. | Conceptual/design/source-contract review only |
| 27 | Backtest: | Using data before its availability. | Conceptual/design/source-contract review only |
| 28 | Current history: | No. | Conceptual/design/source-contract review only |
| 29 | Precision: | Yes. | Conceptual/design/source-contract review only |
| 30 | Tie: | A source sequence or other documented tie-breaker. | Conceptual/design/source-contract review only |
| 31 | Ingestion order: | No. | Conceptual/design/source-contract review only |
| 32 | UTC conversion: | No. | Actual reference-source calls |
| 33 | Date-only: | No. | Conceptual/design/source-contract review only |
| 34 | Original text: | To support audit and interpretation. | Conceptual/design/source-contract review only |
| 35 | Timezone database: | Named-zone rules can change. | Conceptual/design/source-contract review only |
| 36 | Available-by: | No. | Conceptual/design/source-contract review only |
| 37 | Market calendar: | No. | Conceptual/design/source-contract review only |
| 38 | Nonexistent local time: | A rejection or correction policy. | Conceptual/design/source-contract review only |
| 39 | Tests: | No. | Conceptual/design/source-contract review only |
| 40 | Normalization: | No. | Conceptual/design/source-contract review only |

F28 notebook/platform,F32 shared-input integration,F165 tails,F185 signed-normal-terminal integration and independent acceptance remain open. Market-calendar versions,provider timestamp truth,full revision history,sequence/tie-breaking,input resource limits and other platforms are outside this scope. Next:Section19.10 Currency and Unit Normalization formal workflow/local-answer review.
