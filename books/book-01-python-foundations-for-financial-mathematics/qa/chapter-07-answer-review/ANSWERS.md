# Chapter 7 — Twenty scoped answers

Reviewer: Codex executor, 2026-10-30. Prepared CPython3.12.14/pandas2.2.3/NumPy2.3.5 runtime; fresh environment and independent acceptance remain outside scope. Captured source locals, assertions and supplemental materializations are distinguished below.

## 7.18-P01 — Label alignment

Weights are A=.6, B=.3, C=.1; returns arrive in order C=0, A=.1, B=-.05. Calculate aligned contributions and explain the positional error.

**SOURCE + RATIONAL ALIGNMENT**. Pair by asset label: A contributes (3/5)(1/10)=3/50, B (3/10)(−1/20)=−3/200 and C0; total9/200=0.045. Positional pairing with arrival order C,A,B yields1/40=0.025. Captured input orders and original assertions are retained. Validate unique expected identities and completeness before alignment; pandas outer alignment and skip-missing sums do not establish coverage.

## 7.18-P02 — Series metadata and access

Construct opening values A=600, B=300 with name opening_value and index name asset. Compare label and position access, and explain integer labels.

**SOURCE METADATA/ACCESS**. The source builds float64 Series named opening_value with index name asset and values A600,B300. loc[B] and iloc[1] select the same300 in this fixture. With integer index[1,0], loc[0] selects second value20 while iloc[0] selects first value10. Labels are identities, not implicit positions; duplicate/missing keys and input schema need separate policy.

## 7.18-P03 — Table dimensions and units

Create quantities [6,3] and prices [100,100] by assets A,B. Derive value, total it, and compare selecting price as a Series versus a table.

**SOURCE + INTEGER VALUE ORACLE**. Six units at100 give600, three at100 give300, total900 in the stated currency. The captured table includes quantity, price and value columns. Selecting price with one bracket yields a Series; price as a one-column list yields shape(2,1) DataFrame. Quantity, per-unit price and value have different units and must not be added across a row.

## 7.18-P04 — Selection and ownership

For A,B,C values 600,300,100, compare label slice A:B and position slice 0:1. Select C,A in requested order into an independent copy.

**SOURCE SELECTION/OWNERSHIP**. On this ordered unique A,B,C index, loc[A:B] includes A and B; iloc[0:1] includes only first position A. The independent deep-copied C,A subset preserves requested order. Editing its A value to0 leaves source A600 unchanged, as both captured frames show. This is the numeric-column fixture, not a promise of recursive deep copies of arbitrary nested Python objects.

## 7.18-P05 — CSV identifier policy

Read CSV text asset,price followed by 00123,100 and NA,80. Preserve both identifiers literally and parse prices separately. Explain why inferred dtypes are insufficient.

**SOURCE TEXT INGESTION**. Read the controlled CSV as text with default missing-token handling disabled. Captured asset IDs remain exactly00123 and NA; prices remain text until separate explicit numeric conversion, totaling180. Default inference can erase leading zeros or interpret NA as missing. Preserve raw IDs, enforce expected schema and numeric grammar/range separately; successful conversion alone is not upstream label validation.

## 7.18-P06 — Nullable whole counts

Represent [6,unknown,0] as nullable Int64. Explain why unknown differs from zero and why casting 1.75 to an integer is not validation.

**SOURCE NULLABLE TYPE/DOMAIN**. Nullable Int64 holds [6,pd.NA,0], preserving unknown versus observed zero. Captured values/dtype and source truncation assertion are retained: casting1.75 to ordinary int64 gives1 in this fixture, not a proof that the input was a whole count. Validate whole-count syntax, sign/range and missing policy before conversion; do not replace missing with0 to satisfy an integer kernel.

## 7.18-P07 — Conversion audit

Convert [100,BAD,None] from text with errors=coerce. Count introduced failures separately from all missing results. Explain Boolean parsing.

**SOURCE CONVERSION AUDIT**. [100,BAD,None] converts to [100,missing,missing]. One nonmissing original token introduces a conversion failure; two outputs are missing in total because one input was already missing. Preserve original token, row identity and failure reason rather than conflating the counts. bool(false-text) is True for a nonempty string; use an explicit allowed-token mapping with separate unknown/rejection behavior, not Python truthiness. A general Boolean parser is explained, not implemented here.

