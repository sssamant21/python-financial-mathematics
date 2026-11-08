# Section19.2 — scoped CSV/text review

Baseline `72aa53dd47dcb91d838e9ece800a1626486e3992`. [Source](../../chapter-19/19.02-csv-and-text-data.md) · [40 prompt/answer records](answer-records.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-csv-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-csv-review/review.py 72aa53dd47dcb91d838e9ece800a1626486e3992
```

Baseline command intentionally exits1. [Baseline](baseline.json) retains4 failed predicates,with [identical predicate replay](baseline-replay.json). [Corrected results](results.json):41 supplemental predicates and5 exact-source commands passed. Commands are verbatim UTF-8-sig read snippet,CSV writer snippet,reference demo/ten existing methods,compile and quiet import. One workflow,40 local answers and12 lab records reviewed;zero new historical methods. Commands,predicates,review records and historical methods are separate. No observer correction needed.

## F189 — CSV header error boundary and return-copy correction

Strict CSV syntax errors while lazily reading headers previously escaped as csv.Error,outside the row-error boundary. Header syntax now raises ValueError consistently with malformed data rows,without returning a partial result. The return copy also retained end/start-1 cancellation and ambient precision after Section19.1 was corrected. It now uses that section's complete rational/34digit private HALF_EVEN report contract. Near-unity cancellation is a numerical defect; private precision/exception conventions are explicit policy alignment rather than retroactive promises. F189 resolved in this scope only;arbitrary Decimal exponent/length resources and currency-specific rounding remain open.

The two modules intentionally have different CSV contracts:19.1 allows extra columns but requires one instrument and increasing dates with at least2 records;19.2 requires the exact field set,permits multiple instruments/unsorted rows,and requires at least1 row with unique instrument/date keys. Actual calls verify those19.2 contracts. Parser closes must be positive;standalone simple_return allows zero terminal value. Linked return comparison is integration parity with a shared implementation,not a new independent oracle.

## Exact artifacts and limits

[LF fixture](synthetic.csv),[BOM fixture](synthetic-bom.csv),[CRLF fixture](synthetic-crlf.csv) and [actual writer output](writer-output.csv) are retained with SHA256 in results. BOM/newline variants decode to the same parsed rows but hash differently as raw bytes. Quoted commas and quoted newlines produce intact fields and2 logical records. Writer output's field order and values are independently read back;syntactic validity is not financial or spreadsheet-export safety acceptance.

This source loads input bytes and retains rows/global duplicate keys;it is not an unbounded-file streaming implementation. No timing/peak-memory claim or spreadsheet formula sanitization,live source,licensing,point-in-time,exchange-calendar,corporate-action or currency conversion acceptance. F28/F32/F165/F185 and independent/platform acceptance remain open.

## Twelve lab-step records

| Step | Prompt | Evidence / limit |
|---|---|---|
| 1 | Synthetic input | CSV fence written as UTF-8 raw bytes; LF,BOM andCRLF artifacts retained |
| 2 | Contract | Comma,exact required field set,USD,positive finite Decimal closes,key instrument/date;multiple instruments and unsorted distinct keys allowed |
| 3 | Byte identity | Independent hashlib SHA256 checks;raw source bytes preserved before decoding |
| 4 | Save/environment | All3 Python fences extracted verbatim;Python/platform/source hashes retained |
| 5 | Parse/return | Exact source demo/tests and supplemental calls produce.015 |
| 6 | Analytical comparison | Exact(101.50-100)/100=3/200;near-unity complete quotient checks independent expected1e-30 |
| 7 | BOM | Same parsed logical rows;different raw hashes;utf-8-sig read snippet executed |
| 8 | Duplicates | Duplicate header/key failures executed;schema header syntax now normalized too |
| 9 | Malformed input | Empty/NA/NaN/infinite/nonpositive prices,wrong widths,invalid dates/encoding,currency and unterminated quotes rejected |
| 10 | Availability | Date alone is not publication/ingestion/decision instant;conceptual review only |
| 11 | Reference tests | 10 existing unique methods passed;five exact-source commands and41 supplemental predicates separate |
| 12 | Evidence/limits | Raw fixtures/writer output/digests retained;no source authenticity,streaming,calendar,point-in-time or platform certification |

## Forty prompt-to-answer records

| Exercise | Topic | Reviewed answer | Scope |
|---|---|---|---|
| 1 | CSV: | No; they are text requiring a schema. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 2 | TSV: | A tab. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 3 | Quoted comma: | No. | Actual source byte/parser/return/write checks |
| 4 | Quoted newline: | No. | Actual source byte/parser/return/write checks |
| 5 | Encoding: | To decode consistently under the stated contract. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 6 | BOM: | Removes a leading UTF-8 BOM if present. | Actual source byte/parser/return/write checks |
| 7 | Header: | Dictionary mapping can overwrite a field. | Actual source byte/parser/return/write checks |
| 8 | Missing field: | No. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 9 | NA marker: | Whatever the documented source policy defines. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 10 | Close 100→101.50: | 1.5%. | Actual source byte/parser/return/write checks |
| 11 | Decimal: | To preserve its specified decimal value. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 12 | NaN price: | No. | Actual source byte/parser/return/write checks |
| 13 | Negative yield: | No. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 14 | Negative close: | No. | Actual source byte/parser/return/write checks |
| 15 | Zero ending price: | Yes. | Actual source byte/parser/return/write checks |
| 16 | Zero starting price: | No. | Actual source byte/parser/return/write checks |
| 17 | Duplicate key: | No; venue or version may matter. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 18 | File date: | Not necessarily. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 19 | Event time: | When an event occurred. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 20 | Ingestion time: | When the system received it. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 21 | Look-ahead: | Yes, if later information is used earlier. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 22 | Checksum: | The hashed bytes. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 23 | Checksum: | No. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 24 | BOM: | Yes. | Actual source byte/parser/return/write checks |
| 25 | Line endings: | Yes. | Actual source byte/parser/return/write checks |
| 26 | Streaming: | No. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 27 | Duplicate set: | Grows with distinct keys. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 28 | Outlier: | No; investigate. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 29 | Close type: | They may have different meanings and returns. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 30 | Currency: | Values in different currencies need defined conversion. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 31 | Rate: | .05. | Independent unit arithmetic:5/100=.05 and1/10000=.0001;no source unit-conversion function |
| 32 | Basis point: | .0001 decimal. | Independent unit arithmetic:5/100=.05 and1/10000=.0001;no source unit-conversion function |
| 33 | Delimiter: | To parse fields consistently. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 34 | Malformed row: | Only under an explicit policy with evidence. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 35 | Spreadsheet export: | Spreadsheet software may interpret formula-like fields. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 36 | Writer: | It handles delimiters and quoting according to the configured dialect. | Actual source byte/parser/return/write checks |
| 37 | Schema: | No; follow a defined policy. | Actual source byte/parser/return/write checks |
| 38 | Calendar: | No. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 39 | Licensing: | Not necessarily. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |
| 40 | Tests: | No. | Contract/conceptual review; not source accuracy,license,availability,streaming or spreadsheet-safety acceptance |

Next: Section19.3 JSON Data formal workflow/local-answer review;broader Book1 validation remains in progress.
