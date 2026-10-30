# Chapter 4 project, checklist and extension review

These 45 derived review records are not 45 tests, workflows or new exercise prompts. Source behavior, new supplements and design-only work are distinguished per row.

## CONTRACT-01 — SOURCE

**long-only quantities**

Exact finite nonnegative Decimal units; fractional and zero accepted, no monetary arithmetic. Existing quantity tests plus explicit zero/fraction sequence.

## CONTRACT-02 — SOURCE

**schemas and identity**

Exact field sets, exact nonempty unpadded string scalars; catalog/holding uniqueness and known reference. Existing schema/duplicate/unknown tests; extension-1 missing quantity and padded/numeric probes.

## CONTRACT-03 — SOURCE

**full-input validation**

validated_inputs completes before any command or filter; unused invalid catalog and invalid later holding reject. Existing negative tests; supplemental lookup also rejects invalid later row.

## CONTRACT-04 — SOURCE

**add**

Known catalog ID absent from holdings; append one record. Sequence S1 independently checks B,A,C order and absolute quantity3.

## CONTRACT-05 — SOURCE

**replace**

Existing holding, absolute quantity (not delta), unchanged index; S2 B0,A20,C3. Equal replacement12.50 equals12.5 while new revision required.

## CONTRACT-06 — SOURCE

**remove**

Existing holding, quantity None; removes even stored zero; S3 A20,C3. Existing tests reject non-None quantity and absent targets.

## CONTRACT-07 — SOURCE

**report**

Fresh enriched rows, ID lexicographic order; active means strictly positive; A then B all, A active. Catalog order does not provide sort policy.

## CONTRACT-08 — SOURCE

**ownership**

Validation creates canonical pairs, commands reconstruct every holding dictionary, reports reconstruct enriched rows. Existing ownership test and independent before/after sequence checks preserve catalog and S0.

## CONTRACT-09 — SOURCE

**revision**

Portfolio ID unchanged; immediate parent label must differ. Historical S0 reuse from S1 and two competing S1 successors are allowed and executed as limitations, not defects.

## CONTRACT-10 — SOURCE

**empty**

Wrapper retains identity with empty holdings; existing empty/remove-last test and supplemental empty membership check.

## CONTRACT-11 — SOURCE

**errors**

TypeError for unsupported scalar/container types; ValueError for schema/domain/reference/identity. Invalid commands never return a partial successor; duplicate-add failure preserves S1.

## CONTRACT-12 — SOURCE

**scope**

No database/network/cache/trades/valuation/FX/global audit history. Structure choices establish supplied-data consistency only; code inspection, not external operations or certification.

## STEP-01 — SOURCE

**Prerequisites and save**

Use standard-library Python3.10+ syntax; executed only CPython3.12.14 Linux. Extract entire first Python block to portfolio_holdings_manager.py. No pip dependency needed.

## STEP-02 — SOURCE

**Run tests**

Exact first block executed directly in isolated temp directory; return0, Ran10tests and OK retained. Subtests are not additional unique methods.

## STEP-03 — SOURCE

**Save and run demo**

Exact second block beside module; original imports work; return0 and exact PASS message. Assertions check active A12.5,C3 plus preserved baseline.

## STEP-04 — SOURCE

**Duplicate add boundary**

Run an explicit duplicate SEC-A add against S1, expect ValueError, inspect unchanged S1; no catch-all/empty fallback.

## STEP-05 — SOURCE

**Import behavior**

Import project module in clean child interpreter; return0 and no stdout/stderr. No runner executes during import.

## STEP-06 — SOURCE

**Inspect sequence and boundary**

Explicit S0/S1/S2/S3 literals check order, units and immediate revision; inspect fresh containers and documented no-global-history behavior.

## ACCEPT-01 — SOURCE

**Exact schema and valid scalar values**

existing schema/quantity tests; extension-1; instructional acceptance evidence only.

## ACCEPT-02 — SOURCE

**Catalog and holding uniqueness**

existing duplicate tests; instructional acceptance evidence only.

## ACCEPT-03 — SOURCE

**Known references including zero holdings**

existing unknown-zero test; instructional acceptance evidence only.

## ACCEPT-04 — SOURCE

**Distinct command semantics**

independent sequence literals and failed duplicate add; instructional acceptance evidence only.

## ACCEPT-05 — SOURCE

**New immediate revision label**

equal-value and reused-parent probes; instructional acceptance evidence only.

## ACCEPT-06 — SOURCE

**Deterministic ID report order**

existing independently stated exact report; all-order probe; instructional acceptance evidence only.

## ACCEPT-07 — SOURCE

**Active filtering preserves stored zero**

source all/active tests; S0 literal still B0; instructional acceptance evidence only.

## ACCEPT-08 — SOURCE

**Empty portfolio remains identifiable**

