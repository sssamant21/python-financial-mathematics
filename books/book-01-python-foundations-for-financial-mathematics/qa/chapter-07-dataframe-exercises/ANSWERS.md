# Section 7.3 — Eight scoped local answers

These QA answers correspond to the original local prompts; they do not alter the manuscript or imply an absent-companion defect. E1–E7 use unchanged source calls and explicit supplemental pandas selection/assignment mechanics. E8 is a proposed valuation design, not implemented integration.

## 7.3-E1

**Prompt:** Select price once as a Series and once as a DataFrame; report both shapes.

**Scope:** SOURCE RESULT + DIMENSION MECHANICS

table["price"] selects a Series of shape(3,) and ndim1. table[["price"]] selects a DataFrame of shape(3,1) and ndim2. Both contain the same asset prices; the list selector preserves the field axis for callers requiring a table. No rank assumption should be inferred solely from one displayed column.

## 7.3-E2

**Prompt:** Reverse the asset row order and confirm the total is unchanged while labels remain correct.

**Scope:** SOURCE + RATIONAL ORACLE

Pass fixture().iloc[::-1] into the original holdings_table. Output rows are CASH,BETA,ALPHA with market values100,300,600. Input row ordering is retained while asset/value pairings remain correct. Independent integer arithmetic1*100+3*100+6*100=1000 gives the unchanged total; this fixture does not establish universal bitwise invariance for every floating reduction.

## 7.3-E3

**Prompt:** Reverse input column order and inspect the function's fixed output order.

**Scope:** SOURCE SCHEMA CONTRACT

Select source columns in order price,quantity. The API accepts the exact unique field set in either order and constructs output order quantity,price,market_value. Output values and total equal the original report; changing field order does not change field identity. Missing,extra or duplicate fields still reject.

## 7.3-E4

**Prompt:** Add a derived field named price_times_two to a separate report. State its units and explain why it is not another holding value.

**Scope:** SUPPLEMENTAL DERIVED FIELD + UNITS REVIEW

Use a separate table.assign(price_times_two=table["price"]*2). The fixture gives200 for each asset while leaving the original report unchanged. The factor2 is dimensionless, so this field remains currency per asset unit; it is not quantity*price and is not another holding value. It is not an FX conversion unless a separate documented conversion contract supplies that meaning. Summing it into market value would mix dimensions.

## 7.3-E5

**Prompt:** Assign a Series lacking BETA to a copied table; inspect the resulting missing cell without silently filling it.

**Scope:** SUPPLEMENTAL ASSIGNMENT + SOURCE OWNERSHIP

Copy the report and assign external_price=pd.Series([1.,101.],index=["CASH","ALPHA"]). ALPHA receives101,CASH1,BETA NaN. The missing mask isFalse,True,False and count2. pandas aligns by key but does not certify full coverage; retain the unknown BETA cell and original source/report without silently filling. This is an inspection table, not a validated replacement price feed.

## 7.3-E6

**Prompt:** Reject a duplicate asset, a duplicate column, and an unexpected currency column through the validated function.

**Scope:** SOURCE REJECTION + IDENTITY/SCHEMA REVIEW

An ALPHA,ALPHA,CASH asset index rejects because each asset must be unique. Duplicate quantity columns reject because a field would be ambiguous and the schema would not have exactly one quantity and one price. Adding currency="USD" also rejects: even a plausible extra field violates this intentionally narrow API. The wider workflow must validate common currency before stripping/transforming metadata; this component performs no FX conversion.

## 7.3-E7

**Prompt:** Change ALPHA's quantity in a returned report. Demonstrate that market_value becomes stale, then recompute using only the two source columns.

**Scope:** SOURCE + STALE-DERIVATION PROBE

In a separate returned report, set ALPHA quantity from6 to7. Stored market_value remains600 and its summed total remains1000, demonstrating a stale derived field. Passing the whole report rejects its extra market_value field. Call holdings_table(changed.loc[:,["quantity","price"]]) to recompute ALPHA700 and total1100 independently from7*100+3*100+1*100. The source fixture still has quantity6 and the edited intermediate report stays stale until explicitly replaced; derived columns are not spreadsheet formulas.

## 7.3-E8

**Prompt:** Explain what would need to change before valuing holdings with different currencies, contract multipliers, or valuation timestamps.

**Scope:** CONCEPTUAL VALUATION DESIGN — NOT EXECUTED INTEGRATION

Define an expanded schema and financial contract before accepting heterogeneous sources. Carry instrument/position identity,currency,quantity units,price units,contract multiplier and valuation/availability timestamps; validate compatible q*price*multiplier dimensions,then convert to a reporting currency using independently sourced FX with explicit direction,rate date/age,alignment and missingness policy. Establish a common valuation instant or an explicit as-of policy with quote-age and decision-time constraints. Reconcile coverage,avoid duplicate positions,select appropriate exact/approximate arithmetic and add unit/context/boundary/rejection tests before implementation. Do not merely append fields and remove them to satisfy this API. No multi-currency,multiplier or temporal matching implementation was validated here.

The original demonstration,eight-method discovery and compileall pass in the documented parent/sibling layout with FutureWarning as error. First-run outputs,source hashes and expected rejection traces are retained. No unexpected QA failure or manuscript defect surfaced. Float64 roundoff/underflow,upstream lost-type information,context completeness,platform and independent acceptance remain outside these scoped results.
