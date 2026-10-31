# E7/E8 — Proposed extensions and test cases, not executed implementations

For E7, a possible signature is load_holdings(path,*,currency,valuation_date,expected_assets). expected_assets comes from an independent approved universe/configuration, not from the file itself. Require a bounded nonempty tuple of unique trimmed nonempty strings. Preserve literal identifier spelling/case; do not strip or normalize to make sets agree. Resolve invalid parameter policy before processing; preserve existing native file/decode/CSV/conversion exceptions and source contract rejections.

Within the pipeline, validate source structure/context/identities, compare observed and expected sets, then value and publish only on exact coverage. This needs an explicit parsing/validation/valuation boundary; the existing public function has no expected-set argument. No adapter or refactor is implemented here. A broader reference universe would need another deliberate policy. Expected-set provenance,valuation date,version and hash should travel beside payload evidence.

| Proposed case | Expected policy | Execution status |
|---|---|---|
| Exact fixture population | Accept existing literal IDs and total1000 | Proposed new API case; not run |
| Same population in different source order | Accept; preserve source row order and keyed values | Proposed new API case; not run |
| Missing BETA | Reject with missing={BETA}; no complete result | Proposed new API case; not run |
| Extra OTHER | Reject with extra={OTHER}; no silent discard | Proposed new API case; not run |
| Duplicate expected name | Reject invalid expected-universe parameter | Proposed new API case; not run |
| Empty/list/nontext/whitespace expected identifiers | Reject invalid expected-universe parameter | Proposed new API case; not run |
| Duplicate/invalid source record | Preserve source rejection before valuation | Proposed new API case; not run |
| Context or structural error despite matching assets | Reject; set equality cannot override other checks | Proposed new API case; not run |

These eight planned cases are design records, not added tests, predicates, workflows or historical methods. Existing-source probes demonstrate acceptance of omitted/extra whole records and original guards; they do not verify the proposed feature.

For E8, pin schema,record grain,currency/date and normalization policy across all chunks. Maintain complete seen-key state with record/batch lineage or a transactional unique index. A record duplicated in chunk2 must be caught even if chunk1 has already produced a subtotal. Stage results and finalize only after no duplicate/schema/context/coverage failure remains. Compare expected-minus-observed and observed-minus-expected at end; reconcile counts and financially valid controls with explicit numerical policy. Hash exact input bytes once under a stable snapshot/stream provenance contract; per-chunk hashes alone do not establish a full-file identity/order policy.

Planned chunk cases include duplicates within one chunk and across nonadjacent chunks,equal-value duplicates,schema/context drift,late parse failure,unexpected/missing assets,empty tail chunks,restart/replay duplication and source changes mid-read. Changing chunk boundaries should preserve the accepted normalized population and valid results under the declared arithmetic policy. Bound seen-key storage or use an external key store; input chunk size does not bound all process memory. Concurrency/restart/atomic publication,resource limits and numerical reconciliation require implementation and actual execution before acceptance. None of these chunked tests ran in this batch.