existing empty/remove-last; empty membership; instructional acceptance evidence only.

## ACCEPT-09 — SOURCE

**Baseline and catalog remain unchanged**

source ownership tests and saved baseline comparison; instructional acceptance evidence only.

## ACCEPT-10 — SOURCE

**End-to-end use**

exact demo command/assertions; instructional acceptance evidence only.

## EXT-01 — SOURCE

**Reject padded command IDs, numeric revision IDs, missing quantity**

Three command invalid-scalar probes and missing-quantity report test reject with declared errors. Source code unchanged.

## EXT-02 — SUPPLEMENT

**Fresh holding lookup**

New lookup validates whole dataset before target search, returns new ID/quantity dictionary, rejects absent target. Zero and alias isolation plus invalid later row executed.

## EXT-03 — SUPPLEMENT

**All-ID membership**

New parent-identified membership report returns frozenset of all validated holding IDs including zero; empty retains P/E identity.

## EXT-04 — SUPPLEMENT

**Multi-portfolio wrapper**

New multi returns owned reports keyed (portfolio_id,snapshot_id); rejects duplicate wrapper keys. Same SEC-A in PORT-01 and P2 remains two records. Tests edit one report without affecting another.

## EXT-05 — DESIGN

**Tax-lot identity**

Proposed key=(portfolio_id,snapshot_id,lot_id), separate security reference, acquisition date, quantity, cost amount/currency and accounting selection policy. Same security can occur in several distinct lots; duplicate lot identity rejected before indexing. No lot engine or tax accounting implemented.

## EXT-06 — SUPPLEMENT

**Catalog version and observation basis**

New metadata_report retains caller-supplied exact nonempty unpadded labels and owned report. Labels do not prove catalog hashes or simultaneous observations; underlying quantities unchanged.

## EXT-07 — DESIGN

**Specify atomic command batch**

Policy: one parent and one distinct successor label for whole batch; commands have no intermediate public revision labels. Validate catalog/parent and every command schema first, then simulate sequential preconditions privately (add can make later replace valid), reject whole batch on any failure. Return one successor after all pass; do not require each operation to be valid independently on original parent. Empty batch policy must be declared (propose reject). No batch executor is claimed.

## EXT-08 — DESIGN

**Persistence and concurrent revisions**

Persist immutable snapshots with globally unique revision IDs and parent pointer; compare expected parent under database transaction/conditional write, atomically store successor plus audit metadata. Conflicts reject/retry on fresh input; idempotency key prevents duplicate commands. Function copying provides none of this. No persistence/concurrency test performed.

## EXT-09 — SUPPLEMENT

**Supplied prices after explicit policy**

New supplied_prices accepts exact records: security_id,price,currency,quote_unit,observed_at,source_id. Positive exact finite Decimal, per_instrument_unit only; explicit datetime with timezone.utc only; matching catalog quote currency; unique(security_id,observed_at). Reconstruct rows, preserve input order; no FX, total, quantization or price arithmetic, so no arithmetic-context result asserted. Empty allowed but does not imply priced coverage. Future valuation must choose as-of/staleness/completeness, FX and rounding rules; unsupported per100 quotes are rejected. Tests cover owned rows, empty, duplicates, invalid currency/unit/time/amount/reference.

## DESIGN-4.12-1 — DESIGN

**Authoritative input**

Caller-retained portfolio snapshot plus supplied catalog; derived views are disposable.

## DESIGN-4.12-2 — DESIGN

**Record identity and scope**

One security_id per supplied catalog and per portfolio snapshot; portfolio_id and snapshot_id identify parent.

## DESIGN-4.12-3 — DESIGN

**Valid repetitions**

Different portfolios may share a security; within this aggregate snapshot duplicate security IDs are errors. Lots need separate schema.

## DESIGN-4.12-4 — DESIGN

**Ordering**

Holdings preserve source/command order; report sorts case-sensitive security IDs; membership has no presentation order.

## DESIGN-4.12-5 — DESIGN

**Discarded fields/distinctions**

Snapshot pair omits metadata; lookup loses duplicate multiplicity unless validated first; membership discards quantity and order. Do not confuse zero with absent.

## DESIGN-4.12-6 — DESIGN

**Mutable ownership**

Input dictionaries/lists and wrapper/lookup/report dictionaries remain mutable; immutable scalar snapshots share only supported immutable values. Return fresh mutable records.

## DESIGN-4.12-7 — DESIGN

**Rebuild policy**

Treat corrected authoritative input as a new version; build all views before publishing one versioned wrapper. No automatic cache refresh/concurrent swap is implemented.

## DESIGN-4.12-8 — DESIGN

**Empty/zero/missing/invalid**

Empty holdings valid with parent identity; zero valid stored/member but inactive; missing quantity/reference is error, unsupported types/nonfinite/negative rejected. No default-zero repair.
