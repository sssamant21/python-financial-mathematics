# Book 02 — Substantive Coverage: Chapter 8

**Date:** 2026-10-28  
**Inspected revision:** `110ea087e00668c1080f4a57d87a5a7f01fd8a02`  
**State:** Ten sections mapped; independent derivation and numerical accuracy review pending.

Inspected manuscripts, implementations, ten numbered checks and difference-denominator regression. Mapping reaches85/215 sections (Chapters1–8). No new execution occurred. [Pinned runtime](pinned-revision-runtime-validation.md) and [derivative boundary review](chapter-08-difference-denominator-review.md) retain their original scopes.

## 8.1 — Derivative definition
Source: [checks](../chapter-08/code/check_section_8_01.py).

E1 definition/nonzero h: zero steps rejected, proof/manual. E2 derivative4x+7: exact example absent. E3 x² derivation: centered and forward values at four points, symbolic limit manual. E4 x3 slope6: exact point3 not in grid(-3,0,2,10). E5 |x| kink: matching evidence in8.8/8.9, not here. E6 PV500/t2: grid uses cash0/100/1000 and times0/1/3/10, so exact input absent. E7 matching PV10bp approximation absent. E8 marginal12-.04q: value8 at100 checked. E9 tiny-step accuracy and E10 infinitesimal vs finite: manual; profit finite change7.98 contrasts derivative8.

Stable PV quotient checks use selected±1e-6 steps; they support a limiting calculation, not a proof or an optimal step-selection rule.

## 8.2 — Power/sum/constant rules
Source: [checks](../chapter-08/code/check_section_8_02.py).

E1 constant derivative0: matching constant and coefficient result. E2 7x^5: absent exact polynomial. E3 cubic4x³-6x+9: matching derivative grid. E4 quartic derivative199 at2: matching. E5 x^-2 and E6 sqrt(x): neither implemented by polynomial coefficient helper; domains/derivations manual. E7 revenue/marginal: matching values/grid. E8 marginal cost30 and E9 marginal profit30 at100: matching. E10 finite increment29.75: matching contrast, conceptual explanation manual.

Coefficient order/constant-zero behavior, revenue domain and malformed coefficients sampled. Finite derivative agreement does not establish a general power rule, particularly outside integer polynomial powers.

## 8.3 — Product/quotient rules
Source: [checks](../chapter-08/code/check_section_8_03.py).

E1 rule proof manual. E2 x²(3x+1) and E3 rational quotient: six-point comparisons to expanded derivatives; zero denominator rejected. E4 u'v' false rule: exact x*x counterexample not asserted. E5 R'=P+qP': matching revenue-specific expression and finite differences, derivation manual. E6 marginal revenue60 and E7/E8 average-cost derivative .05: matching. E9 coverage derivative: matching time grid. E10 discounted C(t) product: analytic/finite difference at positive times; t0 finite difference deliberately skipped because central negative-time perturbation is outside its domain.

Domain-aware one-sided checks at endpoints are not thereby established.

## 8.4 — Chain rule
Source: [checks](../chapter-08/code/check_section_8_04.py).

E1 definition proof/manual. E2 (2x+1)^5 absent. E3 (3x²+2)^4: matching explicit derivative, generic chain helper and finite difference. E4 exp(-3x²)/E5 log(1+x²): exact functions absent. E6/E7 constant/variable-rate PV: finite-difference grid of variable-rate function, derivation manual. E8 matching -8exp(-.128). E9 nominal rate as function: finite-difference model at selected years/shocks; domain cases sampled. E10 log price derivative: matching price/time samples.

Callable/type validation sampled. Finite-difference comparisons may share model-function/convention errors with analytic functions.

## 8.5 — Exponential/log derivatives
Source: [checks](../chapter-08/code/check_section_8_05.py).

E1 derivative definition proof manual. E2 7exp(3x): matching derivative/finite differences. E3 5exp(-.3x²) absent. E4 log(1+2x): matching values and domain boundary-.5. E5 log10 derivative absent. E6 accumulation time/rate sensitivities: matching r*A/t*A grid. E7 accumulation1000,.04,5 checked; matching time derivative is outside rate/time grid and not separately benchmarked. E8 PV sensitivity/1bp: derivative and exact shock change at1e-4 checked; error of linear approximation not explicitly bounded. E9 prices100→103 and E10 elasticity1.5: matching values.

