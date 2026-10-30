# Section5.3 — eight local exercise answers

SOURCE executes original parser; SUPPLEMENT introduces explicitly named teaching interfaces; DESIGN/DERIVATION is explanatory review, not executed settlement/valuation.

## 5.3-E1 — SOURCE

**Prompt:** Add an extra event field and verify the schema rejects it.

Appending extra to an otherwise valid event causes ValueError under the exact event-field schema. Other fields are not silently discarded; source parser unchanged.

## 5.3-E2 — SUPPLEMENT

**Prompt:** Define a stricter decimal-text grammar with no exponent or underscore syntax. Add lexical and numeric-domain tests separately.

strict_amount accepts exact ASCII text matching [+-]?(0|[1-9][0-9]*)(.[0-9]+)? with literal decimal point (see escaped regex in code). Signed amounts/zero allowed; no exponent, underscore, padding, leading-zero integers, bare fractional form or trailing dot. Separate finite_amount enforces exact finite Decimal numeric domain. Lexical tests and direct numeric-domain tests are distinct: nonfinite tokens fail grammar, and NaN/sNaN/±Infinity Decimal values fail the domain helper. This is a new scalar interface; original schedule parser still permits Decimal exponent syntax.

## 5.3-E3 — SUPPLEMENT

**Prompt:** Add explicit maximum payload length before JSON decoding. Document what that limit does and does not bound.

limited_parse requires an exact string and positive exact integer maximum_chars (default4096), checks len(payload) before invoking unchanged parser. At-boundary valid input passes, one below rejects; oversized malformed JSON never reaches parser (observed via a temporary delegated-call counter restored afterward). Limit counts Unicode characters, not UTF8 bytes; input string is already allocated. It does not independently establish network/file byte bounds, nesting/recursion policy, token-specific caps, elapsed CPU/memory guarantees or hostile-ingestion certification. Total characters indirectly bound contained spellings only.

## 5.3-E4 — SOURCE

**Prompt:** Add a file test for malformed JSON in a correctly encoded UTF-8 file.

A malformed JSON document with SCH-é is saved as valid UTF8. read_schedule raises JSONDecodeError after successful text decoding, and file bytes remain unchanged; this differs from UnicodeDecodeError and missing-file failure. No empty fallback.

## 5.3-E5 — SOURCE

**Prompt:** Add a test rejecting an invalid later date while preserving the earlier valid events in the caller's source text.

Later event date2027-02-29 is impossible; full source parse raises ValueError. Earlier E0 remains unchanged in the original source text and decoded caller snapshot. No partial accepted schedule is returned; do not coerce invalid date to another day.

## 5.3-E6 — SUPPLEMENT

**Prompt:** Design an explicit wire exporter for canonical date and Decimal fields, then test a round trip without converting through float.

export_schedule accepts exact canonical wrapper/events and scalar date/Decimal fields, investor perspective, USD/EUR; rejects extra fields rather than discarding data. Dates become isoformat text and Decimal becomes str directly. Validate full emitted wire with original parser before returning; duplicates reject. Round trips retain event order, same-day identity, empty metadata, signed zero, exponent and long fractional Decimal tuple/scale without float. Wrong datetime/float/nonfinite/extra-field cases reject. This exporter follows original broad amount grammar, not the separate strict scalar interface.

## 5.3-E7 — DESIGN+DERIVATION

**Prompt:** Explain why counting events is not the same as reconciling a cash balance.

Count is cardinality3 events, not USD units or a balance. Supplied amounts -1000+0+1040 yield nominal net40USD, but a cash balance additionally requires opening balance, account identity, complete settled movements, timing and reconciliation against an authoritative ledger/statement. The two same-day events retain separate identities; counting or netting does not prove completeness or settlement. No balance API/test is claimed.

## 5.3-E8 — DESIGN

**Prompt:** Identify additional fields required to distinguish planned and settled payments.

Retain obligation/event ID and account/counterparty scope, planned amount/currency/due date, explicit lifecycle status, actual settled amount/currency/timestamp with timezone, settlement/transaction reference and source, observed/revised-at provenance. Partial settlement/reversal may require separate linked settlement-event IDs and amounts rather than one boolean. Define finality, correction and calendar rules before interpreting status. These fields/policies are proposals, not implemented payment-state or accounting functionality.
