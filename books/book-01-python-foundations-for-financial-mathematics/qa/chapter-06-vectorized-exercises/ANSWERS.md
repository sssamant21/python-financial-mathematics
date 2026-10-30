# Section 6.5 — Eight scoped answers

Prerequisites: the Section 6.1 prepared runtime, unchanged sibling listings, aligned exact float64 vectors and caller-guaranteed position identity/currency/unit conventions. Review: Codex executor, 2026-10-30; not independent acceptance.

## 6.5-E1

Add a long position with quantity 2, start price 40, and end price 35; derive every output before running.

**EXACT SOURCE + INDEPENDENT INTEGER ORACLE**. Append quantity 2, start 40, end 35 as LONG-D to all three aligned vectors and the external ID tuple. Derive opening 2×40=80, closing 2×35=70 and price-only change 2×(35−40)=−10 before calling source. The four-position outputs are opening [1000,−400,0,80], closing [1050,−380,0,70], change [50,20,0,−10], each shape (4,). Caller arrays remain byte-identical and outputs do not share their storage.

## 6.5-E2

Add a short position whose price rises and verify the sign of its price-only change.

**EXACT SOURCE + INDEPENDENT INTEGER ORACLE**. Choose quantity −3, start 20, end 25. Opening mark is −60, closing mark −75 and price-only change −3×5=−15. A rising price loses value for this fixed short quantity. Negative marks are not account equity: proceeds, collateral, financing, cash flows and trades remain excluded. All three outputs are checked.

## 6.5-E3

Add tests that nonfinite end prices fail even for a zero quantity.

**EXACT SOURCE REJECTION PROBES**. For quantity 0 and valid start 50, independently supply NaN, positive infinity and negative infinity as the end price. All three calls raise ValueError before returning results. This adds explicit end-price predicates beyond the existing source test of bad start prices. Expected tracebacks and unchanged input-byte comparisons are retained; no original test listing is edited.

## 6.5-E4

Compare q*(end-start) with q*end-q*start on large nearby values; document observed finite-precision differences without assuming one formula always wins.

**FINITE-PRECISION OBSERVATION + EXACT BINARY-INPUT ORACLE**. Use start 10^16 and end 10^16+2, two distinct representable nearby float64 values. With quantity 3 the direct formula gives 6, but rounded closing minus opening gives 8; exact Fraction arithmetic on the represented inputs gives 6. With binary64 quantity 0.1 the direct result is 0.2 and the alternative 0.25. The exact represented-input result is 3602879701896397/18014398509481984; retained hex inputs and rational errors distinguish binary-input arithmetic from the intended decimal quantity 1/10. No overflow or invalid signal occurs; finite results alone do not imply adequate precision. These controlled observations favor the direct formula for these inputs only, not a theorem that it always wins. The original source uses the direct formula and is checked against each result.

## 6.5-E5

Specify the inputs and sign conventions needed to add a cash distribution per unit.

**DESIGN REVIEW + SUPPLEMENTAL RATIONAL EXAMPLE**. For a simple extension require fixed signed quantity, an aligned distribution-per-unit vector in the same currency/per-unit basis as prices, eligibility/record-date and payment-date policy, observation interval, gross/net tax and withholding conventions, and treatment of reinvestment. Under the explicit assumption that every held unit is entitled throughout the interval, cash flow=q×d and combined change=q×(end−start+d). Positive d pays a long, requires a short to pay, and yields zero for flat quantity. At d=0.5, quantities 2,−3,0 yield cash 1,−1.5,0; combined changes for the preceding long and short examples are −9 and −16.5. Rational predicates execute these illustrative equations only; no distribution API, entitlement engine or source change is implemented.

## 6.5-E6

Explain why summing these outputs across mixed currencies is not meaningful without another policy.

**DESIGN REVIEW + SUPPLEMENTAL RATIONAL EXAMPLE**. USD and EUR amounts have different units, so a bare sum has no single currency meaning. Keep currency groups separate or specify a reporting currency, FX quote direction, timing, source, stale/missing-rate policy and rounding before conversion and aggregation. Illustratively, 10 USD plus 20 EUR at 1.10 USD/EUR is 32 USD, not an unlabelled raw sum 30. This rational unit example is not an implemented FX service. For changes over time, start/end FX effects and cash-flow timing require a fuller model than one arbitrary common rate.

## 6.5-E7

Design a scenario-by-position extension, stating axis semantics before choosing broadcast shapes.

**DESIGN REVIEW + EXISTING SOURCE ROW CHECKS**. Declare scenario axis 0 and aligned position axis 1: end prices (S,N), fixed start prices (N,), quantities (N,), with explicit (1,N) views when implementing broadcasts. Define opening per-position (N,), scenario closing (S,N), scenario price-only change (S,N), named scenario IDs (S) and position IDs (N); label and currency alignment precedes shape checks. An illustrative S=2,N=2 design uses q=[2,−3], start=[40,20], ends=[[35,25],[45,15]], yielding changes [[−10,−15],[10,15]] by rational arithmetic. Each scenario is verified using the unchanged one-dimensional source separately. A broadcast extension is not implemented: it would need a distinct API, nonempty dimension/budget guards, no accidental position expansion, finite/nonnegative whole-input checks, strict local error policy, independent storage and invalid-shape/nonfinite/overflow tests.

## 6.5-E8

Plan a fair benchmark that checks numerical agreement before measuring runtime.

**BENCHMARK PLAN + EXECUTED AGREEMENT PREFLIGHT**. Plan equivalent fixed-quantity native-array and scalar-loop implementations of all three outputs with the same supported inputs, validation/error policy and independent return arrays. Check equal shapes, identity order, known integer answers, fractional and cancellation-sensitive cases, explicit rtol/atol with NaNs disallowed, and rejection behavior before starting timers. Execute no timing when agreement fails; retain raw errors and agreed tolerances tied to magnitude/purpose. Use deterministic retained inputs, representative sizes, warmups, repeated interleaved measurement order, perf_counter or timeit, matched conversion/allocation scope, controlled thread settings, environment versions and raw samples; report median/spread and memory separately. Do not equate np.vectorize with native kernels or extrapolate one size to production. This batch executes a four-position known-answer preflight and original scalar-reference suite, not the planned benchmark. No speedup claim or complete benchmark harness is made.
