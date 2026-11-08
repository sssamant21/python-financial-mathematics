# Section19.4 — scoped Excel workflow/answer review

Baseline `2e211d5f6b7c0d1875a7f84000083ddaca425554`. [Source](../../chapter-19/19.04-excel-data.md) · [40 answer records](answer-records.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-excel-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-excel-review/review.py 2e211d5f6b7c0d1875a7f84000083ddaca425554
```

Baseline command intentionally exits1. [Baseline](baseline.json) retains2failed predicates with [identical predicate replay](baseline-replay.json). [Corrected](results.json):36supplemental predicates and4exact-source commands passed (row-inspection snippet,reference demo/ten existing methods,compile,quiet import). One workflow,40local answers and12lab records reviewed;zero new historical unique methods. No observer correction needed. Exact examples use openpyxl as the manuscript specifies;fixtures are validation inputs,not authored financial-report deliverables.

## F191 — Excel return-copy correction

The standalone Excel return helper retained end/start-1 near-unity cancellation and ambient Decimal precision after adjacent modules were corrected. It now uses their complete-ratio/private34digit HALF_EVEN policy. Exact zero/zero terminal remain allowed;unreportable finite/nonzero reports raise ValueError. Near-unity arithmetic failure is distinct from explicit context-isolation/reporting policy adoption. No workbook-parser behavior was changed. Arbitrary exponent/coefficient resource bounds,currency-specific cash rounding and financial/model suitability remain open.

## Retained workbook evidence and scope

[Initial workbook bytes](fixture-base64.json),[initial fixture archive](fixtures-initial.json),[corrected-run fixtures](fixtures-current.json) and [baseline-replay fixtures](fixtures-baseline-replay.json) retain base64 ZIP payloads with SHA256. Decode an entry's base64 with Python base64.b64decode to recover its exact.xlsx input. The observer imports the exact source example generator once for a retained initial fixture;ZIP/core timestamps can differ between fresh source-generated workbooks. Source command outputs retain their actual per-run hashes;we do not claim repeated generation is byte-identical. Supplemental baseline/replay predicates reuse retained initial bytes andcompare actual semantics/errors,not timestamps of newly serialized mutants.

Formula fixtures retain formula=100+1.5 in cellC3 and a manually seeded101.5 cache. Actual openpyxl reads show missing cacheNone and seeded cache101.5 under data_only=True;data_only=False preserves the expression. Neither is native Excel recalculation or cache freshness certification. The import rejects formulas regardless of a cache. No macros were executed and no external workbook/user files were opened.

Actual serialized fixtures cover1900/1904 workbook date systems,hidden rows,blank rows,numeric/string closes,formulas,headers,key/record errors andmerged cells. Direct helper checks cover timezone andnumeric rejection. Corrupt archive BadZipFile remains an intentional documented library-level error,not silently converted or claimed secure. The parser uses raw bytes plus retained rows/keys:read_only does not make it bounded-memory. No native UI/visual layout,full legacy date-system quirks,recalculation,external-link trust,source authenticity,corporate-action,exchange-calendar,point-in-time or supported-platform/independent acceptance. F28/F32/F165/F185 remain open.

## Twelve lab-step records

| Step | Prompt | Evidence / limit |
|---|---|---|
| 1 | Contract | Prices sheet,exact ordered instrument/date/close/currency,USD,formula rejection,positive closes;no financial-source authenticity claim |
| 2 | Synthetic workbook | Exact source example_workbook used;initial bytes retained as base64 with SHA256;additional serialized variants are supplemental |
| 3 | Raw identity | Independent SHA256 for the retained initial bytes;archive entries and digests retained |
| 4 | Versions | Python/platform/openpyxl3.1.5 recorded;source fence extracted verbatim |
| 5 | Parse/return | Actual source demo and supplemental parse return.015 |
| 6 | Analytical benchmark | (101.50-100)/100=3/200=.015;long-decimal delta1e-30 checked |
| 7 | Formula rejection | Actual formula cell rejected whether cache absent or manually seeded |
| 8 | Formula/cache | data_only=False returns formula;True returnsNone without cache and101.5 from manually seeded OOXML;no formula engine/recalculation proof |
| 9 | Bad data | Duplicate keys,missing price,bad dates/nonmidnight,extra/order/formula headers,EUR,bool andmerged-cell missing values rejected |
| 10 | Visibility/blanks | Actual hidden-row inclusion andfully blank-row skipping verified;retained keys/rows imply growing memory |
| 11 | Reference suite | 10existing methods passed;4source commands and36supplemental predicates separate |
| 12 | Limits | Dates1900/1904 tested;legacy date quirks,native Excel/UI/recalculation,macros,trust,resource limits,source/model/platform acceptance remain open |

## Forty prompt-to-answer records

| Exercise | Topic | Reviewed answer | Scope |
|---|---|---|---|
| 1 | Workbook: | The workbook. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 2 | Sheet: | No. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 3 | Cell formatting: | No. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 4 | Formula: | No. | Actual serialized-workbook/helper/source check |
| 5 | data_only: | Cached formula values when available. | Actual serialized-workbook/helper/source check |
| 6 | Cache: | No. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 7 | Formula policy: | Reject formulas in imported cells. | Actual serialized-workbook/helper/source check |
| 8 | Return: | 1.5%. | Actual serialized-workbook/helper/source check |
| 9 | Date: | No. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 10 | Datetime: | No. | Actual serialized-workbook/helper/source check |
| 11 | Date system: | Serial dates depend on workbook date-system conventions. | Actual serialized-workbook/helper/source check |
| 12 | Boolean price: | No. | Actual serialized-workbook/helper/source check |
| 13 | NaN price: | No. | Actual serialized-workbook/helper/source check |
| 14 | Negative yield: | No. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 15 | Negative close: | No. | Actual serialized-workbook/helper/source check |
| 16 | Numeric float: | Not necessarily. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 17 | Decimal string: | To preserve the supplied decimal text under the contract. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 18 | Blank row: | Skip an entirely blank row. | Actual serialized-workbook/helper/source check |
| 19 | Hidden row: | No. | Actual serialized-workbook/helper/source check |
| 20 | Merged cells: | Yes. | Actual serialized-workbook/helper/source check |
| 21 | Duplicate key: | No. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 22 | Hash: | No. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 23 | Raw workbook: | For lineage and reprocessing. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 24 | Macro: | No. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 25 | Untrusted input: | To manage resource use. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 26 | Source date: | No. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 27 | Revision: | Yes, if used before it was available. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 28 | Sheet name: | Explicitly report the schema failure. | Actual serialized-workbook/helper/source check |
| 29 | Header: | Four exact ordered headers. | Actual serialized-workbook/helper/source check |
| 30 | Currency: | No. | Actual serialized-workbook/helper/source check |
| 31 | File size: | No; raw bytes and records are retained. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 32 | Formula cache: | Yes. | Actual serialized-workbook/helper/source check |
| 33 | Publication time: | No. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 34 | Rounding: | No. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 35 | Source version: | To identify the workbook used. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 36 | Library version: | To support reproducibility. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 37 | Extra columns: | No. | Actual serialized-workbook/helper/source check |
| 38 | Currency conversion: | No. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 39 | Tests: | No. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |
| 40 | Source accuracy: | No. | Source/contract/conceptual review;not native Excel,trust,resource or independent acceptance |

Next: Section19.5 APIs and Financial Data formal workflow/local-answer review;broader Book1 validation remains in progress.

Dependency prerequisite:openpyxl3.1.5 was already installed;the installation command was not rerun. Native Excel recalculation/UI/platform checks remain unexecuted.
