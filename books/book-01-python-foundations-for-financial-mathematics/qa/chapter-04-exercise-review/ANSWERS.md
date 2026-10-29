# Chapter4 —20 chapter-wide answer reviews

Reviewed2026-10-29. Conceptual/model-design reasoning is distinct from runtime predicates. Source implementations are used unchanged; no supplemental valuation or lot aggregation is inferred.

## Exercise1 — Select a Representation

List of identified event records preserves repeated dates; dictionary keyed by unique security ID supports catalog lookup; frozenset of exact labels supports immutable membership; tuple of validated scalar pairs captures an immutable holdings baseline. None establishes completeness, prices or financial valuation.

## Exercise2 — Mutation and Rebinding

original and other first alias the same list/dictionary. Mutation through other sets the shared quantity to2; rebinding other=[] leaves original with its changed record. The executed ownership demonstration matches those states.

## Exercise3 — Tuple Descendants

A tuple can contain a mutable dictionary; changing its descendant is allowed. A tuple of (exact string ID, exact finite Decimal quantity) pairs has no mutable supported descendants. Validation must enforce the shape; annotations alone cannot freeze a list.

## Exercise4 — Duplicate-Key Loss

A/1,A/2,B/0 becomes {A:2,B:0} by last-key overwrite, and ID membership {A,B}. The first quantity, multiplicity and order information are lost; no lot quantities are summed or tax-lot identity retained.

## Exercise5 — Missing, Zero, and Empty

Zero quantity is a known valid position, missing quantity violates schema, empty holdings is valid but says nothing about completeness. Portfolio/snapshot identity belongs to the surrounding wrapper even when holdings is empty.

## Exercise6 — Identity Scope

Aggregate position key: (portfolio_id,security_id). Lots need a separately declared unique key such as (portfolio_id,account_id,lot_id), retaining security_id as a reference. Payment date alone cannot identify two same-day events.

## Exercise7 — Immutable Capture

Exact source capture validates all rows, IDs, quantities and duplicates before returning ordered immutable pairs. Fixture starts SEC-B/0 then SEC-A/12.5,SEC-C/3. Empty gives(); duplicate and invalid later rows reject. Retained scalar tuples do not change after source dictionaries change.

## Exercise8 — Active Records

active_rows validates through complete capture then selects positive quantities in source order: SEC-A then SEC-C. Empty gives[]. Fresh returned dictionaries are independently mutable. Invalid final rows still reject, even when they would not be selected.

## Exercise9 — Lookup View

quantity_lookup includes all validated IDs, including SEC-B Decimal0. Empty gives{}. Editing it cannot update a retained capture or source. Duplicate IDs reject rather than silently overwrite.

## Exercise10 — Deterministic ID Report

id_report returns fresh records sorted SEC-A,SEC-B,SEC-C. Reversing input changes captured source order but not the sorted report. Empty gives[]; invalid/duplicate later records reject before sorting.

## Exercise11 — Membership Reconciliation

compare_ids validates exact unpadded strings, allows repeats, compares membership and sorts differences. [A,B,B] versus[B,C] gives missing[A],unexpected[C]. It does not verify quantities, record multiplicity or lot identity; existing reference tests include empty and wrong inputs.

## Exercise12 — Inclusive Subset

at_least validates an exact finite nonnegative Decimal threshold and all holdings, then applies>=. Threshold3 selects SEC-A/12.5 and SEC-C/3; zero retains all;13 selects none. Fresh records preserve ownership. Cross-instrument quantity comparison needs caller justification and is not economic exposure ranking.

## Exercise13 — Preserve Same-Day Events

group_events validates unique event IDs across all dates, exact date excluding datetime, and exact finite signed Decimal amounts. It groups into date-ascending/event-ID-ascending lists without collapsing same-day events. Independent fixtures preserve negative and zero amounts; empty returns{}; duplicate IDs across dates and datetime reject. Output event dictionaries are fresh.

## Exercise14 — Calendar and Model Time

Ordinal period1 needs a unit/origin; date lacks intraday settlement time;30-day increments do not implement contractual calendar months. Discounting additionally needs valuation/payment basis, currency/sign perspective, day-count/year fractions, rate curve and compounding conventions, and source/calendar versions. No discounting is implemented here.

## Exercise15 — Do Not Hide Unknown Data

Replacing missing with0 changes unknown into known; one amount per date overwrites event multiplicity independently. Retain identified records or date-to-event-list views; reject missing required fields or quarantine with explicit reasons, preserving source identity. Any derived net view must retain audit lineage.

## Exercise16 — Independent Views

views returns immutable ordered snapshot, fresh lookup and immutable membership. Source and lookup edits do not change retained snapshot/membership. Rebuild all three from the corrected source and associate them with its new snapshot identity rather than mixing versions.

## Exercise17 — Extend the Manager with Lookup

find_holding validates the whole catalog and portfolio, then the requested text. It returns a fresh record including stored zero; catalog-known but unheld or unknown IDs raise ValueError. An independently injected unused invalid catalog row rejects before an otherwise valid lookup can return.

## Exercise18 — Scenario Sequence

Exact project operations add SEC-C/3 atS1, replace SEC-A absolutely with20 atS2, then remove SEC-B atS3. Final source/report ID order SEC-A,SEC-C, quantities20/3. S0 stays SEC-B/0 then SEC-A/12.5. Replace is assignment of absolute position, not trade-delta arithmetic.

## Exercise19 — Rejection Matrix

Exact companion test_19_rejection_matrix exercises duplicate add, unheld replace, repeated immediate label, bool quantity, invalid unused catalog currency and hidden unknown zero holdings. Each expected exception preserves the tested baseline. The combined suite passes; local immediate-label rejection does not ensure global uniqueness or concurrent transaction safety.

## Exercise20 — Design Review

Production extension review: define account/tax-lot identity and quantity/price/multiplier/FX units; bind observation/catalog versions; reject or quarantine unresolved references with reasons; preserve owned source snapshots. Persist global revision uniqueness and optimistic concurrency checks, atomic commit semantics and durable history/access/backup recovery. Reproduction needs source/code/model/policy versions and numeric context. Passing synthetic local tests establishes selected representation/ownership contracts, not production accounting, valuation completeness or live concurrency reliability.

