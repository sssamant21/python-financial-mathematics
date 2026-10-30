# Sections4.4–4.6 —27 exercise review records

Reviewed2026-10-29. Exact-source calls, teaching object probes and proposed financial/schema contracts remain distinct.

## 4.4-E1

key in mapping checks keys; value in mapping.values() checks values. The fixture distinguishes a payment_id key from its VALUE contents; key membership does not inspect record fields recursively.

## 4.4-E2

A missing mandatory amount raises KeyError through direct lookup. get returns None by default; supplying0 would silently replace unknown with a known amount. Validate required schema before calculation rather than treating get as validation.

## 4.4-E3

Changing a currency label changes metadata only. Conversion requires an authorized FX convention/rate/source/as-of time and an actual numerical calculation with declared rounding. Do not relabel the unchanged amount as a converted value.

## 4.4-E4

Check duplicate payment IDs before dictionary assignment; otherwise the later row silently overwrites the earlier one. Exact source index_payments rejects identical duplicate records with ValueError and preserves input.

## 4.4-E5

Exact case-sensitive source policy accepts P001 and p001 as distinct identifiers. Both amounts remain100; no normalization is applied. Case-distinct does not prove distinct real-world payments without a documented source identity policy.

## 4.4-E6

Proposed key:(source_system,payment_id), or include account/dataset scope where required by upstream uniqueness. Define correction revision separately. This is not silently added to the strict compact source schema.

## 4.4-E7

A mutable notes list invalidates the current immutable-scalar copy rationale. A shallow dictionary copy aliases that list; reconstruct validated descendants or define deliberate sharing. The probe demonstrates shared mutation.

## 4.4-E8

Deleting B from A,B,C then reinserting B produces key order A,C,B. Dictionary order reflects current insertion history, not a payment timeline or sorting criterion.

## 4.4-E9

Proposed corrections are append-only revisioned events with original identity, supersedes/reference, reason and effective/source timestamps. Validate uniqueness and active-version selection explicitly. Keep the current duplicate-rejection contract unchanged; global revision and transaction enforcement need separate implementation.

## 4.5-E1

{} creates a dictionary; set() creates an empty set. A set literal needs members such as {A}; empty braces do not mean empty membership.

## 4.5-E2

Expected{A,B,C},received{B,C,D}: missing=expected−received={A};unexpected=received−expected={D};matched={B,C};duplicate_received is empty. Direction matters.

## 4.5-E3

Expected[A],received[B,B] reports missing{A},unexpected{B},matched{},duplicate_received{B}. Duplicates are evidence of repeated received IDs, not excess-occurrence counts or monetary reconciliation.

## 4.5-E4

remove(X) raises KeyError when absent; discard(X) returns None without changing the set. Neither chooses a financial missing-event policy automatically.

## 4.5-E5

Converting equal transactions/amounts to a set collapses repeated equal values that may be legitimate separate payments. Preserve identified records and multiplicity first; value equality alone is not event identity.

## 4.5-E6

Use(source_system,payment_id) as a proposed minimum compound identity when systems reuse IDs; add account/source-version scope if upstream rules require it. Normalize only under an explicit reviewed policy.

## 4.5-E7

Checks exercise expected=missing∪matched and received_membership=unexpected∪matched, with both partition pairs disjoint, across empty/mixed/duplicate/all-matched fixtures. Inputs remain unchanged. duplicate_received is separate from these membership partitions.

## 4.5-E8

Alphabetic sorted output supplies deterministic presentation, not recovered arrival/payment order. Preserve source sequence or timestamps/event ordinals if a timeline matters.

## 4.5-E9

After IDs match, verify amounts/signs, currencies/scales, observation/source versions, effective dates, settlement/status, duplicate/correction treatment, fees and any FX/rounding/tolerance policy. ID equality alone cannot certify payment reconciliation.

## 4.6-E1

Proposed field table: portfolio(portfolio_id,report_currency,accounts:list); account(account_id,positions:list); position(position_id,instrument_id,quantity,quantity_unit). Specify types, required fields, uniqueness scopes, ordering and ownership at each level before access. This expanded account hierarchy is a design, not the current simpler portfolio schema.

## 4.6-E2

Missing positions violates required schema; explicitly empty positions is valid and source flatten returns[]. Do not infer completeness or unknown data from emptiness. The executed fixtures distinguish both behaviors.

## 4.6-E3

The source rejects a later position lacking instrument_id with ValueError. A valid earlier position cannot justify partial output. The untouched valid baseline is checked separately.

## 4.6-E4

dict(portfolio) copies the outer mapping but retains the same positions list and dictionaries; append through the copy is visible in the original. Copy depth must follow the declared ownership contract.

## 4.6-E5

[position]*3 repeats the same dictionary reference. Mutating one entry changes all three visible aliases; construct/reconstruct independent dictionaries if separate positions are intended.

## 4.6-E6

Proposed lot key:(portfolio_id,account_id,lot_id), retaining instrument_id as a reference and stating lot-ID uniqueness/version policy. Permit repeated instruments only under that new lot model; the current aggregate-position duplicate rule stays unchanged.

## 4.6-E7

Current flatten_portfolio([] positions) returns no rows and therefore loses parent identity in the flat list. A supplemental wrapper retains portfolio_id,currency,rows=[]; retain original wrapper/metadata rather than inventing a sentinel holding.

## 4.6-E8

Before adding tags, specify list-of-validated-text shape, ordering/duplicates, mutation owner, copy/reconstruction policy and failure rules. Do not accept arbitrary mutable descendants or weaken the current exact-field schema silently. An immutable tuple may suit captured tags if its scalar policy is validated.

## 4.6-E9

Market value needs instrument quantity units, price unit and quote currency, contract multiplier where relevant, price source/as-of time, catalog/security version, valuation date, FX basis if combining currencies, and declared arithmetic/rounding rules. Quantities alone are not comparable economic exposure.

