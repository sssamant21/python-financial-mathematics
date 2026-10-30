# Section 6.3 — eight scoped exercise answers

Prerequisites: the documented Python/NumPy environment and an owned writable temporary directory. Actual run: CPython 3.12.14, NumPy 2.3.5, Linux. The original implementation and tests remain unchanged. Supplemental constructions, completion validation, exact whole-unit policy and design-only proposals are distinguished.

## 6.3-E1 — SUPPLEMENTAL CONSTRUCTION + RATIONAL ORACLE

**Prompt:** Create a seven-point shift grid including -0.015 and 0.015; derive the spacing and test its count.

Seven points including both endpoints require six equal gaps: (0.015−(−0.015))/6=0.005=1/200. Construct float64 linspace with num=7 and endpoint=True; independently derive −0.015,−0.010,−0.005,0,0.005,0.010,0.015 using Fraction. Count, endpoints, dtype and all underlying values pass explicit checks (absolute tolerance 1e-15 for binary approximations). seven_points.py is a separate construction example; it does not silently replace the original five-row scenario workspace or claim a valuation.

## 6.3-E2 — SUPPLEMENTAL CONSTRUCTION

**Prompt:** Add a typed integer observation-index array starting at zero and document its purpose.

Use np.arange(7,dtype=np.int64), yielding [0,1,2,3,4,5,6]. It identifies the ordinal positions of the seven synthetic grid observations in this separate example. It is not a date, year fraction, forecast horizon or replacement of the source periods array [1,2,3,4]. The zero origin, length, dtype and intended correspondence must remain explicit when pairing it with data.

## 6.3-E3 — SOURCE

**Prompt:** Add tests at the rate-vector length bounds of 1 and 1,000.

The unchanged rate_vector accepts one and 1,000 exact text entries, tested with canonical 0.025=1/40. Both produce the expected one-dimensional float64 shape, all values and unchanged source tuple. Zero and 1,001 entries fail with ValueError. These checks establish the declared length boundaries for the supported text, not all possible wire inputs.

## 6.3-E4 — SOURCE ROLES + CONCEPTUAL INTERPRETATION

**Prompt:** Explain why a true missing price must not be filled with a neutral factor of one.

Original results contain 15 NaNs with all completion flags false; factors contain three ones for a separate neutral multiplicative role. A factor of one asserts unchanged multiplicative value, while a price of one asserts a particular quote in its units. Neither means unknown. Substituting one for a truly missing price would invent data and can change returns or valuations. Reject or retain incomplete status under an explicit missing-data policy; no price imputation was implemented.

## 6.3-E5 — SUPPLEMENTAL IMPLEMENTATION

**Prompt:** Design a completed-result validator that rejects any unfinished entry without replacing NaN silently.

completion.validate_completed implements a separate teaching boundary: exact nonempty two-dimensional float64 results, exact bool status with identical shape, every flag true, every result finite. It rejects incomplete entries without changing flags or replacing NaN and returns an independent writable C-order copy only on success. Executed checks reject original uncomputed workspace, one unfinished finite cell, NaN hidden behind true flags, numeric flags and shape mismatch; completed zero results are valid. This helper does not verify financial equations, label provenance, synchronization or an application memory budget, and it is not added to the manuscript API.

## 6.3-E6 — SUPPLEMENTAL EXACT POLICY + REPRESENTATION COMPARISON

**Prompt:** Compare deliberate integer-unit rounding with astype truncation using positive and negative fractional values.

Choose nearest whole units with ties to even as an explicitly separate illustrative rounding policy. Exact Fraction inputs 1.9,−1.9,1.5,2.5,−1.5,−2.5 give [2,−2,2,2,−2,−2]. Casting the corresponding float array to int64 gives [1,−1,1,2,−1,−2], truncating toward zero. The safe casting rule rejects fractional float-to-int narrowing. A deliberately chosen whole-unit rule is not a universal currency or accounting rule; specify unit scale, stage, signs, bounds and required policy before application.

## 6.3-E7 — DESIGN + EXECUTED IDENTITY-LOSS PROBE

**Prompt:** Propose a dtype policy for an identifier larger than exactly representable float64 integers.

Treat an identifier as opaque text unless the source contract explicitly defines a bounded integer identifier. Preserve spelling and leading zeros where meaningful; do not route IDs through floating arrays for convenience. For a defined numeric ID within range, int64 can preserve 2^53+1=9007199254740993, while the executed int64→float64→int64 route becomes 9007199254740992. Python integer/text round-trip retains this numeric value. Values outside int64 bounds require another explicit representation such as text or Python integers. Numeric kernels and positional label metadata should remain separate; no general identifier-ingestion adapter was implemented.

## 6.3-E8 — DESIGN NOT IMPLEMENTED + UNIT DERIVATION

**Prompt:** Describe the checks required before accepting percent text such as 2.5% in the wire format.

Before adding percent wire text, define exact string type, one trailing % token, allowed sign/spelling/whitespace policy, precision, range, units and ambiguity rules. One possible separate contract permits canonical optional-minus decimal percent numbers in [−100,100], at most four fractional percent digits, no exponent/aliases/whitespace, converting exactly by division by 100 before the existing bounded fraction boundary. This preserves at most six fractional rate digits; define canonical output and zero-sign policy explicitly. Test 2.5%,0%,±100% and rejected double signs/tokens/nonfinite/out-of-range/ambiguous mixed formats, plus provenance and no accidental percentage-point interpretation. Independent Fraction arithmetic gives 2.5/100=1/40; the original API accepts separately supplied 0.025 but still rejects 2.5%. No percent parser or new support claim is made.
