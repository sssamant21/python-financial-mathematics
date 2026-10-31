# Section 7.8 — Eight scoped local answers

Original cleaner execution is separate from E5/E8's supplemental field-audit implementation and E4/E7's unimplemented designs. These QA answers map the supplied prompts without changing the manuscript.

## 7.8-E1

**Prompt:** Inspect all three output tables and identify the source records behind each rejection.

**Scope:** EXACT SOURCE + ROW LINEAGE

Original good/bad/log counts are2/4/6. Rejected ordinals1 and2 are raw BETA and padded BETA,each duplicate_asset;ordinal4 BAD retains priceoops with invalid_price;ordinal5 EURO retains EUR with unsupported_currency. Accepted ordinals0(ALPHA600) and3(CASH100) plus rejected ordinals partition0..5,and each ordinal appears once in the decision log. The accepted subtotal700 is not a complete batch valuation.

## 7.8-E2

**Prompt:** Add a valid record with leading-zero identifier 00007 and confirm spelling is preserved.

**Scope:** EXACT SOURCE + RATIONAL ORACLE

Append00007 with text quantity0.5,price100,currencyUSD. The original cleaner preserves that spelling and accepts value(1/2)*100=50. Three accepted plus four rejected records conserve the seven-row input; adding a valid row does not resolve the four older rejections or establish portfolio completeness.

## 7.8-E3

**Prompt:** Add a third BETA record with an invalid price and confirm all BETA rows remain rejected.

**Scope:** EXACT SOURCE DUPLICATE POLICY

Append a third BETA at quantity1,priceoops,USD. All three normalized BETA rows at source ordinals1,2,6 remain rejected. The new record keeps duplicate_asset;invalid_price together;accepted assets remain onlyALPHA,CASH. An invalid competitor does not authorize choosing another unreviewed duplicate winner.

## 7.8-E4

**Prompt:** Propose a lot-level composite key and explain why the current asset-level duplicate rule would be wrong for it.

**Scope:** LOT-GRAIN DESIGN — NOT IMPLEMENTED

For multiple positions propose a stable composite key(account_id,instrument_id,lot_id) within an explicitly identified valuation snapshot;include snapshot date/time and currency/context if several snapshots are processed together. Stable lot identifiers must come from the source or a documented mapping,not local row order. Two legitimate lots of one asset can coexist,so the current asset-only duplicate rule would wrongly quarantine them. Define duplicate/revision policy at the actual grain,validate quantity/price/multiplier conventions,and aggregate to asset only under an explicit model. No lot-aware cleaner was implemented.

## 7.8-E5

**Prompt:** Add field-level before/after change records without modifying original input.

**Scope:** SUPPLEMENTAL FIELD-AUDIT IMPLEMENTATION

audit_extension.audited_clean first invokes unchanged clean(raw),then independently records approved field normalization differences without editing raw input. Fixture changes are ordinal0 asset" ALPHA "->"ALPHA",ordinal0 currency" usd "->"USD",ordinal2 asset" BETA "->"BETA":three changed fields across two changed rows. Accepted/rejected outputs and original decision columns match source output. Before/after values remain exact strings,linked to local ordinal plus the declared batch digest and policy version.

## 7.8-E6

**Prompt:** Explain why relabeling EUR as USD without conversion is not cleaning.

**Scope:** EXACT SOURCE + CURRENCY INTERPRETATION

The original EURO record remains rejected as unsupported_currency with raw EUR retained. Uppercasing eur toEUR changes spelling only;rewriting EUR toUSD without an actual exchange-rate calculation would falsely change the unit label while leaving the numeric amount unchanged. FX valuation needs rate direction,valuation/availability time,source and precision policies,not a cleaning shortcut.

## 7.8-E7

**Prompt:** Design an expected-asset-set check that runs after rejection handling and before valuation.

**Scope:** EXPECTED-UNIVERSE DESIGN — NOT IMPLEMENTED

After resolving or explicitly handling every rejected key,compare the full intended accepted asset set with independently supplied expected_assets before publishing a batch valuation. Keep rejected expected assets visible as unresolved;do not derive the expected set from accepted rows or call an accepted subset complete. Reject/withhold missing,extra or unresolved keys;do not silently fill values,choose duplicate winners or relabel currencies. Planned cases:exact complete set accepts,missing record blocks,extra accepted asset blocks,expected key only in rejection blocks,duplicates remain unresolved,source-order change preserves set result. Current fixture has rejections and stays not ready. No expected-set gate or new acceptance tests were implemented.

## 7.8-E8

**Prompt:** Extend the audit with a source batch hash and policy version; distinguish those fields from the local row ordinal.

**Scope:** SUPPLEMENTAL RECORD-HASH/POLICY AUDIT

The extension hashes a precisely declared canonical UTF8 JSON serialization of raw parsed records in source order,using fixed field order,compact separators,ensure_ascii=False and one final newline. source-batch.json retains those exact bytes. Decision/field-change rows carry source_batch_sha256 and policy_version=book1-7.8-strip-uppercase-currency-v1;source_hash_kind names this parsed-record serialization. Original pandas index labels are excluded deliberately;local ordinal resets per input and is not global identity. Same source records/order repeat the digest;reordering changes it. This is not the hash of an original CSV or vendor authentication. Retain original-file byte evidence separately when available and preserve the mapping to parsed records. A human policy-version label must be maintained when semantics change;it does not automatically attest implementation identity.

Full original demo/discovery/compileall and one supplemental audit caller pass. The supplement duplicates only the declared formatting policy to generate field-level differences; it does not replace the original cleaner's accepted/rejected decisions. Agreement is checked for the fixture,not proved for arbitrary future policy changes. Source/listing/extension hashes and raw outputs retained. No unexpected failure or manuscript defect surfaced; earlier F37 failure/correction remains intact. Numerical,source authenticity/completeness,platform and independent acceptance remain open.
