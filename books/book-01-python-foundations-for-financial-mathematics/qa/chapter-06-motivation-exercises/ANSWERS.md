# Section 6.1 — eight scoped exercise answers

Prerequisites: the documented CPython 3.12 / NumPy 2.3.5 environment and an owned writable temporary directory. Actual run: CPython 3.12.14/Linux. Source execution, supplemental caller/representation checks and conceptual designs are distinct.

## 6.1-E1 — SOURCE + SUPPLEMENTAL CALLER

**Prompt:** Add a fourth aligned asset with start 40 and end 44; derive and test its fractional change.

Append ASSET-D with start 40 and end 44 in the same currency/per-unit convention and identifier order. The exact Fraction ratio 44/40−1=1/10 gives a 10% price-only change. The unchanged API returns shape (4,), float64 and values 5%,−5%,0,10% within the fixture tolerance; inputs are unchanged and the result does not share their storage. four_assets.py is a separate guarded caller. Its complete stdout is checked; the original three-asset source/main remain unchanged.

## 6.1-E2 — SUPPLEMENTAL REPRESENTATION DEMONSTRATION

**Prompt:** Demonstrate list repetition versus array multiplication with the same initial values.

Use the same values [2,4]. Python list repetition by 2 gives [2,4,2,4]; an integer ndarray multiplied by 2 gives [4,8]. Neither operation changes the original input in this example. This demonstrates different container semantics, not performance or a financial multiplication rule.

## 6.1-E3 — SOURCE + IDENTITY LIMIT

**Prompt:** Swap two end prices while keeping shape unchanged. Explain why numerical validation cannot detect the identity error.

Swap original end prices 105 and 76, leaving starts [100,80,50] and all shapes valid. The unchanged API accepts the finite nonnegative vector and gives exact rational targets −6/25,5/16,0 (−24%,31.25%,0). These are correct ratios for the supplied positions but are attached to the wrong original instruments. Shape/dtype/domain checks lack the identifiers needed to detect that error. Carry labels at ingestion and require exact matching identity/order or a separately validated alignment adapter; no adapter is implemented here.

## 6.1-E4 — SOURCE

**Prompt:** Add a test for a scalar zero-dimensional array and document why the API rejects it.

Pass exact float64 zero-dimensional arrays np.array(100.) and np.array(105.). The source raises ValueError because it requires nonempty rank-one vectors, even though both scalar values individually satisfy the price domain. A scalar end paired with a rank-one start also fails. This API deliberately does not promote scalars or broadcast them; NumPy scalar arrays are not inherently invalid elsewhere.

## 6.1-E5 — SOURCE + CONCEPTUAL INTERPRETATION

**Prompt:** Explain why replacing a missing end price with zero changes the financial interpretation.

The unchanged API rejects a NaN end price as missing/nonfinite. Replacing it with literal zero is accepted and gives −1, a 100% price loss from a positive start. That substitution invents an economic observation; it does not resolve unknown data. Preserve or reject incompleteness under an explicit upstream policy rather than silently zero filling. A genuine zero terminal quote and unavailable quote remain distinct.

## 6.1-E6 — PROPOSED POLICY + LIMITED NUMERICAL DEMONSTRATION

**Prompt:** Propose a tolerance policy for a different analytical scale; distinguish numerical tolerance from financial materiality.

For a separate dimensionless near-zero analytical question, propose exact shape/finite checks and abs(actual−reference) <= 1e-15 + 1e-8*abs(reference), subject to review of bounded inputs and consequences. The source ratio from 1 to intended decimal 1.0000000000003 is near the independent rational 3e-13. It agrees with that benchmark within 1e-15, but should not agree with zero: the original illustrative atol=1e-12 hides the discrepancy, while the proposed atol=1e-15 rejects it. These chosen tolerances demonstrate one scale and are not a proved universal error bound. Financial materiality depends on units, exposure, use and decision consequences; it cannot be inferred from this numerical predicate or from displayed percentages.

## 6.1-E7 — DESIGN + REPRESENTATION PROBES

**Prompt:** Explain what must change to support float32 without pretending the precision is unchanged.

Keep the original API rejecting float32. A proposed separate float32 interface would explicitly define accepted wire types, conversion point, output/accumulator dtype, bounds, overflow/underflow handling and error budget, then rerun high-precision references, near-zero/extreme ratios, ownership and domain checks appropriate to that representation. Do not silently retain float64 accuracy claims or reuse 1e-12 tolerances by habit. Executed probes show epsilon near 1 differs (2^-23 versus 2^-52), and 1.00000001 narrows to 1 in float32; widening that stored value and calling the original API yields zero change. A later wider type cannot recover discarded input information. No float32 API implementation or support claim is made.

## 6.1-E8 — DESIGN NOT TIMED

**Prompt:** Design a fair benchmark without claiming a speedup before executing it.

Benchmark the actual price-return contract: identical aligned inputs, domain checks, dtype and output representation, known-answer agreement first, then warm-up and repeated measurements at declared sizes. Separate list conversion from resident-array work and charge comparable validation to each candidate. Keep generation/import/reporting outside timers consistently; preserve source inputs, rotate order across sessions, record raw samples and Python/NumPy/build/hardware/thread/GC context, and measure peak memory separately from payload. Include small and larger sizes without a timing pass/fail threshold or promised speedup. No Section 6.1 benchmark was executed in this batch; the earlier measured Section 6.15 P&L workload is different.