Stable exponential quotient reference reuses exp/expm1; it is a translation identity, not an independent high-precision primitive oracle.

## 8.6 — Higher derivatives/curvature
Source: [checks](../chapter-08/code/check_section_8_06.py).

E1 first/second/third polynomial coefficient tuples: matching. E2 x³ concavity/E3 x^4 counterexample: manual, no matching sign-change assertion. E4 cost curvature.1 absent explicit test. E5 profit maximizer160: slope0/curvature-.5 and two comparison points; global feasible-domain proof manual. E6 PV second derivative: value grid plus centered-second check; proof manual. E7 matching204682.688... input in grid. E8 second-order shock improves selected.01 example, not universal error guarantee. E9 nonnegative-flow curvature: two positive cash flows have positive d2, negative-flow example negative; all-flows proof manual. E10 small h cancellation manual.

## 8.7 — Implicit derivatives
Source: [checks](../chapter-08/code/check_section_8_07.py).

E1 circle(3,4) slope-.75 and finite difference: matching. E2 vertical point(5,0) rejected; branch interpretation manual. E3 xy+y² derivative and E4 general implicit theorem: manual/no matching function. E5 ellipse(0,2): exposure helper tested different inputs; exact point absent. E6 break-even derivative formula sampled; E7 price50/cost20/fixed1200 included grid, explicit q40 follows original equality but not separate known-value tuple. E8 bond derivatives negative on positive-flow grids and reciprocal sensitivity product1. E9 one-period payment105 gives sensitivity-.0105 matching. E10 branch switching/near-singularity hazards not directly simulated.

## 8.8 — Numerical steps
Source: [checks](../chapter-08/code/check_section_8_08.py).

E1 forward/backward/center formulas: matching cubic12.61/11.41/12.01. E2 truncation expansion proof manual. E3 cubic centered12.01 matching. E4 second quadratic2 checked. E5 roundoff mechanism manual. E6 suggested first/second steps positive/representable with second>first, but actual epsilon exponents not independently asserted. E7 duration5/E8 convexity25 matching. E9 Richardson12 matching. E10 kink centered0 vs forward1/backward-1 matching, differentiability explanation manual.

## 8.9 — Derivative comparator project
Source: [checks](../chapter-08/code/check_section_8_09.py).

R1 callable first/optional second: correct analytic results and invalid callable sampled, no complete no-second output contract assertion. R2 finite positive steps: zero/unchanged/type/nonfinite rejection plus boundary suite. R3 four first estimates and R4 second: matching cubic known values. R5 signed/absolute errors: estimates/pass flags asserted, error field definitions not independently asserted. R6 configurable tolerances/step ladder: forward fails/center passes at selected tolerance; four model factories produce three-step reports, middle step passes. R7 invalid ratio perturbation and kink disagreement: visible evidence, no automatic proof of nonsmoothness or generic branch consistency. R8 four financial factories exercised. R9 standard-library design inspected. R10 evidence-status separation manual.

Eight review statements about error order, noise, stationary points and independent references are not proved by three returned reports. No ratio-of-errors convergence order or intentionally wrong analytic derivative test is asserted.

## 8.10 — All twenty-five assessment problems
Source: [checks](../chapter-08/code/check_section_8_10.py).