## 7.18-P08 — Incomplete aggregation

For contributions [.06,NaN,0], compare default sum, skipna=False and min_count=1. Explain whether any proves complete portfolio coverage.

**SOURCE INCOMPLETE AGGREGATION**. For [0.06,NaN,0], default sum and min_count=1 produce0.06, while skipna=False remains missing. The source also demonstrates that an all-missing default sum can be0. These operations describe available cells; none independently validates expected assets, unique identities or missing population. Report a partial contribution explicitly and require the expected coverage contract before calling it whole-portfolio return.

## 7.18-P09 — Audited duplicate normalization

Normalize surrounding spaces in asset values [ BETA ,BETA,CASH]. Flag all normalized duplicate records rather than choosing a winner. State what evidence must be retained.

**SOURCE NORMALIZATION AUDIT**. Stripping surrounding spaces maps the first two raw asset tokens to BETA and marks both duplicate with keep=False; CASH is not duplicate. Captured raw data still contains the spaced token. Retain original record/field tokens, normalized key, source/batch/row identity and transformation/rejection/precedence reason. Do not choose a winner or alter case silently; duplicate policy depends on the declared grain and revision contract.

## 7.18-P10 — UTC identity

Parse 2026-01-30T10:00:00-05:00 and 2026-01-30T16:00:00+01:00 as UTC. Are they unique observations under a one-price-per-instant contract?

**SOURCE + MANUAL OFFSET ARITHMETIC**. 10:00 at−05:00 plus5 hours and16:00 at+01:00 minus1 hour both give15:00 UTC on2026-01-30. Source normalization captures identical instants and nonunique index. Under one-price-per-instant this is a duplicate requiring rejection/reconciliation, not two unique observations. Multiple events per instant need a richer instrument/venue/event or revision key.

## 7.18-P11 — Localization and interval closure

Localize winter New York 09:30 on Jan 30, 2026, convert to UTC, then contrast inclusive label selection with [start,end) on two half-hour instants.

**SOURCE LOCALIZATION/BOUNDARY CONTRACT**. New York winter09:30 on2026-01-30 becomes14:30 UTC; localization attaches the source-zone interpretation and conversion preserves the instant. For14:30 and15:00 observations, inclusive label slicing retains both endpoints while the half-open [14:30,15:00) mask retains only14:30. These are observed fixtures, not a full DST/calendar or market-session acceptance test.

## 7.18-P12 — Deterministic screening

For B=600 equity, A=600 equity, C=300 equity and D=800 bond, filter equity values at least 300 and return the top two. Compare mask and fixed query; define tie order.

**SOURCE SCREENING + INDEPENDENT ORDER RULE**. Both the explicit mask and authored query retain B600,A600,C300 equities and exclude D800 bond. Sort value descending, asset ascending, then take two: A,B. The runner independently applies that sort rule to captured candidates. A fixed authored query with bound parameters is not an interface for arbitrary untrusted expression text; screening does not establish investment suitability.

## 7.18-P13 — Sector return denominators

Equity holds opening values [600,300] with returns [.1,-.05]; cash is 100 at return zero. Calculate equity weighted return, simple mean and portfolio contribution.

**SOURCE + RATIONAL DENOMINATORS**. Equity gain600×0.1+300×(−0.05)=45 over900 gives1/20=5%. Simple two-asset mean is(0.1−0.05)/2=1/40=2.5%. Equity contribution to the1000 total portfolio including100 zero-return cash is45/1000=9/200=4.5%. Sector returns and portfolio contributions have different denominators; do not sum sector returns without compatible weights.

## 7.18-P14 — Merge cardinality

Merge two holdings records for A with two quote records for A. Show row multiplication and reject it under a many-to-one quote contract.

**SOURCE MERGE FAILURE + COMBINATORIAL ORACLE**. Two left A records crossed with two right A quotes yield2×2=4 pairs in the unvalidated merge. The original suite retains expected pandas MergeError for validate=many_to_one because the quote key is not unique. Fix declared quote grain/precedence explicitly rather than choosing an arbitrary duplicate. Cardinality validates multiplicity only; it cannot establish match coverage, quote freshness, currency or correct asset provenance.

## 7.18-P15 — Merge coverage

