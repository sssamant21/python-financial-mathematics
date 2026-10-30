# Section 6.16 — Eight scoped project-extension answers

Prerequisites: Section 6.1 prepared runtime, unchanged self-contained project files and original long-only fixed-quantity one-interval same-currency contract. Caller preserves labels, quote conventions and source completeness. New extension boundaries and limitations are stated separately. Reviewer: Codex executor, 2026-10-30; no independent acceptance.

## 6.16-E1

Add a renderer that displays each asset contribution as percentage points without changing stored precision.

**SUPPLEMENTAL RENDERER + UNCHANGED SOURCE REPORT**. render_contributions looks up a named row and formats 100 times each dimensionless contribution as signed percentage points, four decimals. The up scenario renders ALPHA +6.0000 pp, BETA −1.5000 pp and CASH +0.0000 pp. It does not round or overwrite report arrays; byte equality confirms stored precision remains unchanged. Output is presentation only, not currency P&L, accounting rounding or a reactive report.

## 6.16-E2

Add a named scenario lookup. Reject unknown names and test that lookup preserves row identity.

**SUPPLEMENTAL NAMED LOOKUP + ROW IDENTITY PROBES**. lookup validates an exact text scenario name against the source report tuple, rejects unknown names with KeyError, and returns the matching name, row index, asset tuple, scalar outcomes and an independent read-only contribution-row copy. The down lookup returns row1 and P&L −105. Ordinary edits do not affect the report; read-only ownership remains an interface convention, not security-grade immutability. The helper consumes trusted valid Report objects from the source rather than validating arbitrary externally constructed objects.

## 6.16-E3

Add an ingestion adapter that aligns a labeled mapping to the asset tuple; test missing, extra, and duplicate identifiers before constructing arrays.

**SUPPLEMENTAL LABELLED PRICE INGESTION ADAPTER**. align_prices takes the required asset tuple and a labelled Mapping or lossless sequence of key/value pairs. Validate trimmed unique IDs and exact key-set equality before array construction, then align explicitly to the tuple. For CASH100,BETA95,ALPHA110 it returns float64 [110,95,100], and the original calculator gives ending1045. Missing, extra and duplicate-pair cases fail with ValueError while an np.array trap confirms no array construction occurs. A dict cannot reveal duplicate keys already discarded by an earlier parser; retain wire pairs (for example via a suitable JSON object-pairs hook) before constructing a mapping. The helper itself does not implement a JSON parser. It rejects raw Boolean mixtures, text/complex and nonfinite/negative closing prices before conversion. This scoped adapter does not resolve all source arbitrary-input schema issues or Chapter2 F32; original source mixed-Boolean preconditions remain documented. Exact integer/decimal money and source provenance require separate policy.

## 6.16-E4

Replace the constant-price CASH fixture with a supplied interest-bearing instrument. State whether the closing quote already includes interest.

**SUPPLIED INTEREST-BEARING QUOTE + ORIGINAL SOURCE EXECUTION**. Replace every scenario CASH closing quote100 with100.2 while keeping opening100 and quantity1. Explicit assumption: this quote is an interest-bearing mark including the whole entitled interval interest, capitalized once with no separate cash distribution added. Ending values become [1045.2,895.2,1000.2], returns [0.0452,−0.1048,0.0002]. Independent rational values reconcile the cash gain0.2 and total opening1000. This is a supplied quote convention, not an interest-accrual/day-count engine; do not add interest again if already included in the closing quote.

## 6.16-E5

Add a batch-of-portfolios interface using the shape contract from Section 6.11. Define portfolio labels and memory limits before writing a matrix product.