| IDs | Evidence / gaps |
|---|---|
| P1 definition/x²; P2 polynomial; P3 product; P4 quotient; P5/P6 chain/exponential; P7 log domain | Related earlier checks, not matching assessment expressions/proofs |
| P8 profit125 | Slope0 and profit higher than100/150; global curvature/uniqueness proof manual |
| P9 accumulation2500,.06 and second derivative | No matching assessment assertion |
| P10 PV first/second; P11 Taylor shock | Matching numeric fields and second-order error improvement |
| P12 price80→84 | Matching log return; simple.05 not separately asserted |
| P13 demand elasticity-1.5 | No matching negative-elasticity assertion |
| P14 break-even45/15/900 | Matching q30/derivative-1 |
| P15 payment110/price100 | Matching yield.1 and inverse sensitivity-.011; dP/dy value not explicit |
| P16 cubic concavity; P17 x^4 counterexample | No matching sign-change assertions |
| P18 cubic finite differences | Centered12.01 only here; forward/backward values in8.8 |
| P19 quadratic second difference2 | Matching |
| P20 Richardson proof | Related8.8 example, derivation manual |
| P21 kink | Related8.8/8.9 values; conceptual conclusion manual |
| P22 three epsilon heuristics | Not explicitly asserted; optimality qualifications manual |
| P23 three cash-flow derivatives | Related8.6 uses different two-flow schedule |
| P24 derivative units/bp conversion | Shock computations related; units interpretation manual |
| P25 verification protocol | Requires manual test-design assessment |

Assessment report only asserts a required-key subset, not every output's schema/value. The revised centered-second test h=2e-4 has a stated relative truncation rationale; it is stronger than simply widening tolerance to suppress a failure.

## Boundary regression and gaps

[Difference-denominator suite](../chapter-08/code/check_difference_denominators.py) verifies h² underflow/overflow rejection in three modules, comparator underflow, unchanged shifts, normal quadratic2 and centered-first denominator overflow in8.8. This does not establish consistent guards in every earlier first-difference helper.

| ID | Gap | Next evidence |
|---|---|---|
| COV-49 | Derivative accuracy/convergence order not established by selected passing steps | Independent reference/error-ratio ladders and noisy/wrong-reference cases |
| COV-50 | Comparator error fields/tolerance acceptance not fully asserted | Independent signed/absolute error and boundary gates |
| COV-51 | Implicit branch/domain and first-difference guards vary | Endpoint/near-singularity and representability review across helpers |

These extend COV-01–COV-48. No new implementation defect or independent sign-off is claimed. Next: Chapter9.

## Subsequent COV-49 accuracy follow-up

The [second-difference record](chapter-08-difference-order-followup.md) adds exact polynomial error ladders, a special vanishing-coefficient case and a representable-step cancellation example. Two faulty formula variants were detected. All 21 chapter sources compiled and 11 scripts passed; algorithm unchanged. Other helper/noise/reference/range and independent-review obligations remain open.

## Subsequent COV-50 comparator follow-up

The [comparator audit](chapter-08-comparator-audit-followup.md) adds exact error-field/tolerance-boundary and wrong-reference cases, retains tolerance metadata and rejects nonfinite computed estimates/errors to prevent false passes. All 21 chapter sources compiled and 11 scripts passed. Broader comparator/reference and independent-review obligations remain open.

## Subsequent COV-51 helper-guard follow-up

The [helper guard record](chapter-08-helper-guards-followup.md) rejects nonfinite returned estimates and avoids a Richardson intermediate overflow. Selected invalid controls are checked before callbacks, with denominator and half-step cases. All 21 chapter sources compiled and 11 scripts passed. Earlier copies, implicit domains/ranges and independent review remain open.

## Subsequent normalized-sensitivity follow-up

The [sensitivity range record](chapter-08-sensitivity-range-followup.md) rejects zero price normalization and nonfinite prices/ratios, and checks independent hyperbolic-function stencil ratios at three cash-flow scales. All 21 chapter files compiled and 11 scripts passed. This extends partial COV-51 remediation; cancellation/subnormal and broader domain/review work remain open.

## Earlier derivative-helper guards — V-99

[Section 8.1 earlier-helper follow-up](chapter-08-earlier-derivative-guards-followup.md) retains ten baseline mismatches, an identical replay, an initial checker serialization failure and 25 passing corrected cases. Section 8.1 now preflights represented perturbations before callbacks and evaluates complete sampled quotients before final rounding. This adds selected COV-51 evidence. Thirty-five selected categories remain partially addressed; none are closed.

