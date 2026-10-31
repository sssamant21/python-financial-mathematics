# Section 7.11 — Eight scoped local answers

Unchanged original aggregation is distinguished from supplemental groupby/transform mechanics. Independent rational arithmetic checks the original and added-cash fixtures. E7 account reporting and E8 independently expected population controls remain designs,not a multi-account implementation or external acceptance. Full demonstration expectations are transcribed from the published table/formulas and compared after whitespace normalization.

## 7.11-E1

**Prompt:** Reproduce equity's 2.50% simple mean, 5.00% weighted return and 4.50% portfolio contribution by hand.

**Scope:** SOURCE + RATIONAL DERIVATION

Equity simple mean=(1/10−1/20)/2=1/40=2.50%. P&L600/10−300/20=45 and opening value900 give weighted sector return45/900=1/20=5.00%. Contribution to portfolio uses denominator1000,so45/1000=9/200=4.50percentage points. These have different weights/denominators;sector returns must not simply be summed as portfolio return.

## 7.11-E2

**Prompt:** Reverse source ordering and verify report keys and results remain consistent for the fixture.

**Scope:** EXACT SOURCE ORDERING

Reverse the source rows and call summarize again. For the controlled fixture,the full keyed report and portfolio return remain equal,with sorted sector keys cash,equity,unused. This confirms identity preservation for this case,not universal bitwise invariance for arbitrary floating-point reduction orders.

## 7.11-E3

**Prompt:** Add another invested cash asset and reconcile group counts, values and contributions.

**Scope:** EXACT SOURCE + RATIONAL ADDED-CASH ORACLE

Append CASH2 in sectorcash with opening200 and common-interval return0.02. New cash opening300,P&L4,count2;equity remains900/P&L45/count2;unused count1 haszeroexposure. Five records reconcile to opening1200 and P&L49. Cash ownreturn4/300=1/75,portfolio contribution4/1200=1/300;equity contribution45/1200=3/80. Contributions sum49/1200≈4.08333%. Inputs share the original no-flows/common-currency/common-interval assumptions.

## 7.11-E4

**Prompt:** Replace one sector with a missing value; contrast general pandas behavior with the public function's rejection.

**Scope:** SOURCE REJECTION + GENERAL GROUPBY CONTRAST

Set ALPHA sector toNone. General default groupby drops that missing-key row,retaining3records and opening exposure400;dropna=False retains4records including the unknown-classification group. The public function raises ValueError for incomplete sector text before aggregation. Missing grouping keys must not silently erase600 of opening exposure from a complete-portfolio claim.

## 7.11-E5

**Prompt:** Add a zero-valued observed sector and explain its undefined return.

**Scope:** EXACT SOURCE ZERO-DENOMINATOR POLICY

Append assetZERO2 in new observed sectorotherzero with opening0 and observed return0.1. Report retains its count1,opening0,P&L0,contribution0 and ownsectorreturnNaN because the own-return denominator is0. Portfolio return remains0.045. This is an observed zero-exposure sector,not an unused categorical level or missing source return.

## 7.11-E6

**Prompt:** Use transform to attach sector opening totals to rows, then explain why summing those repeated totals is wrong.

**Scope:** SUPPLEMENTAL TRANSFORM MECHANICS

raw.groupby("sector")["opening_value"].transform("sum") returns[900,900,100,0] aligned to asset rows. Equity total900 is repeated for two assets,so summing the vector gives1900 rather than the true grouped opening1000. Use one summary row per sector for reconciliation;transform supports row-level comparisons,not an independently additive sector table.

## 7.11-E7

**Prompt:** Design account-and-sector keys for separate account reports; state which denominator each contribution should use.

**Scope:** ACCOUNT/SECTOR DESIGN — NOT IMPLEMENTED

For separate account reports define source grain(account_id,asset_or_position_id,valuation_snapshot),with each position mapped to one sector under a documented classification version. Group by(account_id,sector) within compatible currency/time/return conventions. Divide sector P&L by that account total opening value for contribution to the account,not by the consolidated portfolio;own-sector return divides by that account-sector opening value. Preserve zero-denominator/missingness policy per account and reconcile each account before any explicitly authorized consolidation. Do not silently deduplicate the same instrument held in different accounts. No multi-account API or denominator implementation was added.

## 7.11-E8

**Prompt:** Explain why complete observed groups still require an independently expected asset population before claiming portfolio completeness.

**Scope:** SOURCE COVERAGE LIMIT + EXTERNAL CONTROL DESIGN

Complete observed numeric groups establish only internal record/count/value reconciliation. Omitting BETA entirely still passes current source validation and returns3records,opening700,priceP&L60 and return60/700=3/35. Detecting that omission needs an independently maintained expected asset/position population,valuation context and source control totals. Compare missing/extra keys and unresolved classifications before claiming full portfolio completeness;do not derive expected assets from observed group output. No independent source-universe integration was implemented or accepted.

Original source demonstration,discovery and compileall pass with FutureWarning as error. No unexpected QA failure or manuscript defect surfaced;first-run outputs and expected rejection traces retained. No historical unique methods or earlier workflow cases added by overlapping reruns. F28/F32,F37 history and platform/input/numerical/independent acceptance limits remain intact.
