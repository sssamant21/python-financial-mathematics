# Sections 4.10–4.12 — scoped worked answers

SOURCE denotes published-function probes; SUPPLEMENT denotes new QA implementations or semantic demonstrations; DESIGN is reasoning only, not execution or acceptance.

## 4.10-E1 — SOURCE

**Prompt:** Reverse the catalog rows and verify that the enriched report is unchanged.

Catalog order is lookup order only; reverse it and expect exactly the same B-before-A report, including zero EUR holding.

## 4.10-E2 — SOURCE

**Prompt:** Add an unused valid security and verify that the holdings list remains unchanged.

Append valid SEC-C metadata; no new holding is created. Invalid unused metadata must still be rejected.

## 4.10-E3 — SOURCE

**Prompt:** Add a test rejecting an extra holding field and another rejecting a numeric holding security ID.

An extra holding field raises ValueError; a numeric security ID raises TypeError. Input records must remain unchanged.

## 4.10-E4 — SUPPLEMENT

**Prompt:** Extend the model to two portfolios sharing one security. State the identity key for a combined report.

Join two validated portfolios separately; combine by (portfolio_id, snapshot_id, security_id). Reject duplicate portfolio/snapshot wrappers. Shared SEC-A remains two positions, not an aggregate.

## 4.10-E5 — DESIGN

**Prompt:** Design a lot-level holding schema. Explain why duplicate security references may then be legitimate.

Use parent portfolio_id and snapshot_id, and lot rows with lot_id, security_id, quantity, acquisition_date and cost_currency/cost_basis under a specified accounting policy. Key=(portfolio_id,snapshot_id,lot_id); repeated security references are legitimate different lots. Lot validation/aggregation is not implemented here.

## 4.10-E6 — SUPPLEMENT

**Prompt:** Add a nested tags field to catalog metadata and define how report ownership should work.

The extended catalog adds tags:list[exact str], retaining order and duplicates. Validate and copy tags for each output row; mutable tag lists never alias catalog or other reports. Original strict catalog rejects this extra field.

## 4.10-E7 — DESIGN

**Prompt:** Propose fields for price provenance without calculating market value yet.

Propose price_value, price_currency, quote_unit, observed_at with timezone, source_id, source_record_id, retrieved_at, catalog_version and adjustment_basis. Define missing/stale/revised rules before valuation; no price multiplication is performed.

## 4.10-E8 — SOURCE

**Prompt:** Explain why changing quote_currency from EUR to USD is not a currency conversion.

Relabel EUR as USD changes metadata only; 0 and 12.5 units stay unchanged. Currency conversion needs an amount, dated exchange-rate direction and source, and rounding policy; holdings units are not currency amounts.

## 4.10-E9 — DESIGN

**Prompt:** Write a rejected-reference report design that preserves invalid holding details rather than substituting zero values.

Rejected-reference report should retain portfolio/snapshot identity, source index, complete original holding, unresolved ID, reason code and catalog version; use a fresh owned copy under a specified serializable schema. Separate accepted/rejected collections and require explicit downstream partial-result acceptance. Never substitute zero for an unresolved quantity/reference. This quarantine API is a design, not executed code.

## 4.11-E1 — SUPPLEMENT

**Prompt:** Demonstrate rebinding a local parameter without changing the caller's list, then contrast it with appending to that list.

Local rebinding to a new list leaves the caller list unchanged; append mutates the shared list. Probe both operations on the same caller.

## 4.11-E2 — SUPPLEMENT

**Prompt:** Add a tags list to a tuple record and demonstrate why the outer tuple alone is insufficient.

A tuple containing tags:list permits tags.append; the outer tuple prevents replacing slots but not mutation of descendants.

## 4.11-E3 — SUPPLEMENT

**Prompt:** Extend capture to a tags tuple of exact strings. Define validation for duplicate tags and order.

Capture exact row fields security_id,quantity,tags. Tags must be an exact tuple of nonempty unpadded exact strings; reject duplicate tags rather than silently discard them, preserve declared order. Return immutable triple rows and reject duplicate security IDs.

## 4.11-E4 — SOURCE

**Prompt:** Write a test rejecting a Decimal subclass under the exact-type policy.

A Decimal subclass is rejected by exact-type quantity validation even when numerically valid; test capture and replacement.

## 4.11-E5 — SOURCE

**Prompt:** Add a test replacing a quantity with the same numeric value. Verify equality and baseline preservation without requiring scalar identity changes.

