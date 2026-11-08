# Section19.1 — scoped source/format workflow review

Baseline `7789936172ba8ca0545bc051eddee4f9ee08a3cd`. [Source](../../chapter-19/19.01-financial-data-sources-and-formats.md) · [40 answer records](answer-records.json) · [synthetic CSV](synthetic-input.csv) · [synthetic JSON](synthetic-record.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-sources-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-sources-review/review.py 7789936172ba8ca0545bc051eddee4f9ee08a3cd
```

Baseline command intentionally exits1. [Baseline](baseline.json) retains4 failed predicates, with [identical predicate replay](baseline-replay.json). [Corrected results](results.json):41 supplemental predicates and3exact-source commands passed (demo/10 existing methods,compile,quiet import). One workflow,40 local answers and12lab-step records reviewed. Zero new historical unique methods; command predicates and review records are separate. No observer correction was needed.

## F188 — complete Decimal return/report contract

The prior end/start-1 rounded the quotient before subtraction, losing a nonzero near-unity return at ordinary precision. Results also depended on ambient Decimal precision. The helper now derives the complete exact rational quotient from supplied Decimal values and reports34 significant digits with ROUND_HALF_EVEN in a private context, normalizing unreportable decimal results to ValueError. One baseline predicate requiring34digits and the ambient-context case are explicit reporting-policy adoption, not prior promises of context isolation. Exact zero remains allowed; nonzero underflow is rejected. Arbitrary coefficient/exponent resource limits and currency-specific cash rounding remain open; this does not validate the underlying price/currency/model.

The oracle directly constructs the complete Fraction return, converts at120 decimal digits, then rounds to34digits; the source converts the exact ratio directly at34digits. Shared arithmetic backends mean this is independent expectation/ordering, not arithmetic-library certification. Tests include very close long-decimal prices,constant/extreme-scale values,nonterminating fractions,zero terminal,invalid types/domains and hostile ambient precision. Parser prices must be positive; the return helper separately allows a zero terminal. That contract difference is intentional and recorded.

## Prerequisites and limits

Input is Python str CSV text; required columns are instrument,date,close,currency with no duplicate header names. Extra columns are allowed. At least2 records,one nonempty instrument,USD currency,positive finite Decimal closes and strictly increasing parsed dates are required. Dates use Python date.fromisoformat, not a timezone/publication-time validator. JSON is an illustrative record, not an implemented JSON schema parser. Excel/Parquet/API/database/licensing/point-in-time/corporate-action behaviors are conceptual review, not executed integrations. Raw text and normalized UTF-8 digest are not asserted equal to unknown original source bytes. F28/F32/F165/F185 and independent/platform acceptance remain open.

## Twelve lab-step contracts

| Step | Prompt | Evidence / limit |
|---|---|---|
| 1 | Question/model | Synthetic one-instrument USD unadjusted closes; no live market/source-authenticity claim |
| 2 | CSV fixture | Exact Section8 CSV fence retained in synthetic-input.csv; JSON example retained separately |
| 3 | Format/schema | Comma headers instrument/date/close/currency,dates normalized by date.fromisoformat; required-column subset permits extra columns |
| 4 | Save/environment | Reference fence extracted verbatim per selected revision; Python/platform/source hash recorded |
| 5 | Parse/return | Actual source call and demo run; two valid increasing dates,Decimal prices,return.015 |
| 6 | Independent benchmark | Complete exact rational return converted through120-digit oracle then34-digit expected rounding;1.5% benchmark exact |
| 7 | Duplicate date | Actual ValueError probe and existing method; decreasing date separately rejected |
| 8 | Bad input | Malformed row/missing header/duplicate header/invalid price/currency/instrument/date/short sample probes executed |
| 9 | Digest | Exact UTF-8 fixture digest compared independently; LF/CRLF digest difference retained; no raw-file-byte equivalence claim |
| 10 | Missing times | Observation dates do not supply event/publication/ingestion instants; conceptual design review only |
| 11 | Tests | 10 existing methods executed unchanged;3source commands and41 supplemental predicates separate |
| 12 | Limits | Schema/source/units/point-in-time/licensing/platform/resource limits retained; no production or independent acceptance |

## Forty prompt-to-answer alignment records

| Exercise | Topic | Reviewed answer | Disposition |
|---|---|---|---|
| 1 | Category: | Quote data. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 2 | Category: | Trade data. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 3 | Category: | Reference data. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 4 | Category: | Corporate action. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 5 | Category: | Fundamental data. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 6 | Price: | No. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 7 | Ticker: | No. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 8 | CSV: | No. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 9 | JSON: | No. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 10 | Excel: | They can differ or be stale. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 11 | Parquet: | A format, not data quality. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 12 | Date: | No. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 13 | Event time: | When the event occurred. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 14 | Publication time: | When information became available. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 15 | Ingestion time: | When the system received or stored it. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 16 | Look-ahead: | It can leak future information. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 17 | Revision: | No. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 18 | Return: | .015, or 1.5%. | Numeric/unit check in supplemental predicates |
| 19 | Currency: | 100 dollars. | Numeric/unit check in supplemental predicates |
| 20 | Rate: | .05. | Numeric/unit check in supplemental predicates |
| 21 | Basis point: | .0001. | Numeric/unit check in supplemental predicates |
| 22 | Decimal: | To preserve the specified decimal representation. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 23 | Price: | No. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 24 | Missing value: | No. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 25 | Duplicate: | A defined record key. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 26 | Outlier: | No; investigate. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 27 | Split: | Yes. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 28 | Adjusted price: | No. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 29 | License: | Not necessarily. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 30 | Checksum: | The bytes hashed. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 31 | Checksum: | No. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 32 | API: | Results may span multiple pages. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 33 | API: | Data can change or be revised. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 34 | Timezone: | To interpret and align event instants. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 35 | Calendar: | No. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 36 | Schema: | A record fails the stated schema. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 37 | Raw data: | To support lineage and reprocessing where permitted. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 38 | Code version: | To identify the transformation used. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 39 | Return: | Not without a defined conversion. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |
| 40 | Validation: | No. | Conceptual/source/schema/interpretation alignment; no external-format/live-source acceptance |

Next: Section19.2 CSV and Text Data formal workflow/local-answer review. Broader Book1 validation remains in progress.
