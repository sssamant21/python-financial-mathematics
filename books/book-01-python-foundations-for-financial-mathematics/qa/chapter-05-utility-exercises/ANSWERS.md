# Section5.4 — eight local utility exercises

Source execution, new QA interfaces, cross-section integration and design-only proposals are distinguished per record.

## 5.4-E1 — SOURCE

**Prompt:** Add tests for numeric event IDs and extra event fields.

Numeric event_id1 fails TypeError and an extra event field fails ValueError through original normalize_schedule. Failure leaves supplied rows unchanged; no identity coercion or extra-field dropping.

## 5.4-E2 — SUPPLEMENT

**Prompt:** Add a before-cutoff operation with an explicitly exclusive boundary. State empty and equality cases before coding.

events_before validates exact date cutoff and entire schedule via public normalize_schedule, then selects payment_date<cutoff. Equal date excluded; cutoff before/equal earliest yields identifiable empty wrapper; after latest retains all in date/ID order; empty source stays identifiable. Bad excluded row still rejects and output edits do not alter source. Existing inclusive events_on_or_after remains unchanged.

## 5.4-E3 — SUPPLEMENT+SOURCE

**Prompt:** Write a second runner that uses the same utility with a EUR schedule.

Independent EUR runner supplies SCH-EUR investor events -100 at2027-01-15 and0/+109.5 at2028-02-29, calls original inclusive utility and prints EUR selected IDs: E-RECEIVE, E-ZERO in ID tie order. No conversion/relabel arithmetic, implicit clock or mutable global financial state. Original USD runner and quiet imports also pass.

## 5.4-E4 — SOURCE

**Prompt:** Demonstrate that reversing source order does not change normalized output under the unique-ID rule.

Reversed unique-ID input normalizes identically; explicitly expected E0,E1,E2 date/ID order differs from source E2,E0,E1. Original source remains unchanged. Same-day E1zero/E2positive both retained; event date is not identity.

## 5.4-E5 — SUPPLEMENT

**Prompt:** Add a documented count operation without presenting an event count as an amount total.

count_events validates entire schedule, then returns schedule/currency/perspective plus event_count3 for fixture and0 for empty. Count includes zero/signed events, rejects duplicates first and is cardinality, not money/settled count or cash balance.

## 5.4-E6 — SOURCE_INTEGRATION

**Prompt:** Design an adapter connecting the previous section's canonical output to this input contract. Verify matching fields explicitly.

Section5.3 canonical wrapper fields schedule_id,currency,perspective,events and event fields event_id,payment_date,amount already match5.4. Exact date and Decimal types are checked explicitly. adapt_canonical delegates to original normalize_schedule for full validation/fresh reconstruction/sorting; no conversion needed. Tests use original5.3 parser output, preserve leap-day dates, signed/zero/scaled amounts and parent identity, reject extra metadata and isolate result mutation.

## 5.4-E7 — DESIGN

**Prompt:** Explain what must change before supporting multiple currencies in one schedule.

Per-event currency would require a revised schema, supported-currency and identity policy, grouping/report units and explicit conversion boundary. Keep values separated by currency until a documented FX source/as-of/direction/rounding policy exists; a shared label change is not conversion. Update adapters/callers and version policy, retain provenance. No multi-currency valuation or changed schema implemented.

## 5.4-E8 — DESIGN+BASELINE

**Prompt:** Propose a compatibility test when changing event schema, sign perspective, or duplicate policy.

Keep golden public tests for exact schema fields, investor sign (-1000paid/+1000received), unique IDs across dates, same-day separate events, zeros and inclusive/exclusive boundaries. Reject extra fields and duplicate IDs under current API. Any deliberate new schema/perspective/duplicate policy needs separately named/versioned behavior and caller migration; current golden cases should reveal silent changes. Baseline original9 methods plus new explicit order/field/ownership checks pass; no hypothetical altered policy is claimed tested.
