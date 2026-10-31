# Section 7.12 — Eight scoped local answers

Exact original one-to-one reconciliation is separate from supplemental pandas cardinality/left-join mechanics. Independent scalar arithmetic checks complete valuation and the two-by-two multiplication example. Multi-account grain,intraday alignment and provenance-column extensions remain designs;no replacement financial API or independent source acceptance is claimed.

## 7.12-E1

**Prompt:** Remove CASH from quotes and inspect its outer indicator and missing fields.

**Scope:** EXACT SOURCE

Removing CASH from quotes retains its outer-audit row as left_only with quantity1 and missingprice. The function returns resultNone,totalNone,not the plausible matched subtotal900. Other holdings remain visible for reconciliation;missing quote is not a zero price.

## 7.12-E2

**Prompt:** Add an extra quote and explain how this lab differs from an intentional broad-reference left-join workflow.

**Scope:** SOURCE + LEFT-JOIN CONTRAST

Append an OTHER quote. Strict exact-population reconciliation exposes right_only OTHER and withholds valuation. A separate mechanical left join retains only the three holdings,allmatched,to illustrate a different policy where a reference quote universe may be intentionally broader. That policy would still require full holdings coverage,unique appropriate quote keys and context/observation checks;the source API was not changed.

## 7.12-E3

**Prompt:** Duplicate a quote key and demonstrate one_to_one rejection.

**Scope:** SOURCE + PANDAS CARDINALITY

Duplicate ALPHA quote key. Original source validation raises ValueError before merging;separately,h.merge(...,on=KEY,how="outer",validate="one_to_one") raises pandas MergeError. Duplicate keys are not resolved by picking first/last or averaging without an explicit source-backed policy. Both expected traces are retained.

## 7.12-E4

**Prompt:** Reproduce the two-by-two key multiplication example and explain its effect on exposure totals.

**Scope:** SUPPLEMENTAL MULTIPLICATION + SCALAR ORACLE

Two A holdings quantities1,2 and two A quotes10,11 create four pairs(1,10),(1,11),(2,10),(2,11). Joined quantities sum6 rather than original3;candidate-pair values sum10+11+20+22=63. Neither quote is established as authoritative;using one unique quote10 would instead give30,and quote11 would give33. Summing all candidates duplicates exposure rather than resolving ambiguity.

## 7.12-E5

**Prompt:** Reverse source ordering and verify the normalized valuation is unchanged.

**Scope:** EXACT SOURCE + KEYED ORACLE

Reverse both source row orders. Original normalized outer audits and valuation tables remain equal,with total6*100+3*100+1*100=1000 and asset values600,300,100. Both numeric sources are unchanged when returned output is edited. This verifies the controlled fixture,not all floating reduction scales.

## 7.12-E6

**Prompt:** Propose a many_to_one contract for multiple accounts sharing one quote per instrument/date/currency.

**Scope:** MECHANICS + MULTI-ACCOUNT DESIGN

A mechanical many_to_one merge of two A holdings with one A quote preserves two rows and quantitysum3. For real accounts,define unique left keys(account_id,position_or_asset_id,currency,valuation_snapshot) and unique right quote keys(asset_id,currency,valuation_snapshot,approved price convention),then merge on explicitly compatible quote keys with validate="many_to_one". Preserve account/position identities,inspect missing matches and allow extra reference quotes only under a declared policy. Intraday/price-unit/multiplier conventions and financial validation remain required. No account-aware valuation API was implemented.

## 7.12-E7

**Prompt:** Explain why a matched calendar-date key does not establish equal intraday valuation times.

**Scope:** SOURCE DATE REJECTION + INTRADAY DESIGN

The source rejects a different calendar label before matching. Equal2026-01-30 strings still do not establish the same intraday valuation instant,time zone,session,quote freshness or publication/decision availability. A wider snapshot contract needs explicit aware observation/valuation timestamps and allowed age,source/version and availability constraints. An as-of policy requires its own matching direction,tolerance,group keys and tests;none was implemented here.

## 7.12-E8

**Prompt:** Design source-row and batch-hash columns that preserve provenance across the merge without making those fields accidental join keys.

**Scope:** PROVENANCE DESIGN + SOURCE SCHEMA BOUNDARY

Propose distinct holdings_source_row/quotes_source_row,holdings_batch_sha256/quotes_batch_sha256 and explicit hash-kind/policy metadata,retaining exact source payloads beside them. Financial join keys remain explicitly on=[asset,currency,valuation_date] or the approved broader grain;lineage must not become accidental common-name join keys. Include per-side source ordinals for unmatched rows and distinguish file hashes from parsed-record hashes. Current source rejects added provenance columns under its exact schema,as probed;extending it requires revised validated schemas and evidence tests. Do not simply strip metadata and claim provenance preserved. No provenance-preserving merger was implemented.

Original source demonstration, discovery and compileall pass with FutureWarning as error. No unexpected QA failure or manuscript defect surfaced; first-run outputs and expected rejection traces retained. No historical unique methods or earlier workflow cases added by overlapping reruns. F28/F32, F37 history and platform/input/numerical/independent acceptance limits remain intact.