Replacing SEC-A 12.5 with Decimal("12.50") yields an equal snapshot and new result tuple while preserving baseline. Scalar identity changes are not required.

## 4.11-E6 — SUPPLEMENT

**Prompt:** Implement a separate insert operation with an explicit duplicate-ID policy.

Separate insert validates the whole snapshot, exact ID and quantity, rejects existing ID, and appends a new row in declared order. Empty input is supported; replace continues to reject absent targets.

## 4.11-E7 — SUPPLEMENT

**Prompt:** Design a wrapper that retains portfolio and snapshot identifiers together with captured holdings.

Use an owned wrapper with portfolio_id,snapshot_id,holdings; validate exact nonempty unpadded IDs and capture the immutable holdings component separately. Empty holdings retains parent identity; wrapper metadata is mutable and is not described as frozen.

## 4.11-E8 — DESIGN

**Prompt:** Explain why deepcopy is not a validation strategy for unsupported financial fields.

deepcopy duplicates supported object graphs but does not enforce financial units, required fields, duplicate identity, valid quantities or immutable descendants. Validate schema first; do not treat copied unsupported objects as accepted data.

## 4.11-E9 — DESIGN

**Prompt:** Describe the additional evidence needed to reproduce a valuation from an immutable holdings snapshot.

Reproduction needs security master/version, dated prices and quote units, FX data/conventions, valuation date/timezone, model/code/dependency versions, parameters, numeric context/rounding, input provenance and complete dataset, plus recorded outputs/tolerances. Immutability alone supplies none of these external facts.

## 4.12-E1 — DESIGN

**Prompt:** Choose representations for an ordered payment schedule, a security catalog, and an allowlist. State what each retains and omits.

Use ordered event rows for a payment schedule (identity/date/amount preserved, no implied aggregation), dictionary keyed by unique security ID for catalog (lookup and insertion order, no duplicate identities), frozenset of allowed IDs for allowlist (membership, no multiplicity/report order). Validate before conversion.

## 4.12-E2 — SUPPLEMENT

**Prompt:** Explain why a set of complete transactions can discard legitimate repeated events when identity is absent.

Two identical transaction tuples collapse to one in a set. Separate event IDs distinguish legitimate repeated events; do not deduplicate solely by equal date and amount.

## 4.12-E3 — SOURCE

**Prompt:** Add a test proving that reversing source order reverses snapshot and lookup iteration order while preserving membership equality.

Reversing source reverses snapshot and dictionary iteration order; frozenset membership remains equal, including zero SEC-B.

## 4.12-E4 — SUPPLEMENT

**Prompt:** Add portfolio and snapshot metadata around the three views without placing those mutable dictionaries inside the immutable holdings component.

Use mutable owned parent metadata and views tuple(snapshot,lookup,members); immutable holdings snapshot contains only exact scalar pairs. Changing parent/lookup never changes snapshot or source. This wrapper does not freeze all components.

## 4.12-E5 — DESIGN

**Prompt:** Change the input model to lots and define a composite lookup key before adapting the implementation.

For lots choose composite (portfolio_id,snapshot_id,lot_id) lookup identity, retain security_id as reference and quantity per lot. Validate duplicate lot keys before indexing; same security can appear in several lots. No lot implementation is claimed.

## 4.12-E6 — SUPPLEMENT

**Prompt:** Implement an explicit display function that returns sorted IDs without mutating the views.

display_ids returns a new sorted list of lookup keys. It neither sorts a source in place nor changes snapshot/lookup iteration order; lexicographic exact-ID order is the declared display policy.

## 4.12-E7 — SOURCE

**Prompt:** Add an exact-type rejection test for a string subclass.

A subclass of str fails the exact string ID policy even if it compares equal to a valid ID.

## 4.12-E8 — DESIGN

**Prompt:** Describe when maintaining only the ordered snapshot would be simpler than maintaining all three views.

Only snapshot is simpler for small, read-mostly ordered traversals without repeated random lookup or membership workloads. Build other views only for measured needs; no speed or memory benchmark is claimed.

## 4.12-E9 — DESIGN

**Prompt:** Design a rebuild policy for an application receiving a corrected source snapshot. State how it avoids mixing old and new views.

Validate an entire corrected source under a new version, build all views privately, then replace one versioned wrapper as a unit. Readers pin that wrapper/version; do not refresh lookup independently. Concurrency, persistence and atomic publication require an application-level mechanism not implemented by the lab.
