# Section19.6 — scoped parsing/validation workflow review

Baseline `30fe802218e5ad9978031287330cd887ebbcf1dc`. [Source](../../chapter-19/19.06-parsing-and-validation.md) · [40 answer records](answer-records.json) · [synthetic decoded batch](synthetic-batch.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-validation-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-validation-review/review.py 30fe802218e5ad9978031287330cd887ebbcf1dc
```

Baseline command intentionally exits1. [Baseline](baseline.json) retains2failed predicates with [identical predicate replay](baseline-replay.json). [Corrected](results.json):33supplemental predicates and3source commands passed (demo/12existing methods,compile,quiet import). One workflow,40local answers/12lab records reviewed;zero new historical unique methods. No observer correction needed.

## F193 — validation return-copy alignment

The standalone helper retained premature end/start-1 rounding andambient Decimal precision after adjacent modules were corrected. It now uses their complete-ratio/private34digit HALF_EVEN policy. Near-unity arithmetic failure is distinct from explicit context/reporting-policy alignment. Exact zero/zero terminal remain valid;unreportable finite/nonzero reports raise ValueError. Arbitrary exponent/coefficient resources,currency-specific rounding andfinancial/source suitability remain open. No batch/parser behavior was changed.

## Independent expectations andquarantine contracts

Complete(101.50-100)/100=3/200=.015 andunit-scale long-decimal difference1e-30 provide independent arithmetic targets. The mixed5-row fixture has exactly2accepted rows and3rejections:index2close,index3duplicate,index5currency. Accepted dates remain in input order. Later valid duplicates are quarantined after normalization;an earlier invalid record doesnot reserve its key. Caller input is unchanged. Error records contain only1-based index/reason codes,not full raw rows. Canonical YYYY-MM-DD is enforced:compact,week-date anddatetime spellings are rejected even if another parser could interpret them. This exact-date contract is stricter than earlier date.fromisoformat-only examples.

Empty input is completeTrue by explicit teaching policy;unsorted valid dates remain accepted. Neither means actual market-source coverage is complete. The observer serializes synthetic decoded input andretains its checksum;the source is not a CSV/JSON decoder andthese are not original retrieval bytes. Downstream-publication gates,threshold approvals,source authenticity/availability,venue/price type/calendar/corporate actions,resource/security/platform andindependent acceptance are not implemented orcertified. F28/F32/F165/F185 remain open.

## Twelve lab-step records

| Step | Prompt | Evidence / limit |
|---|---|---|
| 1 | Contract/key | Already-decoded dictionaries,exact4string fields,canonical YYYY-MM-DD,USD,positive finite Decimal text;key stripped instrument/date |
| 2 | Save/environment | Reference fence extracted verbatim;Python/platform/source SHA256 andbase revision recorded |
| 3 | Good batch/return | Source demo two accepted/zero rejected/completeTrue;actual return.015 |
| 4 | Benchmark | Exact3/200=.015 andnear-unity1e-30 targets;private reporting context |
| 5 | Schema failure | Missing/extra fields andnonobject rows reject withschema reason |
| 6 | Close errors | Null/bool type reason;empty/NaN/Infinity/nonpositive close reason;no zero substitution |
| 7 | Currency | EUR rejected withcurrency reason;no implicit conversion |
| 8 | Duplicate quarantine | Later normalized valid duplicate quarantined;invalid earlier row doesnot reserve a key;actual indices/reasons retained |
| 9 | Downstream policy | Illustrative design:reject downstream publication ifany rejected row;completeTrue alone also needs source-coverage requirements. No publisher orapproved thresholds implemented |
| 10 | Missing semantics | No price-type/venue/source/publication/revision/availability contract;conceptual review only |
| 11 | Tests | 12unchanged existing unique methods passed;3source commands/33supplemental predicates separate |
| 12 | Input/evidence | Synthetic decoded batch serialized/digested;not original source bytes. Counts/order/empty policy/caller immutability checked;resource/independent acceptance remains open |

## Forty prompt-to-answer records

| Exercise | Topic | Reviewed answer | Scope |
|---|---|---|---|
| 1 | Syntax: | Whether input conforms to its representation. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 2 | Schema: | Expected fields, types and structure. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 3 | Domain: | Positive and finite under this contract. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 4 | Business meaning: | No. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 5 | Missing key: | No. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 6 | Null: | No. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 7 | Empty close: | No. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 8 | NaN: | No. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 9 | Infinity: | No. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 10 | Zero close: | No. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 11 | Negative yield: | No. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 12 | Currency: | No. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 13 | Date: | Yes. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 14 | Date: | No. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 15 | Date: | No. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 16 | Return: | .015 or 1.5%. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 17 | Start price: | To avoid an invalid denominator under the contract. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 18 | Decimal: | No. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 19 | Duplicate: | Quarantine later occurrences. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 20 | Revision: | No. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 21 | Key: | No. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 22 | Venue: | Yes, depending on the dataset. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 23 | Fail-fast: | Stop or reject on failure according to policy. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 24 | Quarantine: | Separate invalid records for review. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 25 | Rejected row: | No. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 26 | Empty batch: | Complete; real policy may reject it. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 27 | Ordering: | No. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 28 | Raw bytes: | No. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 29 | Hash: | No. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 30 | Outlier: | No; investigate. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 31 | Corporate action: | Yes. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 32 | Publication time: | No. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 33 | Look-ahead: | Yes. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 34 | Time zone: | No. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 35 | Memory: | Yes. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 36 | Sensitive data: | No. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 37 | Schema change: | No; exact fields are required. | Actual decoded-record/domain/date/quarantine/arithmetic checks |
| 38 | Completeness: | No. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 39 | Tests: | No. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |
| 40 | Production: | No. | Contract/conceptual review;not syntax decoder,source completeness,publication/financial/platform acceptance |

Next:Section19.7 Schema andData Types formal workflow/local-answer review;broader Book1 validation remains in progress.