Holdings have A and B, while quotes have A and C. Perform a validated outer audit and identify every match category. Explain why an inner result is insufficient.

**SOURCE OUTER COVERAGE AUDIT**. Validated one-to-one outer audit retains A as both, B as left_only and C as right_only. An inner join keeps only A, hiding the unpriced B holding and extra reference C. Define whether unused reference quotes are allowed, but do not silently drop required holdings. Retain match indicators and join-key evidence before valuation.

## 7.18-P16 — Observed-event bars

Use UTC events 14:00 price100 volume10, 14:29 price102 volume20 and 15:00 price101 volume5. Form left-closed, right-labeled 30-minute bins; retain the empty middle bin.

**SOURCE + SUPPLEMENTAL BIN MATERIALIZATION**. Under UTC left-closed, right-labelled30-minute bins, events14:00/14:29 occupy[14:00,14:30), labelled14:30. Their OHLC is[100,102,100,102] and volume30. The[14:30,15:00) bin labelled15:00 is empty and its OHLC/volume remain missing with min_count=1. The15:00 event belongs to[15:00,15:30), labelled15:30, not the empty middle bin. Source assertions cover counts[2,0,1]; the QA runner separately materializes labels/bars to inspect them. Empty supplied events do not prove no market trading or feed completeness.

## 7.18-P17 — Rolling and expanding

For prices [100,102,104,106], calculate a three-observation mean with three required observations, expanding mean and previous-row rolling mean. Explain warm-up gaps.

**SOURCE WINDOWS + INDEPENDENT ARITHMETIC**. Three-observation mean with min_periods3 is[missing,missing,102,104]. Expanding means are100,101,102,103 from cumulative scalar sums divided by1,2,3,4. Shifting rolling means one row gives[missing,missing,missing,102]. Preserve warm-up gaps and distinguish row lag from elapsed delay, calendar interval or actual publication availability; descriptive alignment alone is not proof of a historically usable feature.

## 7.18-P18 — Price return linking

For prices [100,110,99], calculate simple returns without filling and compare their sum, linked result and endpoint ratio.

**SOURCE + RATIONAL LINKING**. Prices100,110,99 give an undefined first return and subsequent1/10,−1/10. Sum is0; gross product(11/10)(9/10)=99/100 gives linked−1/100=−1%, matching endpoint99/100−1. Source uses pct_change(fill_method=None), retaining the missing first interval. These are one-asset price-only intervals under consistent conventions; no distributions, FX or annualization are added.

## 7.18-P19 — Expected multi-asset grid

A has prices100,110,99 on three times; B has200 and220 only on first/last. Build wide prices on both assets and all times, then calculate adjacent-grid no-fill returns.

**SOURCE EXPECTED-GRID COVERAGE**. Expected wide grid contains A[100,110,99] and B[200,missing,220] on all three times. A has returns0.1,−0.1; B has no observed adjacent-grid return because each required pair touches its missing middle price. Its two-step endpoint change220/200−1=0.1 is still known, with a different horizon. No interval is complete across both assets. Do not drop the middle row, fill it, or relabel the two-step endpoint as a final one-step return.

## 7.18-P20 — Analyzer evidence and release decision

For the incomplete panel in Problem19, specify a report with source hash, record count, expected axes, complete-path flags and separate endpoint/linked fields. Explain which evidence can authorize a linked path result.

**SOURCE COMPACT POLICY + SUPPLEMENTAL CONCRETE RECORD**. The companion demonstrates linked-path withholding but uses a compact dummy payload hash check, not a full parser/report for the five-record panel. QA retains panel.csv and panel-report.json as an explicit controlled supplement: actual payload SHA256, five data records, expected two assets/three exact UTC times/six cells, five observed cells, versions and strict no-fill policy. A has3/3 prices, endpoint−0.01 and independently rational-linked−0.01; B has2/3, endpoint0.10, linkedNone and release_linkedFalse. The runner forms the linked product only for a complete expected-grid path. A linked result may be released only under complete validated required prices/identities/timing/units/adjustment conventions and successful numerical checks; an endpoint or digest alone is insufficient. Hashes identify bytes, not authenticity or availability. This supplement is not execution of Section7.17 analyzer/parser or independent release approval; its full project and malformed-input review remain pending.