[V-99](runtime-refresh-2026-11-07-r05.md) compiled 564 files, passed 351 scripts and verified 565 required blobs before and after at `d702d2761735c11ab501900c899cae4557742a09`. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [Section 8.3 product/quotient baseline](chapter-08-product-quotient-range-baseline.md) records finite analytic product/quotient derivative results lost to intermediate overflow. Check complete expressions, callbacks and true final range without attributing completed sampled-stencil cases to those separate helpers. Remaining financial-PV and copied-helper ranges and manual review remain open.

## Complete product and quotient derivatives — V-100

[Section 8.3 analytic derivative follow-up](chapter-08-product-quotient-range-followup.md) retains eleven baseline mismatches, an identical replay and 34 passing corrected observations. Exact local-series references check complete results while actual callback traces check validation, order and single evaluation. The existing Section 8.3 suite passes. This adds selected COV-51 evidence. Thirty-five selected categories remain partially addressed; none are closed.

[V-100](runtime-refresh-2026-11-07-r06.md) compiled 565 files, passed 352 scripts and verified 566 required blobs before and after at `2f6b47559fc7baa82e59772bbdfbd6445e5374e1`. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [Section 8.3 financial rational baseline](chapter-08-financial-rational-range-baseline.md) records finite average-cost and coverage-derivative results lost to separate float terms. Reconcile complete rational-expression ranges and denominator-domain guards for the financial examples. Discounted-payment and copied finite-difference helpers and manual review remain open.

## Financial rational-expression range — V-101

[Section 8.3 financial rational follow-up](chapter-08-financial-rational-range-followup.md) retains eleven baseline mismatches, an identical replay and 41 passing corrected observations. Complete polynomial-quotient references check finite results, true range failures and adjacent-pole behavior; the exact represented coverage denominator is documented separately from its financial interpretation. The existing Section 8.3 suite passes. This adds selected COV-51 evidence. Thirty-five selected categories remain partially addressed; none are closed.

[V-101](runtime-refresh-2026-11-07-r07.md) compiled 566 files, passed 353 scripts and verified 567 required blobs before and after at `e674373645a4b9787b3a412fd8262ff9a4c30fdf`. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [Discounted-payment baseline](chapter-08-discounted-payment-range-baseline.md) records finite/zero values and a finite derivative lost to separate exponential/coefficient arithmetic. Check actual payment callbacks and complete scaling; preserve the value wrapper's unused derivative-argument behavior. Copied finite-difference and Section 8.1 financial helpers and manual review remain open.

## Discounted-payment callback range — V-102

[Section 8.3 discounted-payment follow-up](chapter-08-discounted-payment-range-followup.md) retains eleven expanded baseline mismatches, an identical replay, earlier screen/rerun and 32 passing final cases. Independent separate discounted-term references check complete coefficient scaling, zero/cancelled identities, genuine final overflow and actual callback arguments/order. The existing Section 8.3 suite passes. This adds selected COV-51 evidence. Thirty-five selected categories remain partially addressed; none are closed.

[V-102](runtime-refresh-2026-11-07-r08.md) compiled 567 files, passed 354 scripts and verified 568 required blobs before and after at `0b109a17f2ee256a3cdffeeeffb0417720bcf3ed`. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [Section 8.1 initial-PV baseline](chapter-08-initial-pv-range-baseline.md) records finite PV/derivative/stable-quotient results lost to premature underflow in Section 8.1's distinct financial functions. Preserve their domains and derive complete references. The copied Section 8.3 centered difference and other early derivative helpers and manual review remain open.

## V-103 checkpoint — 2026-11-07

[Section 8.1 financial range](chapter-08-initial-pv-range-followup.md): forty corrected checks pass; seventeen baseline mismatches and valid baseline replay retained. [Section 8.3 centered wrapper](chapter-08-centered-copy-followup.md): eight checks pass; six baseline observations retained, including two new delegation requirements. The invalid missing-directory replay setup and corrected harness are disclosed separately.

[V-103](runtime-refresh-2026-11-07-r09.md) at `a6441d707337946a76e059c6cf53a5b05291afa0`: 569 Python files compiled, 356 scripts passed, 570 required source/fixture hashes verified before/after. Counts derive from this pinned tree. Thirty-five selected COV categories remain partial, none closed; this is not a completion percentage or independent sign-off.

