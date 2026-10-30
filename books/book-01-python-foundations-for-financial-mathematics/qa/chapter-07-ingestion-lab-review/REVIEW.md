# Sections 7.5–7.8 — Formal workflow review

Each section has eight derived review units, separate from commands, predicates and existing methods. Setup is partial; six execution/assembly categories pass within scope and interpretation is conceptual.

## 7.5

Parse one bounded exact local CSV byte snapshot and validate its identity, numeric grammar, currency and calendar-label context before holdings valuation.

**Prerequisites/input:** UTF-8 local file <=1000000 bytes, exact ordered asset/quantity/price/currency/valuation_date header, 1–10000 correctly sized rows; unique trimmed literal IDs, unsigned ordinary decimal quantities/prices and explicit expected uppercase three-letter currency/calendar date.

**Output/step contract:** Indexed float64 holdings values, finite scalar total and evidence for the same parsed bytes: SHA256, byte count, row count and expected context.

**Independent expectation:** Literal IDs00123,BETA,NA;6×100+3×100+1×100=1000. LF fixture SHA256 e68b437d0a8476c1b21a01a0ae4577144b54c79b8383d1f0d9779dd958297c11; CRLF changes bytes/hash while the controlled parsed table stays equal.

**Scope/limits:** Hash is byte identity, not authenticity/freshness. File path and expected context are caller-owned; one bounded read is not an OS transactional snapshot against concurrent writers. No FX, intraday/session/calendar availability or arbitrary file/service integration is established.

## 7.6

Validate text tokens before choosing numeric/nullable/Boolean representations; preserve unknown counts and source row identity.

**Prerequisites/input:** Exact ordered asset/lot_count/price/reviewed text columns, 1–10000 rows, unique source index, cells strings <=64 chars, unique trimmed IDs. Counts unsigned whole text or empty unknown, checked exactly against Int64 max; prices ordinary unsigned decimal; reviewed exactly true/false.

**Output/step contract:** Source-index-preserving DataFrame with string, Int64, float64 and nullable boolean columns; missing count stays missing and observed zero stays zero.

**Independent expectation:** Price100.25=401/4; six/unknown/zero counts and true/false/true flags retained.2^63−1 preserved exactly;2^63 rejected before float conversion. Conversion-audit example has one introduced failure and two missing outputs.

**Scope/limits:** No CSV ingestion, valuation, FX or schema recovery after prior lossy conversion. Price float64 remains approximate; Boolean token mapping is narrow and rejects undocumented spellings. Constructor accepts raw text only and does not silently stringify Python numeric objects.

## 7.7

Assess complete expected asset coverage before publishing a one-interval portfolio return, distinguishing absent rows, explicit missing values and observed zero.

**Prerequisites/input:** Nonempty finite nonnegative ordinary numeric weight Series sum near one at atol1e−12/rtol0; zero-or-more ordinary numeric return rows with unique flat trimmed IDs subset of expected weights, NaN allowed but observed entries finite and>=−1.

**Output/step contract:** Aligned report in expected weight order, summary expected/observed/missing/absent/complete counts, and either a finite complete scalar total or None. Never fill, drop expected names or renormalize observed weights.

**Independent expectation:** Complete fixture9/200=0.045. A/C-only fixture has expected3,observed2,missing1,absent1 and totalNone. Explicit missing B has absent0. Empty return source has missing3/absent3. Observed zero permits total0; missing zero-weight asset still blocks the total.

**Scope/limits:** Completeness is relative to caller-supplied expected identities, not vendor/feed authenticity. Partial sums/renormalized observed totals describe another question. Price-only assumptions, common interval/currency and numerical-range/inference limitations remain; no market data repair or financial release approval.

## 7.8

Normalize only explicitly permitted formatting, validate all records, quarantine all normalized duplicate keys and retain a full source-row audit.

**Prerequisites/input:** Exact ordered asset/quantity/price/currency text schema,1–10000 rows,cells strings<=64 chars; same valuation instant/common USD long-only contract. Strip fields, uppercase currency only; asset case significant. Duplicate original row index allowed because source_row is a new local ordinal.

**Output/step contract:** Accepted numeric holdings table, rejected raw records with normalized asset/reasons, and one changed/status/reason audit row per local source ordinal. No batch aggregate is returned; any rejection means the fixture batch is not valuation-ready.

**Independent expectation:** Six rows conserve as2 accepted(ALPHA,CASH) and4 rejected; values600/100. Both BETA rows quarantined, including the raw spaced token. Two rows changed under normalization. Bad numeric and EUR rows retain explicit reasons.

**Scope/limits:** Normalization is specific to this source policy, unlike strict whitespace rejection in7.5/7.6; currency spelling normalization is not FX. Accepted subtotal700 is not a complete batch valuation. Local ordinals are not global identity, read-only enforcement is absent, and provenance/concurrency/extreme monetary accuracy remain broader integration limits.

Standalone files, temporary layouts and documented commands remain unchanged. The 7.6/7.7 explanatory fragments assume pandas is imported, supplied explicitly in the QA namespace. The 7.8 duplicate-mask fragment assumes normalized; QA captures that DataFrame from an unchanged original clean(fixture()) return-event trace, rather than reimplementing normalization. Prelude orchestration is labelled separately from original fenced statements. All snippet hashes/stdout are retained.
