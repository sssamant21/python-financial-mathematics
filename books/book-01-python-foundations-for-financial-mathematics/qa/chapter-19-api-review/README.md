# Section19.5 — scoped injected-API workflow review

Baseline `dea228397b36589d91f7b325b48a8165a5c43a4e`. [Source](../../chapter-19/19.05-apis-and-financial-data.md) · [40 answer records](answer-records.json) · [synthetic decoded page fixture](synthetic-page.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-api-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-api-review/review.py dea228397b36589d91f7b325b48a8165a5c43a4e
```

Baseline command intentionally exits1. [Baseline](baseline.json) retains2failed predicates with [identical predicate replay](baseline-replay.json). [Corrected](results.json):45supplemental predicates and3exact-source commands passed (demo/ten existing methods,compile,quiet import). One workflow,40local answers and12lab records reviewed;zero new historical unique methods. No observer correction needed.

## F192 — mock-API return-copy alignment

The standalone API return helper retained end/start-1 near-unity cancellation andambient Decimal precision after adjacent modules were corrected. It now uses their complete-ratio/private34digit HALF_EVEN report policy. Actual near-unity andambient-precision failures retained;context isolation is explicit reporting-policy adoption rather than an original guarantee. Exact zero/zero terminal remain valid;unreportable finite/nonzero reports raise ValueError. Arbitrary exponent/coefficient resources,currency rounding andfinancial suitability remain open. No pagination behavior was changed.

## Actual collection and independent expectations

Mock collection completes only on next_cursorNone,or raises on duplicate keys/cursor cycles/page limits/schema errors/fetch exceptions. Actual traces cover2-page success,one-page limit,3-call cycle andsecond-page failure. Empty complete datasets andempty intermediate pages are allowed;provider order andopaque whitespace cursors are retained. Normalized instrument/date duplicate keys reject across pages. No silent partial list is returned on the tested errors;this does not roll back external effects a future fetch implementation might perform. Limit validation precedes fetch calls.

The fixture is a serialized synthetic decoded Python payload,not original HTTP response bytes. This collector does not implement raw-JSON duplicate-key detection,HTTPstatus/authentication/TLS,networktimeouts/retries orprovider-specific completeness. The 1.5% target follows exact(101.50-100)/100=3/200;the narrow helper assumes comparable same-currency/instrument prices selected by the caller. Mixed instruments/provider order are not a return-pair selection implementation. Shared complete-return helper logic is integration alignment,not an independent library certification. F28/F32/F165/F185 remain open.

## Hypothetical bounded retry design — lab10,unexecuted

For a fictional permitted read-only operation:a maximum3attempts,5second overall deadline and1second total request budget per attempt;full-jitter delays bounded by.2 and.4seconds after the first2failures. Without Retry-After,the nominal request-plus-delay budget is at most3.6seconds,excluding scheduling/transport limitations. A real implementation must bound connect/read/total behavior andremaining deadline;valid provider retry guidance may be followed only within that remaining budget,otherwise stop incomplete. Retry only provider-permitted transient conditions;do not blindly retry writes/authentication/invalid requests. These are illustrative design assumptions,not executed transport/retry code or a provider recommendation. No credentials,live requests,network waits orproduction actions were used.

## Twelve lab-step records

| Step | Prompt | Evidence / limit |
|---|---|---|
| 1 | Fictional data question | Synthetic USD unadjusted comparable closes;no live provider/forecast/pricing claim |
| 2 | Response contract | Decoded dict with exact records/next_cursor fields;records list,all row fields strings,positive finite Decimal close |
| 3 | Cursor/completion | InitialNone,opaque nonempty string cursors,completionNone;whitespace cursor retained exactly |
| 4 | Save/environment | Reference fence extracted verbatim;Python/platform/source hash retained |
| 5 | Collect/count | Actual source mock2pages;fetch trace[None,p2],2records,max_pages2 completes |
| 6 | Return benchmark | Exact3/200=.015;near-unity delta1e-30 andambient precision checked |
| 7 | Repeated cursor | Actual3-call cycleNone,a,b thenrepeateda rejected;no fourth fetch |
| 8 | Page cap | max_pages1 yieldsRuntimeError after1call;no partial list returned |
| 9 | Bad records | Null/nonfinite/bool/numeric/invalid fields andnormalized cross-page duplicate keys rejected |
| 10 | Hypothetical retry | Design record below only;no HTTP/timeouts/backoff execution or provider-specific approval |
| 11 | Reference tests | 10unchanged existing unique methods passed;3source commands and45supplemental predicates separate |
| 12 | Provenance/gaps | Synthetic page fixture/actual call traces retained;no actual retrieval/publication timestamps,HTTPstatus/authentication/pagination-provider contract or point-in-time acceptance |

## Forty prompt-to-answer records

| Exercise | Topic | Reviewed answer | Scope |
|---|---|---|---|
| 1 | API: | An interface for requesting or receiving defined resources. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 2 | GET: | Retrieve a resource under the provider contract. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 3 | Token: | No; use approved secret handling. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 4 | HTTPS: | To protect transport according to the client and provider security configuration. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 5 | Status: | No. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 6 | Page: | No. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 7 | Cursor: | No; treat it as opaque. | Actual injected page/schema/arithmetic/call-trace checks |
| 8 | Repeated cursor: | Raise an error. | Actual injected page/schema/arithmetic/call-trace checks |
| 9 | Page limit: | Report an incomplete result. | Actual injected page/schema/arithmetic/call-trace checks |
| 10 | Empty final page: | Yes. | Actual injected page/schema/arithmetic/call-trace checks |
| 11 | Return: | 1.5%. | Actual injected page/schema/arithmetic/call-trace checks |
| 12 | Price representation: | No; it is a string. | Actual injected page/schema/arithmetic/call-trace checks |
| 13 | Null close: | No. | Actual injected page/schema/arithmetic/call-trace checks |
| 14 | NaN close: | No. | Actual injected page/schema/arithmetic/call-trace checks |
| 15 | Currency: | No. | Actual injected page/schema/arithmetic/call-trace checks |
| 16 | Duplicate key: | Instrument and date. | Actual injected page/schema/arithmetic/call-trace checks |
| 17 | Venue: | No. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 18 | Timeout: | To avoid waiting indefinitely. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 19 | Rate limit: | No. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 20 | Backoff: | To reduce synchronized retry bursts. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 21 | Retry-After: | Follow a valid provider instruction within the client's bounded policy. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 22 | Write retry: | No; check idempotency and side effects. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 23 | Authentication failure: | No; correct access or credentials. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 24 | Observation date: | Not necessarily. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 25 | Retrieval time: | When the client obtained the response. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 26 | Revision: | Yes. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 27 | Look-ahead: | Using information before it was available. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 28 | Current data: | No. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 29 | Hash: | The hashed bytes. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 30 | Hash: | No. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 31 | Logs: | No. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 32 | License: | No. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 33 | Cache: | No. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 34 | Provider limit: | Yes; check current documentation. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 35 | Partial failure: | No. | Actual injected page/schema/arithmetic/call-trace checks |
| 36 | Order: | No; it preserves provider order. | Actual injected page/schema/arithmetic/call-trace checks |
| 37 | Memory: | No. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 38 | Network: | No. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 39 | Tests: | No. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |
| 40 | Quality: | No. | Contract/conceptual/design review;no live HTTP/authentication/retry/provider acceptance |

Next:Section19.6 Parsing and Validation formal workflow/local-answer review;broader Book1 validation remains in progress.
