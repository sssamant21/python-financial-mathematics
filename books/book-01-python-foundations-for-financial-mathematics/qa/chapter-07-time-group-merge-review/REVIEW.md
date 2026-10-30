# Sections 7.9–7.12 — Formal workflow contracts

Four workflows each have eight derived review units, separate from command checks, predicates and reference-method invocations. Setup remains partial; six assembly/execution categories pass within scope; interpretation is conceptual.

## 7.9

Build a unique sorted UTC price Series without separating price/time identity; distinguish inclusive and half-open windows.

**Prerequisites/input:** Exact ordered timestamp/price columns, 1–10000 single-instrument rows. Second-resolution YYYY-MM-DDTHH:MM:SS with Z or numeric offset; Python calendar/clock checks and offset bounds before explicit pandas UTC parsing. Prices ordinary NumPy-backed i/u/f, finite nonnegative; no numeric strings/Boolean/extension types.

**Outputs/step alignment:** Owned float64 price Series, event_time index unique/sorted/UTC. Reject duplicate normalized instants; do not choose a duplicate winner. Source remains unchanged.

**Independent expectation:** 09:30-05:00 = 14:30Z. 10:00-05:00 and 16:00+01:00 both equal15:00Z and must reject. Corrected16:30+01:00 yields15:30Z; ordered values100,101,102. 15:00..15:30 inclusive has2 observations, half-open has1; elapsed first interval1800seconds.

**Limits:** Numeric offset does not establish regional zone identity/rules. Original named-zone tests execute winter conversion, ambiguous/nonexistent 2026 wall times and roundtrip only on this host. Sorted/unique data is not complete trading-calendar coverage or decision-time availability. Date_range labels are not observations; timestamp extremes, leap seconds, venue schedules and platform timezone providers remain outside acceptance.

## 7.10

Validate all source rows, filter eligibility, rank deterministically, then limit the reporting subset.

**Prerequisites/input:** Exact ordered asset/sector/market_value columns,1–10000 rows,unique asset IDs,trimmed text<=64 chars; ordinary finite nonnegative numeric values. Validated finite nonnegative real floor, exact sector, Integral limit1–10000; bool floor/limit rejected. Input index may repeat and is lineage only.

**Outputs/step alignment:** Independent report preserving source index and schema, sorted value descending/asset ascending. Evidence includes criteria and input/eligible/returned counts. Fixed authored query matches mask; empty no-match result retained without invented values.

**Independent expectation:** 5 inputs,3 equities at inclusive floor300; rank ALPHA600,BETA600,GAMMA300,return2. Limit1 choosesALPHA regardless source order. Bond filter before head yieldsDELTA800; head-before-filter yieldsnone. Unselected invalid value still fails.

**Limits:** Eligibility/truncation changes population; report totals are not full portfolio value or performance. Supplied market values, common snapshot/currency, classification and availability remain caller contracts. Query is authored fixed expression with validated local values, never an untrusted expression sandbox. No performance benchmark or trading recommendation.

## 7.11

Aggregate complete asset observations by sector; distinguish value-weighted sector return, portfolio contribution and simple mean.

**Prerequisites/input:** Exact ordered asset/sector/opening_value/asset_return,1–10000 rows,unique asset IDs,trimmed complete keys,ordinary finite numeric values>=0 and returns>=-1. One common interval/currency/snapshot, no flows/fees/FX/distributions/rebalancing; positive total opening value.

**Outputs/step alignment:** Sector-keyed counts,opening values,P&L,portfolio weights/contributions,sector return plus portfolio return. Observed zero-value sector retained,own returnNaN,contribution0. Missing input even on zero exposure rejected; no complete portfolio denominator for all-zero input.

**Independent expectation:** 600*(1/10)+300*(-1/20)=45; equity opening900,sector return1/20=.05,portfolio contribution9/200=.045,weight.9. Simple mean1/40=.025. Group counts4,opening1000,contributions.045. Transform[900,900,100,0] sums1900,not1000.

**Limits:** Group output cannot establish expected asset-universe completeness or correct classification/context. NaN on zero denominator is intentional, unlike missing source input. Float64 rounding/underflow remain; finite-output/overflow guards are not exact settlement accounting. Only fixture order invariance/tolerances checked, not universal bitwise reduction invariance.

## 7.12

Match holdings and quotes by complete snapshot key with cardinality and exact-population coverage before valuing.

**Prerequisites/input:** Each source1–10000 rows, exact ordered asset/currency/valuation_date plus quantity or price, complete trimmed string keys<=64 chars,unique composite keys, fixed USD/2026-01-30. Ordinary finite nonnegative numeric measures. Compatible per-unit and intraday context assumed upstream.

**Outputs/step alignment:** Sorted outer audit with both/left_only/right_only indicator. Complete one-to-one key population yields independent float64 valuation and finite total; any unmatched holding OR extra quote returns result=None,total=None. Source indices are not financial identity.

**Independent expectation:** 6*100+3*100+1*100=1000. Alternative6*(203/2)+3*(321/4)=849.75. MissingCASH retainsleft_only and blocks total;extraOTHER retainsright_only and also blocks. Zeroquantities permit total0. Original methods demonstrate2-by-2 merge4rows,many_to_one rejection/validalternategrain,null-null pandasmatch and indexjoin.

**Limits:** Exact same populations is a narrow policy; broad-reference left join needs another explicit policy. Calendar date match is not intraday synchronization, observed/authentic price or independently complete holdings universe. No as-of/fuzzy/FX matching; provenance fields would need explicit columns, not accidental join keys. Cardinality bounds rows,not peak memory; float64 is approximate.

All 11 explanatory Python fences run unchanged. The Section 7.9 interval fragments presuppose series/start/end, supplied from the documented corrected fixture and 15:00/15:30 boundaries; its first localization fragment supplies naive/local/utc itself. Section 7.10's first sort fragment presupposes eligible before the later mask fragment defines it: QA supplies the stated mask, default floor/sector and exact fixture. Section 7.11 aggregation presupposes table/price_pnl: QA supplies the original fixture and stated V*r expression; the later transform uses that same table. Section 7.12 merge presupposes holdings/quotes, supplied from original fixture(). These are explicit supplemental prelude statements, not newly standalone source examples. No prior lab module is required by any complete listing.

Original methods cover DST error names, source reversal/copy behavior, invalid domains, missing-key mechanics, overflow and merge multiplication. Supplemental source calls add controlled boundary/input checks, not replacements for original algorithms. No supplemental financial implementation is claimed. No manuscript defect or unexpected QA failure occurred; first-run results retained. Exercises remain pending, so this workflow review does not mark any of the 136 local prompts complete. Troubleshooting explanations are consistent with the observed contract; venue calendars, classification sources, temporal matching designs and independent acceptance remain unexecuted.