**SUPPLEMENTAL BATCH IMPLEMENTATION + SOURCE/RATIONAL ORACLES**. batch_portfolios declares Q shape(P,N), opening prices(N,), closing prices(S,N), portfolio labels(P), scenario labels(S) and identical ordered asset tuples(N). Require exact finite float64 arrays, nonnegative quantities/closes, positive openings and a positive opening denominator for every portfolio. The exact-int max_cells policy is1..100000 and checks each Q,closing and output(S,P) footprint before the product; it is not peak RSS or a pre-ingestion allocation guard. Compute values/weights(P,N), asset returns(S,N), portfolio returns R@W.T, ending values P1@Q.T and P&L(S,P); omit an S-by-P-by-N contribution cube. Return independent read-only arrays with both surviving label axes. Controlled portfolios [6,3,1] and [2,3,5] give ending rows [[1045,1005],[895,975],[1000,1000]] and return rows [[0.045,0.005],[−0.105,−0.025],[0,0]]. Each portfolio also reconciles with an original single-portfolio source call. Duplicate portfolio labels, too-small cell budget and zero-value portfolio fail. This is a bounded teaching implementation, not arbitrary-wire validation, leveraged accounts or comprehensive independent acceptance.

## 6.16-E6

Add distributions only after specifying per-unit cash amounts and timing. Update both return and direct valuation routes together.

**SUPPLEMENTAL DISTRIBUTION IMPLEMENTATION + TWO UPDATED ROUTES**. distribution_report assumes fixed long quantities, common scenario horizon, raw ex-distribution closing prices and explicit nonnegative gross cash per unit in a finite exact float64 matrix(S,N). Cash is entitled once per held unit and credited at the horizon, without reinvestment, taxes, fees or interim interest; early payments would need an explicit carry/reinvestment model. Update asset total-return route to (P1+D)/P0−1 and weighted contributions, and direct value route to base ending plus D@q, with P&L against the same opening denominator. The controlled D rows [[1,2,0],[0,1,0],[0.5,0,0]] give cash [12,3,3], ending [1057,898,1003], returns [0.057,−0.102,0.003] and P&L [57,−102,3]. The routes reconcile within explicit fixture tolerance; wrong shape fails and input D is preserved. No extra distribution may be added to an already total-return-adjusted quote. The original source stays price-only; this is a separate implementation with its own assumptions and no entitlement/FX/accounting integration.

## 6.16-E7

Benchmark repeated validated calls and compare them with a separately validated resident-array kernel. Report the two boundaries independently.

**EXACT SOURCE VALIDATED-CALL TIMING + SUPPLEMENTAL RESIDENT SNAPSHOT**. resident_snapshot copies inputs, calls the original calculator to validate that owned snapshot once outside timing, marks resident arrays read-only, and returns a kernel that recomputes the same six arrays/opening scalar and Report representation on each call. It keeps arithmetic error/finiteness checks and read-only independent outputs, but does not repeat input/label/schema checks or copies every call. Numerical gates compare every field to the source and verify snapshot isolation after a caller edit. Time repeated original calculate calls separately from the resident kernel using the same tiny three-asset/three-scenario workload: one warm-up, five samples of20 calls each, raw seconds-per-call/minimum/median retained in timings.json. The full source boundary charges validation/copies each time; resident setup validation/copies are excluded explicitly. No like-for-like end-to-end speedup, timing threshold, machine-independent ratio or peak-memory claim is made. Read-only arrays are not transactional snapshots or security-grade immutability; concurrent input writers and malicious edits remain outside scope.

## 6.16-E8

Add a test with tiny price changes and explain when direct P&L and return reconstruction lose significant digits differently.

**EXACT SOURCE EXTREME-SCALE OBSERVATION + RATIONAL ORACLE**. Use quantity3, opening price10^16 and closing10^16+2, a small relative price change with exactly represented integer prices. Exact represented-input P&L is3×2=6. On this runtime the source direct ending-minus-opening valuation yields8 because each large mark rounds; return reconstruction opening_value×portfolio_return gives6.661338147750939 because the ratio/subtraction rounds differently. The separately evaluated delta expression q×(P1−P0) gives6 for this fixture. Retain all values and exact absolute errors in tiny-change.json. This does not prove a universally best formula: it demonstrates different losses at large magnitudes within finite arithmetic. The manuscript explicitly disclaims arbitrary-scale/cent-exact accuracy, so this is retained as a numerical limitation rather than an inferred source defect or an instruction to relax criteria. Choose appropriate scaling, independently justified tolerances and exact monetary representation where required; no algorithm is silently replaced.
