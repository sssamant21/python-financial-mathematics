# Section 7.5 — Eight scoped local answers

Exact-source ingestion and byte comparisons are separated from E7/E8 extension designs. The section supplies local prompts; these QA answers do not alter the manuscript or imply an absent-companion defect.

## 7.5-E1

**Prompt:** Change 00123 to 00007 and confirm the new identifier stays text.

**Scope:** EXACT SOURCE

Replace literal00123 with00007 in the exact CSV fixture. The original loader retains the index token as str"00007",its market value600 and total1000. Explicit text ingestion prevents leading-zero loss; literalNA also remains an identifier. No parser or financial algorithm was replaced.

## 7.5-E2

**Prompt:** Remove one complete asset record. Explain why uniqueness still passes and what independent coverage evidence is missing.

**Scope:** EXACT SOURCE + COVERAGE LIMIT

Remove the complete BETA record. The original loader accepts the two unique assets00123,NA and returns600+100=700. All remaining records are valid but the original expected portfolio is incomplete. An independently maintained expected asset universe,source record/control totals and context/version evidence are needed to detect a whole missing record; uniqueness and a finite sum cannot establish completeness. This is the source's documented boundary,not a new defect.

## 7.5-E3

**Prompt:** Change one currency or date and inspect the rejection.

**Scope:** EXACT SOURCE REJECTIONS

Changing one USD toEUR or one2026-01-30 to2026-01-29 raises ValueError against independently supplied USD/2026-01-30 expectations. Rejection traces are retained. Do not set the expected context from the first source row or rewrite the file to force acceptance; investigate the export and approved valuation context.

## 7.5-E4

**Prompt:** Put an empty numeric field into the CSV. Explain why zero-filling would change the model.

**Scope:** EXACT SOURCE + MISSING/ZERO CONTRAST

An empty BETA price token rejects. A literal price0 instead passes and gives BETA market value0,total700. Zero is an observed economic value under this loader's nonnegative-price contract; unknown price is unavailable information. Replacing empty text with0 would invent a complete observation and remove300 from the original valuation,not repair ingestion.

## 7.5-E5

**Prompt:** Save an equivalent CRLF fixture and compare its hash with the LF version.

**Scope:** EXACT SOURCE + BYTE EVIDENCE

The retained LF and CRLF files yield equal normalized tables and total1000. Each evidence digest matches its own exact payload; CRLF adds one byte per newline and changes SHA256. The LF digest is e68b437d0a8476c1b21a01a0ae4577144b54c79b8383d1f0d9779dd958297c11. This demonstrates controlled semantic equivalence,not a claim that arbitrary byte changes are harmless or that a hash authenticates a vendor.

## 7.5-E6

**Prompt:** Reorder complete records and verify that asset-level values and total are preserved, while the source hash changes.

**Scope:** EXACT SOURCE + KEY RECONCILIATION

Reverse complete source records. The returned index isNA,BETA,00123 while sorted-by-asset frame equality and total1000 are preserved. The raw-byte digest differs. Compare normalized results by key separately from source-byte identity; never move numeric fields independently of identifiers.

## 7.5-E7

**Prompt:** Design an expected-asset-set parameter with missing/extra asset rejection tests before implementing it.

**Scope:** CONTRACT/TEST DESIGN ONLY — NO EXPECTED-SET IMPLEMENTATION

Add a proposed independently supplied expected_assets tuple with unique trimmed nonempty strings under the workload cap. Require exact set equality after source schema/context/key validation and before valuation/publication; reject both missing and extra names with explicit differences,without filling,dropping or renormalizing. Accept row-order differences while retaining documented source order. DESIGN.md lists proposed acceptance/rejection cases and policy decisions before implementation. The current loader still accepts an extraOTHER row at value1,total1001; no proposed parameter or acceptance suite was executed.

## 7.5-E8

**Prompt:** Describe how a larger chunked workflow would detect duplicate assets appearing in different chunks.

**Scope:** CHUNKED DESIGN + LIMITED FULL-FILE ILLUSTRATION

A larger workflow must retain a global seen-key set or external unique-key registry across chunks,not just check duplicates within each chunk. Validate a fixed schema/context on every chunk; detect within-chunk and cross-chunk repeats,including equal values,then abort or quarantine under an explicit policy. Check the independently expected universe and aggregate controls only after the entire input completes; withhold final valuation/report publication on later failure. For bounded memory use a transactional unique-key staging table or external sort/partition strategy with global checks,not an unbounded in-memory set disguised as streaming. Original full-file loader rejects a duplicated record appended after the fixture;that is not a chunked implementation or scalability test.

Retained fixtures and snapshots establish exact reproducible local inputs/outputs,not source authenticity or an independently complete holdings universe. The hash placeholder in the original demonstration is resolved from the same fixture bytes; all other values/labels/row order match after whitespace normalization. No unexpected failure or manuscript defect surfaced. Prepared-runtime/platform/numerical/independent acceptance limits and F28/F32 remain open.
