# Sections 7.1–7.4 — Formal workflow review

Eight derived review units per section are metadata records, not eight new labs/tests. Each setup is partial; six execution/assembly categories pass within recorded scope and one interpretation category is conceptual. Commands, comparison predicates and existing unittest methods remain separate.

## 7.1

Align long-only opening weights and common-interval simple price returns by a unique complete asset set before contribution arithmetic.

**Prerequisites/input:** Two pandas Series, each 1–10000 values, flat unique trimmed nonempty text index; ordinary NumPy-backed i/u/f dtype, finite; nonnegative weights sum near one at atol1e−12/rtol0; returns>=−1. Order may differ.

**Output/step contract:** Independent aligned weight/return/contribution DataFrame in weight order and finite scalar total, no silent normalization.

**Independent expectation:** 3/5×1/10 + 3/10×(−1/20) = 9/200 =0.045; positional mismatch gives1/40=0.025.

**Scope/limits:** Caller owns interval/currency/label provenance; original numeric inference cannot recover earlier Boolean mixing. Float conversion/range/underflow/materiality remain bounded limitations. This is price-only, not financed/flow/FX accounting.

## 7.2

Construct an owned opening-value Series with explicit asset identity and metadata.

**Prerequisites/input:** Tuple of 1–10000 unique trimmed nonempty strings, matching one-dimensional inferred real numeric vector, finite and nonnegative; raw strings/Boolean/complex/object arrays rejected. Mixed Boolean/numeric source records require upstream checks.

**Output/step contract:** Owned float64 Series with index name asset and Series name opening_value. Zero or all-zero values accepted; positive-weight denominator is a later contract.

**Independent expectation:** ALPHA600+BETA300+CASH100=1000; label BETA and position1 both300 only in this fixture. Missing reindex slot has size2/count1 and strict sum missing.

**Scope/limits:** Names do not validate valuation time/currency. Numeric deep-copy/export behavior is scoped, not recursive object immutability; large integer conversion and future aggregates may lose precision/overflow.

## 7.3

Validate a same-currency long-only holdings table and derive currency market values.

**Prerequisites/input:** DataFrame with 1–10000 rows, exact unique quantity/price columns, flat unique trimmed text asset index, ordinary NumPy-backed numeric columns, finite and nonnegative. Extra derived/currency columns rejected by narrow source schema.

**Output/step contract:** Independent float64 quantity/price/market_value table and finite scalar sum; original row identities preserved, canonical columns ordered.

**Independent expectation:** 6×100+3×100+1×100=1000; alternate prices101.5,80.25,1 give850.75 by rational arithmetic.

**Scope/limits:** Common currency/time/per-unit conventions are caller preconditions. Return table is mutable and market_value does not react to later edits. Zero values accepted. Float precision/tiny underflow/arbitrary magnitudes and live joins remain outside acceptance.

## 7.4

Select required existing numeric rows/columns by explicit ordered labels, preserving table axes and independent numeric storage.

**Prerequisites/input:** DataFrame 1–10000 rows and1–20 columns with unique flat trimmed text axes; nonempty unique existing tuple row/column requests; selected columns ordinary NumPy-backed i/u/f. Source financial validation is required upstream.

**Output/step contract:** Deep-copied numeric DataFrame in requested axis order; singleton remains(1,1). Dtypes preserved; unknown helper keys fail ValueError.

**Independent expectation:** CASH then ALPHA with price/market_value gives [[100,100],[100,600]]; separate price110 repricing recomputes ALPHA660 and total1060.

**Scope/limits:** Selector intentionally accepts NaN, infinity, negative values and stale derived fields. It validates selection identity, not valuation or completeness. External mask unknowns, discarded labels, Copy-on-Write/storage contexts and concurrency need explicit contracts.

All demonstrations, discovery and compilation commands run from the parent directories specified by the manuscripts. Quiet-import checks run inside the corresponding sibling-file directory. Section7.4 explanatory fragments require t; the QA prelude constructs t using the exact original fixture(). Other explanatory snippets run unchanged in their original order, retaining stdout and source-fence hashes. No supplemental financial implementation is substituted for a source listing.