Next substantive work: [Section 8.2 polynomial range baseline](chapter-08-polynomial-range-baseline.md), including two confirmed finite-result failures and the remaining centered-difference copy. Resume there without repeating completed Section 8.1 financial or Section 8.3 wrapper examples. Reviewer, supported-platform, release and canonical decisions remain pending.

## V-104 checkpoint — Section 8.2

[Polynomial and centered-copy follow-up](chapter-08-polynomial-range-followup.md): 64 checks pass, with 22 baseline mismatches and a byte-identical replay retained. Exact power-sum references independently check rational Horner evaluation and point-specific derivatives; the coefficient API rejects unrepresentable outputs and the centered wrapper uses the guarded Section 8.1 helper. Initial checker serialization failure and reruns are disclosed. Existing Section 8.2 reference checks also pass.

[V-104](runtime-refresh-2026-11-07-r10.md) at `78b09101177563c3511c1932f6a4e7469567e7bc`: 570 files compiled, 357 scripts passed, 571 required hashes verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer sign-off, supported platforms, release acceptance and canonical approval remain pending.

Next substantive obligation: [Section 8.2 financial cost-output baseline](chapter-08-cost-output-baseline.md), where a finite accepted quantity returns infinity. Derive complete financial references and establish the finite-output contract; do not repeat the completed polynomial or centered-copy corpus.

## V-105 checkpoint — Section 8.2 cost output

[Cost-output follow-up](chapter-08-cost-output-followup.md) retains four baseline mismatches and an identical replay; all 50 corrected checks pass. Thirty-two independent Decimal value/derivative references establish complete-expression rounding, twelve guard checks preserve quantity domains, and six composition regressions preserve profit call relationships. Three returned infinities now raise OverflowError; one one-ulp difference is reconciled under the explicit new rounding policy. No marginal-cost baseline failure is claimed. Existing Section 8.2 and polynomial-range suites pass.

[V-105](runtime-refresh-2026-11-07-r11.md) at `7db1525c2f390b0eb9afa431c08648b6450737d3`: 571 files compiled, 358 scripts passed, 572 required blobs verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [Section 8.4 callback and centered-copy baseline](chapter-08-chain-callback-baseline.md). Actual probes retain a nonfinite chain product, an identity quotient yielding NaN instead of 1, and collapsed perturbations that still invoke callbacks. Preserve callback order/count and derive full sampled quotient/error contracts; do not repeat completed Section 8.2 cost/polynomial examples.

## V-106 checkpoint — Section 8.4 callback and centered copy

[Chain callback follow-up](chapter-08-chain-callback-followup.md): all 55 checks pass; ten baseline mismatches and an identical original-source replay retained. Independent Decimal products and exact sampled quotient references check actual Section 8.4 calls. Callback arguments/order/counts, short circuit, exception identity, signed zero/underflow, default step and callable-before-controls precedence are checked. Nonfinite final chain products reject and invalid perturbations reject before callbacks. The existing Section 8.4 suite also passes.

[V-106](runtime-refresh-2026-11-07-r12.md) at `9d138bf2bd1fa0ab5806d0ec3e9202b0f26f2cf1`: 572 files compiled, 359 scripts passed, 573 required blobs verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [Section 8.4 variable-rate PV baseline](chapter-08-variable-rate-pv-baseline.md). Actual probes lose finite complete PV/sensitivity results to underflow and return NaN for zero amount. Independent 200/400-digit references agree for the returned represented rate. Establish complete scaling and zero identities while preserving the intended factor-rate convention; do not repeat completed callback/centered-copy examples.

## V-107 checkpoint — Section 8.4 variable-rate PV

[Variable-rate PV follow-up](chapter-08-variable-rate-pv-followup.md): all 63 checks pass; sixteen baseline mismatches, an identical replay and corrected rerun retained. Independent 1800/2400-digit log-scale references check complete coefficients/exponents, zero identities and finite sensitivity recovery when PV rounds to zero. Six independently rounded affine-rate cases preserve the public rate convention. Input domains, signed zeros and validation precedence remain checked. The strengthened validation-priority discriminator did not change observation JSON. Existing Section 8.4 and callback suites also pass.

