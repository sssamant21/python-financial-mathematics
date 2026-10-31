# Section 7.6 — Eight scoped local answers

These QA answers map the supplied prompts without changing the manuscript. Original source conversion, supplemental pandas/cast diagnostics and E4's separate vocabulary adapter are distinguished. E7/E8 policy proposals are not implementations or independent acceptance.

## 7.6-E1

**Prompt:** Add another leading-zero identifier and confirm its spelling survives conversion.

**Scope:** EXACT SOURCE

Append asset00007 with text count2,price12.50,reviewedfalse at a new unique source index10. The original converter preserves the literal string00007 and emits string/Int64/float64/boolean dtypes. Independent25/2 gives price12.5. Identity is not routed through a number.

## 7.6-E2

**Prompt:** Explain why empty lot_count is accepted but empty price is rejected.

**Scope:** EXACT SOURCE + FIELD POLICY

The empty lot_count token is explicitly approved unknown and becomes pd.NA in Int64; known zero on BETA stays0. Empty price raises ValueError because price completeness is required. Nullable storage permits missingness but does not authorize it for every field. No valuation or replacement of unknown counts by zero is performed.

## 7.6-E3

**Prompt:** Compare Int64 with int64 using one missing observation; inspect dtype and missingness.

**Scope:** PANDAS REPRESENTATION MECHANICS

pd.Series([1,pd.NA],dtype="Int64") has nullable integer dtype and mask[False,True]. Constructing ordinary int64 with [1,np.nan] raises a ValueError subtype; exact exception name/trace retained. Ordinary NumPy-backed int64 cannot store that NaN. An inferred float64 representation would be a different dtype,not evidence that int64 can hold missing integers.

## 7.6-E4

**Prompt:** Add a documented Boolean token vocabulary such as Y/N in a separate adapter, with explicit rejection tests.

**Scope:** SUPPLEMENTAL ADAPTER + ORIGINAL CONVERTER

yn_adapter.convert_yn requires the exact source schema and exact uppercase Y/N strings, maps them to original true/false tokens on a deep copy,then calls unchanged convert_records. Y,N,Y becomes True,False,True in boolean dtype; other typed fields match original output and source tokens stay unchanged. y,n,yes,true,empty,None and rawFalse reject; invalid price still rejects downstream. No automatic trimming,case folding or generic truthiness is used.

## 7.6-E5

**Prompt:** Audit ['10','BAD',None,'20'] using errors='coerce'; report newly introduced failures separately from all missing results.

**Scope:** SUPPLEMENTAL COERCION AUDIT

For ["10","BAD",None,"20"], errors="coerce" yields observed10,20 and missing positions1,2. introduced=raw.notna() & parsed.isna() is[False,True,False,False],so one new conversion failure versus two missing results overall. Retain BAD and source identity for investigation; the originally missing None is not another newly introduced parse failure. No incomplete financial total is accepted.

## 7.6-E6

**Prompt:** Explain why casting a truncated integer back to float cannot restore its source fraction.

**Scope:** CAST MECHANICS + RATIONAL ORACLE

The tested1.75 -> int64 -> float64 route yields1.0,not1.75. Exact source7/4 loses3/4 when cast to integer; the later float conversion can represent only the already-truncated1. Distinct fractional sources can collapse to the same integer,so the inverse cannot reconstruct the original value without retained source data. A cast is not a whole-count validator.

## 7.6-E7

**Prompt:** Propose a scaled-integer cents field with an explicit maximum and rounding policy; distinguish it from this approximate price field.

**Scope:** SCALED-CENTS POLICY DESIGN — NOT IMPLEMENTED

Propose a separate nonnegative USD cents field with scale100 and maximum1,000,000,000,000 cents ($10,000,000,000.00). Parse original decimal text exactly,never through float; reject missing/nonfinite/negative amounts. Specify round-half-even to two decimal places when higher precision is permitted,retaining original and rounded values; alternatively reject overprecision if exact cents are required. Under the proposed rounding policy1.005 becomes100cents and1.015 becomes102cents. Validate both pre-round admissibility and final scaled integer bounds; a rounded value beyond the maximum rejects. This is a proposed business policy,not a universal monetary rule. Distinguish a cents-per-unit price from a cash amount; fractional quantities/multipliers can require further rounding decisions. No scaled-money parser or arithmetic was implemented or tested.

## 7.6-E8

**Prompt:** Explain the extra checks needed before aggregating or multiplying nullable lot counts near their maximum range.

**Scope:** EXACT BOUNDARY + DOWNSTREAM ARITHMETIC DESIGN

The original converter preserves exact Int64 maximum2**63−1 and rejects maximum+1. The independent Python-int sum of that accepted count and1 exceeds the storage range; conversion success does not prove later sums/products safe. Before arithmetic,define missingness/completeness,nonnegative domains,target range and aggregation units; accumulate in checked wider/Python integers with explicit bound checks before casting,or reject projected range overflow. Count*price requires currency/quantity semantics and a separate precision policy. Never rely on nullable Int64 wrapping,skip-missing sums or a float conversion to enforce exact range. No general checked aggregation/multiplication API was implemented.

First-run command/predicate evidence and expected rejection traces retained. No unexpected QA failure or manuscript defect surfaced. The adapter imports the unchanged converter by its documented sibling name; the runner reconstructs source files and adapter together only in an owned temporary lab. The adapter is a vocabulary boundary,not a financial valuation implementation. E7's rounding examples are a proposed exact-decimal specification; they were not executed as a cents parser. F28/F32 and platform/input/numerical/independent acceptance limits remain open.
