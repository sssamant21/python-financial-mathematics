# Section5.1 — eight local exercises

SOURCE executes original functions/listings; SUPPLEMENT adds a caller/observer; EXPECTED_MUTATION deliberately breaks and restores a temporary copy; DESIGN is reasoning only.

## 5.1-E1 — SUPPLEMENT+SOURCE

**Prompt:** Add a second runner using the same core and different synthetic quantities. Verify neither runner changes the core or the other's inputs.

New second_runner uses Q0,Z2.5,Y4 and prints Z,Y through the same original core. Original runner still prints A,C from B0,A12.5,C3. Supplemental observer wraps active_ids only to compare each caller input before/after while delegating to unchanged original function, then restores binding. Core and both original files compared by hash after all experiments; no implementation copied.

## 5.1-E2 — SOURCE

**Prompt:** Add a test rejecting a numeric security ID and another rejecting an extra record field.

Numeric security_id1 raises TypeError; extra record field raises ValueError. Both rows remain equal to their before snapshots. These two new source-function assertions extend existing original rejection coverage without adding original unittest methods.

## 5.1-E3 — EXPECTED_MUTATION+RESTORE

**Prompt:** Move a print call outside main temporarily. Observe which fresh-import test detects the change, then restore the guard-based design.

In a temporary extracted runner remove the print from main and put the same visible message at top level. Existing ModuleTests.test_fresh_import_is_quiet fails with one assertion/nonzero exit, identifying startup output. Restore exact original file; full eight-method suite passes. Baseline pass, raw failure, mutant source/hash and restored pass retained. This was deliberate exercise fault injection, not a source defect.

## 5.1-E4 — SOURCE+REVIEW

**Prompt:** Explain why the guard does not prevent top-level imports and definitions from running.

The guard tests __name__ only at its conditional call site. Imports and def statements above it still execute and bind Decimal,main and core functions; function bodies/app data/display wait for explicit calls. Fresh import checks callable bindings and no output, not a universal side-effect sandbox.

## 5.1-E5 — SOURCE

**Prompt:** Add a test checking the active-ID order for a reversed valid source list.

Reverse valid B0,A12.5,C3 source→C3,A12.5,B0, then strictly-positive filter yields (SEC-C,SEC-A). Original source order/values remain unchanged. Do not sort IDs or truth-test away stored zero before validation.

## 5.1-E6 — SOURCE_EXPERIMENT

**Prompt:** Describe what happens when you edit holdings_core.py in a running interactive session and import it again normally.

One child imports core, edits only its own temporary core file to append EDIT_VISIBLE=True, imports normally again and confirms same cached module without new attribute. A fresh interpreter sees new saved attribute. Finally restores bytes. Actual notebook/editor restart procedure is not executed; experiment establishes the normal same-name import-cache behavior.

## 5.1-E7 — DESIGN

**Prompt:** Explain why copying core definitions into each runner creates a maintenance problem.

Copies of validation across runners drift: fixing a duplicate-ID or finite-quantity rule in one copy leaves another stale, with unclear ownership/version and duplicated regression work. Put one authoritative implementation in core and call its API from both runners; compatibility tests cover public behavior, not a guarantee against every future drift.

## 5.1-E8 — DESIGN

**Prompt:** Identify what additional metadata is needed before these holdings can support a reproducible valuation.

Before valuation retain portfolio/snapshot identity, security master/version, quantity units and lot/aggregate scope, dated/source-identified prices with quote units/currencies, valuation as-of/timezone and FX basis, missing/stale/revision policy, model/code/dependency versions, numeric precision/rounding and observed input provenance. Positive units or reproducible imports do not establish completeness, price accuracy, settlement or value. No valuation implementation claimed.
