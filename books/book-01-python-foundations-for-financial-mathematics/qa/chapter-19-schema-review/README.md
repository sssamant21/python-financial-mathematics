# Section19.7 — scoped schema/type workflow review

Baseline `39c3e62d59aade825ff6c414ba6bbbcd66666a90`. [Source](../../chapter-19/19.07-schema-and-data-types.md) · [40 answer records](answer-records.json) · [synthetic decoded records](synthetic-records.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-schema-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-schema-review/review.py 39c3e62d59aade825ff6c414ba6bbbcd66666a90
```

Baseline command intentionally exits1. [Baseline](baseline.json) retains2failed predicates with [identical predicate replay](baseline-replay.json). [Corrected](results.json):40supplemental predicates and3exact-source commands passed (demo/12existing methods,compile,quiet import). One workflow,40local answers/12lab records reviewed;zero new historical unique methods. No observer correction needed.

## F194 — standalone schema return-copy alignment

The helper retained end/start-1 near-unity cancellation andambient Decimal precision after adjacent modules were corrected. It now uses their complete-ratio/private34digit HALF_EVEN policy;unreportable finite/nonzero outputs raise ValueError,andexact zero/zero terminal remain valid. The near-unity1e-30case is a direct standalone-helper test outside the intentionally narrow record-price width/scale;it doesnot imply those prices are schema-valid. The ordinary schema-valid100→101.50case also demonstrates ambient precision dependence before the explicit private-context policy. No record-price/parser rule was widened. Arbitrary exponent/coefficient resources,currency-specific cash rounding andfinancial/source suitability remain open.

## Independent expectations andcontract boundaries

Record text permits1–6ASCII integral digits andoptional1–2fractional digits;positivity then excludes0.00. Maximum-width123456.78 andmaximum numeric999999.99 accepted;1000000.00/1234567.00 rejected. 000001.20 counts6integral digits andpreserves Decimal scale2;0000001.2 has7integral digits andis rejected. Scientific notation,plus/minus signs,.5,1.,trailing newline andfull-width Unicode digits remain excluded. These are this teaching schema's physical rules,not universal accounting precision standards.

Canonical YYYY-MM-DD is enforced;compact/week-date spellings reject. Instrument whitespace normalizes beforeduplicate checking. Input order/caller data are preserved;empty input is allowed. validate_unique fails the batch oninvalid/duplicate rows anddoesnot expose a quarantine/complete-flag API likeSection19.6. Exact return arithmetic3/200=.015 andunit identities5/100=.05,100/10000=.01 are separate from schema/model meaning. Decimal text is preserved even underlow caller precision;this doesnot validate currency/instrument/units.

Synthetic fixture serialization/digest identifies observer input,not original external bytes. No CSV/JSON syntax decoder,live source,venue/revision/publication/availability/source-lifecycle/calendar/corporate-action,resource/security/platform orindependent financial acceptance is implemented orcertified. F28/F32/F165/F185 remain open.

## Twelve lab-step records

| Step | Prompt | Evidence / limit |
|---|---|---|
| 1 | Schema/key | Exact5string fields;USD/unadjusted_close;key stripped instrument,canonical date,price_type;no source/availability/venue fields |
| 2 | Save/environment | Reference fence extracted verbatim;Python/platform/source SHA256 retained |
| 3 | Validate examples | Actual source demo2records;12existing reference methods;direct source calls |
| 4 | Return benchmark | Exact3/200=.015;private complete-ratio return arithmetic separately tested |
| 5 | Missing/extra/null | Missing fields/venue extra rejectschema;null/bool closes rejecttype |
| 6 | Width boundary | 123456.78 and999999.99 accepted;7integral digits rejected;leading zeros countas supplied |
| 7 | Scale/notation | Morethan2fractional digits,scientific notation,signs,missing integral digits,trailing newline andnon-ASCII digits rejected |
| 8 | Duplicate key | Later normalized duplicate causes fail-fast ValueError;no partial return orquarantine API in this section |
| 9 | Real key scope | Venue/source/revision may be required;conceptual review only |
| 10 | Absent semantics | No publication/source/calendar/instrument-lifecycle/corporate-action acceptance |
| 11 | Reference suite | 12unchanged existing unique methods;3source commands/40supplemental predicates separate |
| 12 | Evidence/version | Synthetic decoded-record fixture/digest retained;schema version identified bysection/source revision externally;no publication gate/resource guarantee |

## Forty prompt-to-answer records

| Exercise | Topic | Reviewed answer | Scope |
|---|---|---|---|
| 1 | Schema: | Structure, types and specified constraints. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 2 | Meaning: | No. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 3 | Logical type: | A decimal financial amount. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 4 | Physical type: | Yes. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 5 | Precision: | Total digits in a fixed-decimal definition. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 6 | Scale: | Digits after the decimal point. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 7 | Example: | Yes. | Actual schema/price/key/return checks |
| 8 | Example: | No; integral width exceeds six. | Actual schema/price/key/return checks |
| 9 | Example: | No; scale exceeds two. | Actual schema/price/key/return checks |
| 10 | Example: | No; scientific notation is excluded. | Actual schema/price/key/return checks |
| 11 | Leading zeros: | Yes. | Actual schema/price/key/return checks |
| 12 | Zero close: | No. | Actual schema/price/key/return checks |
| 13 | Negative yield: | No. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 14 | Null: | No. | Actual schema/price/key/return checks |
| 15 | Empty string: | No. | Actual schema/price/key/return checks |
| 16 | Boolean: | No. | Actual schema/price/key/return checks |
| 17 | Currency: | USD. | Actual schema/price/key/return checks |
| 18 | Price type: | unadjusted_close. | Actual schema/price/key/return checks |
| 19 | Return: | .015 or 1.5%. | Actual schema/price/key/return checks |
| 20 | Rate: | .05. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 21 | Basis points: | .01. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 22 | Date: | No. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 23 | Availability: | No. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 24 | Key: | Instrument, observation date and price type. | Actual schema/price/key/return checks |
| 25 | Ticker: | No. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 26 | Revision: | No. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 27 | Schema evolution: | Yes. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 28 | Unit change: | Yes. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 29 | Type inference: | No. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 30 | Unknown field: | Reject. | Actual schema/price/key/return checks |
| 31 | Empty batch: | Accept; policy must be explicit. | Actual schema/price/key/return checks |
| 32 | Hash: | No. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 33 | Calendar: | No. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 34 | Source: | No. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 35 | Outlier: | No; investigate. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 36 | Float→Decimal: | Not necessarily. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 37 | Timezone: | No. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 38 | Cross-field check: | Verify currency against the instrument contract. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 39 | Tests: | No. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |
| 40 | Schema-valid: | No. | Contract/conceptual/unit arithmetic;not source/financial/point-in-time/platform acceptance |

Next:Section19.8 Missing andInvalid Values formal workflow/local-answer review;broader Book1 validation remains in progress.

Executable source revision: `f896f2b31702c4d56427e7d6f81f427f6b2ed235`. [Publication source manifest](publication-verification.json). Metadata pins do not change the tested source, observer or fixture.