[V-107](runtime-refresh-2026-11-07-r13.md) at `21ebbc28a1b08b93c9103d791c90d6bab15ec815`: 573 files compiled, 360 scripts passed, 574 required blobs verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [Section 8.4 discrete-compounding baseline](chapter-08-discrete-compounding-range-baseline.md), with [three retained value/sensitivity probe pairs](chapter-08-discrete-compounding-range-baseline.json). Actual intermediate overflow/underflow loses finite complete values and zero-principal identities. Preserve the intended nominal-rate/base/exponent conventions while deriving full results; do not repeat completed variable-rate PV examples.

## V-108 checkpoint — Section 8.4 discrete compounding

[Discrete-compounding follow-up](chapter-08-discrete-compounding-range-followup.md): all 74 expanded checks pass; sixteen expanded baseline mismatches and a byte-identical replay retained. The initial 69-case baseline/corrected run is also retained. Exact rational integer powers and independent Decimal direct powers at 1600/2200 digits check complete values/sensitivities. Selected rounded bases, exact n·t and n·t−1 behavior near 2^53, signed zero identities, final output/error policy and invalid base/count/quantity behavior are checked. Existing Section 8.4 and variable-rate PV suites pass.

[V-108](runtime-refresh-2026-11-07-r14.md) at `df9ac9bf2952edc78ec5264a25d7caf7f90a21e5`: 574 files compiled, 361 scripts passed, 575 required blobs verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [large integer period-count baseline](chapter-08-large-period-count-baseline.md), with [three retained value/sensitivity probe pairs](chapter-08-large-period-count-baseline.json). Count 10**400 is accepted by the positive-integer guard but base division raises OverflowError despite finite rounded-base expectations. Extend conversion while preserving already working base conventions; do not repeat completed power-scaling examples.

## V-109 checkpoint — Section 8.4 large period counts

[Large-count follow-up](chapter-08-large-period-count-followup.md): all 78 checks pass; forty-two baseline observations and a byte-identical replay retained. Fourteen base/value/sensitivity triples fail at the same original conversion point; this is not forty-two distinct defects. Independent Decimal count conversion and direct powers at 1600/2200 digits check conversion thresholds, huge counts with nonzero quotients and working 2^53+1 denominator rounding. The fallback is used only when float/int division overflows. Existing Section 8.4 and 74-case compounding suites pass.

[V-109](runtime-refresh-2026-11-07-r15.md) at `a93acb89609087281b4e1872c6420313ddf7adca`: 575 files compiled, 362 scripts passed, 576 required blobs verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [nested-power range baseline](chapter-08-nested-power-range-baseline.md), with [five exact-polynomial/actual probe pairs](chapter-08-nested-power-range-baseline.json). Actual finite outputs differ from one-rounding references and nonfinite outputs/errors are inconsistent; establish the accuracy/overflow contract before editing. Price/log-growth, other earlier copies and independent review remain open. Do not repeat completed count-conversion or compounding examples.

## V-110 checkpoint — Section 8.4 nested-power derivative

[Nested-power follow-up](chapter-08-nested-power-range-followup.md): all 45 checks pass; seventeen baseline mismatches and an identical replay retained. Independent expanded rational monomials check a factored rational implementation with one final rounding. An oracle-only monotone float-bit search finds adjacent finite/overflow inputs; both signs, tiny values, seeded magnitudes and type/domain guards are checked. Six baseline infinities now raise OverflowError; eleven finite differences are reconciled under the explicit accuracy contract. Existing Section 8.4 and 78-case large-count suites pass.

[V-110](runtime-refresh-2026-11-07-r16.md) at `76208b8f944cf6ab706ae75f94cc0329d1f3dbfe`: 576 files compiled, 363 scripts passed, 577 required blobs verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [price/log-growth baseline](chapter-08-price-log-growth-baseline.md), with [five retained probe pairs](chapter-08-price-log-growth-baseline.json). Price returns infinity at 1e104 while larger unrepresentable cases raise OverflowError; selected log-growth outputs match their represented-ratio references. Establish price output/accuracy consistency and preserve or explicitly reconcile the rounded base and represented coefficient convention. Do not repeat completed nested-power/count examples.

