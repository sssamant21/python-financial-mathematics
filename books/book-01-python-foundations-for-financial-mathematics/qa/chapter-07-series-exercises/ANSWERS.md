# Section 7.2 — Eight scoped local answers

The section supplies prompts, not a separate local companion. This QA supplement records answers and their evidence without changing the manuscript. E1–E7 use the original constructor or explicitly supplemental pandas construction/selection/copy mechanics. E8 is a metadata design review only.

## 7.2-E1

**Prompt:** Construct the fixture from a dictionary and compare its values, dtype, names, and index with the lab result.

**Scope:** SOURCE + SUPPLEMENTAL CONSTRUCTION

Construct pd.Series({"ALPHA":600.,"BETA":300.,"CASH":100.},name="opening_value",dtype="float64"). Values, asset order, dtype and Series name match the source constructor; its index name is initially None, whereas the source sets asset. Use rename_axis("asset") explicitly before comparing the full schema. The independent integer sum is1000 common-currency units. Dictionary insertion order is retained here; duplicates must be checked before collapsing source records into a mapping.

## 7.2-E2

**Prompt:** Reorder assets to CASH, ALPHA, BETA. Explain how `.iloc[0]` changes while `.loc['ALPHA']` retains its meaning.

**Scope:** SOURCE RESULT + SELECTION MECHANICS

Reindex to ["CASH","ALPHA","BETA"]. The first position changes from600 to100, while .loc["ALPHA"] stays600 because identity is unchanged. Reindex moves labels and their values together; do not independently reorder a value vector and retain old labels.

## 7.2-E3

**Prompt:** Select CASH and ALPHA in that order using `.loc` and explain why the result remains a Series.

**Scope:** SOURCE RESULT + SELECTION MECHANICS

s.loc[["CASH","ALPHA"]] produces a rank-one Series of shape(2,) with values100,600 in that order. A list of labels selects a labeled subset, retaining opening_value and asset names; it does not request a scalar cell as .loc["CASH"] would.

## 7.2-E4

**Prompt:** Compare `.loc['ALPHA':'BETA']` with `.iloc[0:1]` on the supplied index.

**Scope:** SOURCE RESULT + SLICE CONTRACT

On the supplied unique ordered index, .loc["ALPHA":"BETA"] includes both endpoint labels and yields ALPHA600,BETA300. .iloc[0:1] uses an exclusive positional stop and yields only ALPHA600. This is not a promise of alphabetical label sorting for arbitrary indexes.

## 7.2-E5

**Prompt:** Reindex to ALPHA and DELTA. Report size, count, the missing mask, and both sum policies.

**Scope:** SOURCE RESULT + MISSINGNESS MECHANICS

s.reindex(["ALPHA","DELTA"]) yields ALPHA600,DELTA NaN. size=2,count=1,missing mask[False,True]. Default sum is600 after skipping the unknown slot; sum(skipna=False) isNaN. The partial scalar600 does not establish a complete value for both expected assets, and unknown DELTA must not be silently treated as observed zero.

## 7.2-E6

**Prompt:** Attempt duplicate labels, negative values, and numeric strings through the validated constructor. Explain each rejection.

**Scope:** SOURCE REJECTION + DOMAIN REVIEW

Duplicate(ALPHA,ALPHA) with values600,300 raises ValueError because one financial key would have two values. ALPHA600/BETA−300 raises ValueError under the nonnegative opening-value contract. Text["600","300","100"] raises ValueError because parsing is upstream of this real numeric vector constructor. These are model/schema policies, not universal pandas restrictions; Boolean identity lost by prior numeric inference remains an upstream limit.

## 7.2-E7

**Prompt:** Change ALPHA in an explicit deep copy. Verify the original float64 Series remains unchanged.

**Scope:** SOURCE RESULT + COPY OWNERSHIP

other=s.copy(deep=True);other.loc["ALPHA"]=650 changes only the numeric copy. Original ALPHA stays600 and full original Series equality is retained. Copied dtype remainsfloat64 with opening_value/asset names. This guarantees the explicit numeric copy used here; it does not imply recursive copying of arbitrary nested object cells or universal slice ownership behavior.

## 7.2-E8

**Prompt:** Describe the units and valuation metadata required before summing another source's opening values with this Series.

**Scope:** CONCEPTUAL METADATA DESIGN — NOT EXECUTED INTEGRATION

Before summing another source, require compatible monetary units, reporting currency and explicit FX conversion/alignment if currencies differ; the same valuation instant/time zone/session and valuation basis; consistent quantity,price,multiplier and corporate-action conventions; stable asset/position identities and population grain; nonoverlap or an explicit consolidation/deduplication policy; source/batch provenance,coverage,availability and freshness controls; and an approved precision/range policy. Matching Series names,dtypes or labels alone cannot establish these facts. Different-date balances or mixed currencies cannot simply be added as one portfolio snapshot. This API carries no metadata validator and the proposal has not been integrated with external sources.

Original demonstration, eight-method discovery and compileall pass in the documented sibling layout. First-run evidence and expected rejection traces are retained. No unexpected QA failure or manuscript defect surfaced. Prepared runtime reuse is not fresh-install, Windows/macOS, notebook or external independent acceptance.
