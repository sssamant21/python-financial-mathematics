# Section 6.2 — eight scoped exercise answers

Prerequisites: the documented Python/NumPy environment, an owned writable temporary directory and sufficient local memory for two 4 MB numeric payloads. Actual run: CPython 3.12.14, NumPy 2.3.5, Linux. Source execution, supplemental caller and design reviews are distinct.

## 6.2-E1 — SOURCE + SUPPLEMENTAL CALLER

**Prompt:** Add a third observation date, update labels, and predict every reported array attribute before running.

Add 2026-01-07 with prices [103,78,52] after the two original rows, retaining ASSET-A/B/C column order. Before execution: shape (3,3), ndim 2, size 9, dtype float64, itemsize 8 and nbytes 3*3*8=72. The source output agrees with all predictions and preserves the three supplied rows exactly. third_date.py is a separate guarded caller whose full stdout is checked. The original two-date demonstration/listings remain unchanged.

## 6.2-E2 — SOURCE

**Prompt:** Compare the shapes (3,), (1, 3), and (3, 1). Explain which the snapshot API accepts and why.

A (3,) vector has rank one and fails regardless of whether its values are valid prices. A (1,3) row and (3,1) column each have rank two and are accepted with matching one-date/three-ID and three-date/one-ID label tuples respectively. Both fail if the original two-date/three-ID labels are reused. Adding an axis changes structure and meaning; it is not an automatic repair for label mismatches.

## 6.2-E3 — SOURCE

**Prompt:** Add a test that duplicate observation labels fail even when price values are otherwise valid.

Use the valid 3x3 price table with dates (same,same,last). The original price_snapshot raises ValueError for duplicate observation labels, despite finite nonnegative prices and correct axis lengths. The expected exception and traceback are retained. Label uniqueness is part of this API contract, not a proof that real data provenance is correct.

## 6.2-E4 — SOURCE

**Prompt:** Modify the returned snapshot and verify the source is unchanged.

Modify the returned writable snapshot at [0,0]; the source bytes remain identical. Then change the source at [1,0]; the already returned snapshot retains 105 there. The result shares no numeric storage with the source. A transposed read-only source also yields an independent writable C-order copy while its original write permission remains false. Independence and immutability are different properties.

## 6.2-E5 — SOURCE + CONCEPTUAL INTERPRETATION

**Prompt:** Explain why a copy of correct numbers with wrong instrument labels remains financially wrong.

Keep the numeric rows unchanged but swap ASSET-A and ASSET-B labels. Unique valid text and matching lengths let the original API accept and copy the data. The copied values are correct stored numbers but belong to wrong identities, so downstream calculations remain financially wrong. A copy cannot authenticate the labels; ingestion must preserve reviewed record identity/order, units and observation provenance.

## 6.2-E6 — DESIGN + SOURCE-LIMIT PROBES

**Prompt:** Design a separate date-parsing/chronology boundary without silently sorting only the labels.

Design a separate boundary that requires canonical YYYY-MM-DD text, checks lexical form and real calendar validity, rejects duplicate parsed dates and requires strictly increasing observations under a stated date/calendar policy. Keep each row paired with its label. Prefer rejecting unexpected order; if sorting is an explicit permitted transformation, apply the same stable permutation to complete row records and preserve original order/provenance. Datetimes need their own timezone/instant and ambiguity contract. Source probes confirm that the current API accepts non-calendar text and does not sort reversed labels; no chronology validator or sorting adapter was implemented or claimed tested.

## 6.2-E7 — SOURCE + INTEGER ESTIMATE

**Prompt:** Estimate the element payload of a 1,000-by-500 float64 table and distinguish it from total memory.

A 1000-by-500 float64 table contains 500000 entries * 8 bytes = 4000000 bytes, or 4.0 MB decimal / about 3.8147 MiB. Allocate that synthetic source table and call the unchanged API with matching generated label tuples: both source and copy report exactly 4000000 element bytes and do not share storage. While both are live their combined element payload is 8000000 bytes, before labels, objects, validation masks, temporaries, allocator state and other process memory. No peak-memory measurement or operating-system reservation is claimed.

## 6.2-E8 — CONCEPTUAL DESIGN ONLY

**Prompt:** State how a concurrent writer would invalidate a stronger transactional-snapshot claim.

Validation and copying are separate reads of caller-owned mutable storage. A concurrent writer could change values after validation or during copying, so a returned array might reflect different logical versions or values not covered by the earlier check. Independence after return does not make the capture linearizable or transactional. A stronger design needs a shared ownership/locking protocol covering validation plus copy and respected by every writer, or an immutable/versioned source snapshot with a reviewed consistency protocol. Copying or setting only one view read-only does not by itself exclude all writers. No live concurrent-writer experiment or synchronization implementation was executed.
