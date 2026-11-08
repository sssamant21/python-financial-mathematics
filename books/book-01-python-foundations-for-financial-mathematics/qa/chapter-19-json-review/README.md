# Section19.3 — scoped JSON workflow/answer review

Baseline `5e574af2b055c7822e053fed5d0f5f24870d79bb`. [Source](../../chapter-19/19.03-json-data.md) · [40 answer records](answer-records.json) · [compact fixture](synthetic-compact.json) · [pretty/reordered fixture](synthetic-pretty.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-json-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-json-review/review.py 5e574af2b055c7822e053fed5d0f5f24870d79bb
```

Baseline command intentionally exits1. [Baseline](baseline.json):2failed predicates,with [identical predicate replay](baseline-replay.json). [Corrected](results.json):39supplemental predicates and3exact-source commands passed (demo/10existing methods,compile,quiet import). One workflow,40local answers and12lab steps reviewed;zero new historical unique methods. No observer correction needed.

## F190 — standalone JSON return-copy alignment

The JSON source copy still rounded end/start before subtracting1 and depended on ambient Decimal precision. It now shares the documented Sections19.1–19.2 complete-ratio/private34digit HALF_EVEN reporting contract. Actual near-unity and ambient-precision failures are retained;private-context reporting is explicit policy alignment rather than a claim that the original promised context isolation. Arbitrary exponent/coefficient resources,currency-specific rounding and financial interpretation remain open. Parser closes must remain strictly positive;standalone return permits a zero terminal and rejects zero initial price.

The source JSON parser itself is unchanged. It accepts UTF-8 bytes,an exact-field object with strings,nonempty stripped instrument,USD,unadjusted_close,valid parsed date andpositive finite Decimal close. It rejects extra/missing fields,top-level scalars/arrays,null/empty/numeric/bool prices,nonstandard constants,duplicates at any nesting,invalid dates/encoding andBOM-prefixed input under its existing UTF-8 contract. Unlike CSV'sutf-8-sig policy,this JSON example does not accept a BOM. No resource cap is implemented or claimed;no oversized/deep-payload denial-of-service validation was attempted. Corporate-action/calendar/point-in-time/API/security/source-quality statements are conceptual boundaries,not executed integrations or certification. F28/F32/F165/F185 remain open.

## Twelve lab-step records

| Step | Prompt | Evidence / limit |
|---|---|---|
| 1 | Fixture/schema | Compact and pretty raw JSON artifacts retained;exact5 string fields,USD/unadjusted close |
| 2 | Types/date | Decimal text preserved;observation date has no instant/timezone/availability implication |
| 3 | Byte identity | hashlib reference SHA256;key/whitespace changes parsed-equivalent but byte-different |
| 4 | Save/environment | Source fence extracted verbatim;Python/platform/source SHA256 and base revision retained |
| 5 | Parse/return | Source demo parses101.50 andreturns.015 from100 |
| 6 | Benchmark | Exact3/200=.015 anddelta1e-30 targets;private precision prevents premature quotient cancellation |
| 7 | Missing key | Required missing close rejected |
| 8 | Null/number/NaN | Separate actual null,numeric-zero,float,bool,NaN/Infinity literals and strings rejected |
| 9 | Duplicates | Top-level and nested duplicates rejected by installed object-pairs hook |
| 10 | Formatting | Compact/reordered pretty objects parse equally;different raw hashes;no canonicalization claim |
| 11 | Reference tests | Ten unchanged existing unique methods executed;three source commands and39supplemental predicates separate |
| 12 | Limits | No live API,pagination,resource limits,source authenticity,licensing,exchange calendar or point-in-time/platform acceptance |

## Forty prompt-to-answer records

| Exercise | Topic | Reviewed answer | Scope |
|---|---|---|---|
| 1 | Object: | A JSON object. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 2 | Array: | A JSON array. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 3 | Null: | No. | Actual source schema/type/byte/return check |
| 4 | Zero: | No. | Actual source schema/type/byte/return check |
| 5 | Empty string: | No. | Actual source schema/type/byte/return check |
| 6 | Price: | No; it is a string. | Actual source schema/type/byte/return check |
| 7 | Decimal: | To retain its specified decimal value under the chosen policy. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 8 | Boolean: | No, under this contract. | Actual source schema/type/byte/return check |
| 9 | NaN: | No. | Actual source schema/type/byte/return check |
| 10 | Duplicate key: | Reject it. | Actual source schema/type/byte/return check |
| 11 | Unknown key: | Reject it. | Actual source schema/type/byte/return check |
| 12 | Top-level array: | No. | Actual source schema/type/byte/return check |
| 13 | Return: | .015 or 1.5%. | Actual source schema/type/byte/return check |
| 14 | Zero starting price: | No. | Actual source schema/type/byte/return check |
| 15 | USD: | No. | Actual source schema/type/byte/return check |
| 16 | Price type: | No. | Actual source schema/type/byte/return check |
| 17 | Date: | No. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 18 | Publication: | To avoid using information before it was known. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 19 | Revision: | No. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 20 | Hash: | The input bytes hashed. | Actual source schema/type/byte/return check |
| 21 | Whitespace: | Yes. | Actual source schema/type/byte/return check |
| 22 | Hash: | No. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 23 | Pagination: | Data may span multiple responses. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 24 | HTTP success: | No. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 25 | Array order: | No. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 26 | Currency: | No. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 27 | Negative yield: | No. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 28 | Negative close: | No. | Actual source schema/type/byte/return check |
| 29 | Schema version: | To interpret and reproduce parsing rules. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 30 | Unknown field: | No; follow a defined policy. | Actual source schema/type/byte/return check |
| 31 | Credentials: | No. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 32 | Untrusted payload: | No. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 33 | Large input: | To control resource use. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 34 | Raw response: | For lineage and reprocessing. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 35 | Nonstandard constant: | No. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 36 | Missing price: | No. | Actual source schema/type/byte/return check |
| 37 | Decimal policy: | No. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 38 | Corporate action: | No. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 39 | Tests: | No. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |
| 40 | Source quality: | No. | Contract/conceptual interpretation;no live source,resource-cap,security or independent acceptance |

Next: Section19.4 Excel Data formal workflow/local-answer review;broader and independent Book1 acceptance remains open.

Nested-duplicate scope:the nested case also contains an extra field,so rejection by that predicate alone would not distinguish the duplicate policy from schema rejection. The source object_pairs_hook applies reject_duplicates at every object level;that mechanism is confirmed by source review rather than treating this combined negative case as isolated parser-depth coverage.

Corrected executable source revision:`0cb56e043276f5f0f2d4496d4adaf3a1a12a593c`. [Publication verification](publication-verification.json) pins this manuscript/observer/fixture snapshot;source inputs remain unchanged in the following verification commit.