## V-111 checkpoint — Section 8.4 price/log-growth contracts

[Price/log-growth follow-up](chapter-08-price-log-growth-followup.md): all 62 checks pass; nine baseline price mismatches and an identical replay retained. Two returned infinities now raise OverflowError; seven finite differences are reconciled under the explicit complete-cubic rounding contract. Independent two-stage affine bases, exact Decimal cubic products, rational growth ratios and an oracle-only adjacent price boundary search preserve existing represented-base semantics. Log-growth code is unchanged; its endpoint/monotonicity finite-output argument states binary64 rounding assumptions. Existing Section 8.4 and nested-power suites pass.

[V-111](runtime-refresh-2026-11-07-r17.md) at `99ef9ddc1fab5e20ca83df6254d639720ff23b36`: 577 files compiled, 364 scripts passed, 578 required blobs verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [Section 8.5 exponential-derivative baseline](chapter-08-exponential-derivative-range-baseline.md), with [four retained probes](chapter-08-exponential-derivative-range-baseline.json). Separate coefficient/exponential arithmetic loses finite signed results and zero-scale identities. Establish complete represented-input scaling and final output/error conventions while preserving type/domain behavior; other Section 8.5 helper/copy and independent review obligations remain open. Do not repeat completed Section 8.4 price/nested-power examples.

## V-112 checkpoint — Section 8.5 exponential derivative

[Exponential-derivative follow-up](chapter-08-exponential-derivative-range-followup.md): all 34 checks pass; fourteen baseline mismatches and a byte-identical replay retained. Independent log-amplitude references at 1600/2200 digits and exact special cases check complete coefficient/exponent scaling, signed zeros, tiny inputs and true final overflow. One ordinary rounding difference is reconciled under the explicit complete-expression contract. Zero-sign flags and raw stdout hashes preserve sign details across JSON serialization. Existing Section 8.5 checks pass.

[V-112](runtime-refresh-2026-11-07-r18.md) at `8a23628022d832fbd80422aaf6ca582b28917de6`: 578 files compiled, 365 scripts passed, 579 required blobs verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [logarithm-derivative baseline](chapter-08-logarithm-derivative-range-baseline.md), with [four retained probes](chapter-08-logarithm-derivative-range-baseline.json). Three positive-argument examples lose finite complete ratios; a cancellation-domain example requires explicit reconciliation of exact represented versus rounded argument policies. Derive signed/zero/overflow quotient expectations and preserve validation behavior. Other Section 8.5 financial and copied-helper obligations remain open. Do not repeat completed exponential-derivative or Section 8.4 examples.

## V-113 checkpoint — Section 8.5 logarithm derivative

[Logarithm-derivative follow-up](chapter-08-logarithm-derivative-range-followup.md): all 33 checks pass; seven baseline mismatches and an identical replay retained. Independent Decimal rounded-domain operations and rational reciprocal references check complete quotient recovery, signed zero/underflow and final output guards. The rounded-positive argument gate is explicitly retained, including the cancellation probe's ValueError; the domain is not widened. Existing Section 8.5 and 34-case exponential suites pass.

[V-113](runtime-refresh-2026-11-07-r19.md) at `04f45d68c3aaf1c3a25838fba4417df5198614c0`: 579 files compiled, 366 scripts passed, 580 required blobs verified before/after. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [accumulation scaling baseline](chapter-08-accumulation-range-baseline.md), with [four retained value/time/rate triples](chapter-08-accumulation-range-baseline.json). Complete Decimal references at 200/400 digits expose finite-result loss, zero identities and sensitivities that remain finite when the value itself is unrepresentable. Establish scaling/output policy and preserve input domains/order. PV/shock, log-return, stable quotient and centered-copy obligations remain open. Do not repeat completed exponential/logarithm derivative examples.

## V-114 checkpoint — Section 8.5 accumulation scaling

[Accumulation follow-up](chapter-08-accumulation-range-followup.md): all 137 checks pass; 37 baseline mismatches and a byte-identical replay retained. Independent 1600/2200-digit log-amplitude references check complete values and sensitivities, signed zero/underflow, true final overflow and validation precedence. Two baseline mismatches enforce the new no-rounded-value-delegation requirement; mismatches are not distinct defect counts. Existing Section 8.5, exponential and logarithm suites pass.

At `a2de6dbfdacb2ef34d30674ee51b5509a8dc4f35`, six scoped files compiled and four scripts passed, with six source/checker hashes verified before/after. Fresh full-tree inventory: 580 Python files, 367 check/test scripts and 581 required source/fixture blobs. This is scoped validation; V-113 remains the latest full candidate Linux run (579/366/580 at its earlier revision). Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [PV/rate-sensitivity baseline](chapter-08-pv-range-baseline.md), with [four pinned actual probe pairs](chapter-08-pv-range-baseline.json). Complete 200/400-digit references expose finite-result loss, nonzero sensitivity beside a zero price, finite sensitivity beside unrepresentable PV and lost zero-payment identities. Establish the final-output/scaling policy and preserve input order/domains, then address rate shock. Log-return, stable quotient, centered copy, resource limits and independent review remain open. Do not repeat the completed accumulation, exponential or logarithm corpus.

## V-115 checkpoint — Section 8.5 PV and rate sensitivity

[PV/rate-sensitivity follow-up](chapter-08-pv-range-followup.md): all 93 checks pass; 26 baseline mismatches and a byte-identical replay retained. Independent 1600/2200-digit log-amplitude references check complete values/sensitivities, signed zero/underflow, true final overflow and validation priority. One baseline mismatch enforces the new direct-sensitivity requirement; mismatches are not distinct defect counts. Pinned corrected observations match local results.

[V-115 full runtime](runtime-refresh-2026-11-08.md) at `536dc531ca19a913507977f63df20d2cefd1f90b`: 581 Python files compiled, 368 scripts passed and 582 required source/fixture hashes verified before/after. This fresh pinned-tree run includes both V-114 accumulation and V-115 PV checkers. Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [rate-shock baseline](chapter-08-rate-shock-range-baseline.md), with [four pinned actual probe/reference pairs](chapter-08-rate-shock-range-baseline.json). Independent complete-price differences at 1600/2200 digits expose finite-change loss through intermediate PV/exponential/product range and a lost zero-payment identity. Preserve years/change prevalidation and remaining input domains/order, explicitly reconcile shifted-rate/exponent/final-output conventions, then continue log-return, stable quotient and centered copy. Resource limits and independent review remain open. Do not repeat completed PV/sensitivity or accumulation examples.

## V-116 checkpoint — Section 8.5 complete rate shock

[Rate-shock follow-up](chapter-08-rate-shock-range-followup.md): all 57 checks pass; 14 baseline mismatches and a byte-identical replay retained. Independent complete Decimal price differences at 1600/2200 digits check signed shocks, tiny products, large/cancelled exponents, zero identities, final overflow and validation priority. One baseline mismatch enforces the new complete-change independence requirement; mismatches are not distinct defect counts. Pinned corrected observations match local results.

At `63ff224ef85691be6a513db55f27c3f567889f76`, eight scoped Python files compiled and six scripts passed, with eight exact Git blobs verified before/after. Fresh full-tree inventory is 582 Python files, 369 check/test scripts and 583 required source/fixture blobs. This is scoped validation; [V-115](runtime-refresh-2026-11-08.md) remains the latest full candidate Linux pass (581/368/582 at its earlier revision). Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer, supported-platform, release and canonical decisions remain pending.

Next: [log-return baseline](chapter-08-log-return-range-baseline.md), with [eight pinned observations](chapter-08-log-return-range-baseline.json): four finite-model range failures and four working half-price, adjacent-unity and equal-price controls. Derive a range-safe evaluation while preserving near-unity accuracy, positive-price domains, validation order and equal-price zero behavior. Stable quotient, centered-copy, resource limits and independent review remain open. Do not repeat completed rate-shock/PV/accumulation examples.
